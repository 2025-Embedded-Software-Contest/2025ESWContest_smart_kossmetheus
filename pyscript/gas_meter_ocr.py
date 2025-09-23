import os
import base64
import json
import requests
from datetime import datetime
from PIL import Image
import io

# OpenAI API 설정
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

# 전역 컨텍스트에서 API 키 가져오기
@service
def get_openai_api_key():
    return pyscript_vars.get('openai_api_key', 'YOUR_API_KEY_HERE')

@service
def gas_meter_image_ocr(input_image=None, output_image=None):
    """yaml
    name: gas_meter_image_ocr
    description: Gas meter OCR using OpenAI Vision API
    fields:
      input_image:
        example: /config/www/tmp/gas/latest.jpg
        required: true
        selector:
          text:
      output_image:
        description: Processed output image path
        example: /config/www/tmp/gas/processed.jpg
        required: false
        selector:
          text:
    """
    """Gas meter OCR using OpenAI Vision API"""

    if not input_image or not os.path.exists(input_image):
        log.error(f"Input image not found: {input_image}")
        return

    try:
        # 이미지 전처리 (회전, 크롭 등)
        processed_image = preprocess_gas_meter_image(input_image)

        # OpenAI Vision API로 OCR 수행
        ocr_result = perform_ocr(processed_image)

        # 결과 처리
        process_ocr_result(ocr_result, input_image)

        # 처리된 이미지 저장
        if output_image:
            output_folder = os.path.dirname(output_image)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            processed_image.save(output_image)

        log.info(f"Gas meter OCR completed successfully: {ocr_result}")

    except Exception as e:
        log.error(f"Error in gas_meter_image_ocr: {e}")
        # 에러 발생 시 메시지 업데이트
        input_text.set_value("gas_message_2", f"OCR Error: {str(e)}")

def preprocess_gas_meter_image(image_path):
    """이미지 전처리: 회전, 크롭, 대비 조정 등"""
    try:
        image = Image.open(image_path)

        # 이미지 회전 (필요시 조정)
        # image = image.rotate(-90, expand=True)  # 시계 반대방향 90도 회전

        # 이미지 크롭 (검침기 숫자 부분만 추출)
        # 실제 카메라 위치에 따라 좌표 조정 필요
        width, height = image.size
        # crop_box = (left, top, right, bottom)
        # image = image.crop((100, 100, width-100, height-200))

        # 이미지 리사이즈 (OCR 정확도 향상)
        # image = image.resize((800, 600))

        # 이미지 대비 향상
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # 대비 1.5배 향상

        return image

    except Exception as e:
        log.error(f"Error in preprocess_gas_meter_image: {e}")
        return Image.open(image_path)  # 전처리 실패시 원본 반환

def perform_ocr(image):
    """OpenAI Vision API를 사용한 OCR"""
    try:
        # API 키 가져오기
        api_key = pyscript_vars.get('openai_api_key')
        if not api_key or api_key == 'YOUR_API_KEY_HERE':
            log.error("OpenAI API key not configured")
            return None

        # 이미지를 base64로 인코딩
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "이 이미지에서 가스 검침기의 숫자 값을 정확히 읽어주세요. 현재 검침값만 숫자로만 답변해주세요. 예를 들어 12345.678 이런 형태로 답변해주세요. 다른 설명은 하지 마세요."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }

        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            ocr_text = result["choices"][0]["message"]["content"].strip()

            # 숫자만 추출
            import re
            numbers = re.findall(r'\d+\.?\d*', ocr_text)
            if numbers:
                return float(numbers[0])
            else:
                return None
        else:
            log.error(f"OpenAI API error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        log.error(f"Error in perform_ocr: {e}")
        return None

def process_ocr_result(ocr_result, original_image):
    """OCR 결과 처리 및 Home Assistant 엔티티 업데이트"""
    try:
        if ocr_result is not None:
            # 가스 검침값 업데이트
            current_value = float(input_number.get_value("gas_meter_2") or 0)
            new_value = float(ocr_result)

            # 값이 유효한 범위 내인지 확인 (너무 큰 변화는 무시)
            if abs(new_value - current_value) < 1000:  # 1000 이상 차이는 오류로 간주
                input_number.set_value("gas_meter_2", new_value)

                # 성공 메시지
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                input_text.set_value("gas_message_2", f"OCR Success: {new_value} m³ at {timestamp}")

                log.info(f"Gas meter updated: {current_value} -> {new_value}")

                # 월별 사용량 자동 계산 (이전값과 차이)
                if current_value > 0:
                    monthly_usage = new_value - current_value
                    log.info(f"Monthly gas usage: {monthly_usage} m³")
            else:
                # 이상치 감지
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                input_text.set_value("gas_message_2", f"OCR Anomaly: {new_value} (prev: {current_value}) at {timestamp}")
                log.warning(f"Anomalous gas meter reading: {current_value} -> {new_value}")
        else:
            # OCR 실패
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            input_text.set_value("gas_message_2", f"OCR Failed at {timestamp}")
            log.error("OCR failed to extract value")

    except Exception as e:
        log.error(f"Error in process_ocr_result: {e}")
        input_text.set_value("gas_message_2", f"Processing Error: {str(e)}")

# Helper function to get entity values
def get_entity_value(entity_id):
    """Get current value of an entity"""
    try:
        state = state.get(entity_id)
        return float(state.state) if state and state.state != 'unknown' and state.state != 'unavailable' else 0
    except:
        return 0

# Helper function to set entity values
def set_entity_value(entity_id, value):
    """Set value of an input_number entity"""
    try:
        if 'input_number' in entity_id:
            input_number.set_value(entity_id, value)
        elif 'input_text' in entity_id:
            input_text.set_value(entity_id, value)
    except Exception as e:
        log.error(f"Error setting {entity_id} to {value}: {e}")
