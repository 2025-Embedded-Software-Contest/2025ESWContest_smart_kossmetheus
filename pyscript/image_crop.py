import os
from PIL import Image

try:
    import cv2  # Optional dependency
except ImportError:  # pragma: no cover
    cv2 = None

# Pyscript 환경에서만 서비스로 등록 (일반 파이썬에서는 함수로 사용)
try:
    # Pyscript 환경 확인
    pyscript_executor
    PyscriptMode = True
except NameError:
    PyscriptMode = False

if PyscriptMode:
    # Pyscript 환경에서 서비스로 등록
    try:
        # 실제 Pyscript 서비스 데코레이터 사용
        from pyscript import service as pyscript_service
        service = pyscript_service
    except ImportError:
        # Fallback: 직접 서비스 등록 함수 구현
        def service(func):
            # 서비스로 등록하는 간단한 구현
            func._is_service = True
            return func
else:
    service = lambda func: func  # 일반 파이썬에서는 그냥 함수로 사용


def detect_digit_area(image_path):
    """
    가스 검침기 이미지에서 숫자 영역을 자동으로 감지합니다.
    """
    try:
        if cv2 is None:
            raise RuntimeError("OpenCV(opencv-python)가 설치되어 있지 않습니다")

        # OpenCV로 이미지 로드
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"이미지를 로드할 수 없습니다: {image_path}")

        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 가우시안 블러로 노이즈 제거
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # 엣지 검출
        edges = cv2.Canny(blurred, 50, 150)

        # 윤곽선 찾기
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 숫자 영역으로 보이는 사각형 윤곽선 찾기
        digit_contours = []

        for contour in contours:
            # 윤곽선 면적이 너무 작거나 큰 것은 제외
            area = cv2.contourArea(contour)
            if 500 < area < 50000:  # 면적 범위 조정 가능
                # 윤곽선을 감싸는 사각형 구하기
                x, y, w, h = cv2.boundingRect(contour)

                # 숫자 영역의 특징: 너비와 높이 비율이 적당하고, 가로로 길쭉한 형태
                aspect_ratio = w / h if h > 0 else 0
                if 1.5 < aspect_ratio < 8.0 and h > 30:  # 숫자 디스플레이 영역의 특징
                    digit_contours.append((x, y, w, h, area))

        if not digit_contours:
            # 기본 영역 설정 (이미지 중앙 부분)
            height, width = image.shape[:2]
            return (width//4, height//3, width*3//4, height*2//3)

        # 면적이 가장 큰 윤곽선을 선택 (가장 큰 숫자 디스플레이 영역)
        digit_contours.sort(key=lambda x: x[4], reverse=True)
        x, y, w, h, _ = digit_contours[0]

        # 여유 공간을 두어 크롭 영역 설정
        padding = 10
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + padding * 2)
        h = min(image.shape[0] - y, h + padding * 2)

        return (x, y, x + w, y + h)

    except Exception as e:
        log.error(f"자동 숫자 영역 감지 실패: {e}")
        # 실패시 기본 영역 반환
        if cv2 is not None:
            image = cv2.imread(image_path)
            if image is not None:
                height, width = image.shape[:2]
                return (width // 4, height // 3, width * 3 // 4, height * 2 // 3)
        return (0, 0, 100, 100)


# 테스트용 함수 (개발 시에만 사용)
@service
def test_gas_meter_detection(input_image=None):
    """yaml
    name: test_gas_meter_detection
    description: 가스 검침기 숫자 영역 감지 테스트
    fields:
      input_image:
        description: 테스트할 이미지 경로
        example: /config/www/gas_latest.jpg
        required: true
        selector:
          text:
    """
    """가스 검침기 숫자 영역 감지 테스트"""
    try:
        if cv2 is None:
            raise RuntimeError("OpenCV(opencv-python)가 설치되어 있지 않습니다")
        crop_box = detect_digit_area(input_image)
        log.info(f"감지된 숫자 영역: {crop_box}")

        # 원본 이미지 로드
        original = cv2.imread(input_image)
        if original is not None:
            # 감지된 영역에 사각형 그리기
            x, y, right, bottom = crop_box
            cv2.rectangle(original, (x, y), (right, bottom), (0, 255, 0), 3)

            # 결과 이미지 저장 (www 폴더에)
            output_path = input_image.replace('.jpg', '_detected.jpg')
            cv2.imwrite(output_path, original)
            log.info(f"감지 결과 이미지가 저장되었습니다: {output_path}")

        return crop_box

    except Exception as e:
        log.error(f"감지 테스트 실패: {e}")
        return None

@service
def image_crop(input_image=None, output_image=None, rotation_angle_before=None, left=None, top=None, right=None, bottom=None, rotation_angle=None, auto_detect=False):
  """yaml
name: image_crop
description: image_crop service / pyscript.
fields:
  input_image:
    example: /congig/www/image.jpg
    required: true
    selector:
      text:
  output_image:
    description: 폴더 지정시 폴더 없으면 생성!
    example: /congig/www/image.jpg
    required: true
    selector:
      text:
  rotation_angle_before:
    description: rotation angle -360 ~ 360
    example: -90
    required: true
    selector:
      number:
        min: -360
        max: 360
        step: 0.1
        mode: box
  left:
    description: crop start X point
    example: 100
    required: true
    selector:
      number:
        min: 0
        step: 1
        mode: box
  top:
    description: crop start Y point
    example: 100
    required: true
    selector:
      number:
        min: 0
        step: 1
        mode: box
  right:
    description: crop end X point
    example: /congig/www/image.jpg
    required: true
    selector:
      number:
        min: 0
        step: 1
        mode: box
  bottom:
    description: crop image end Y point
    example: 400
    required: true
    selector:
      number:
        min: 0
        step: 1
        mode: box
  rotation_angle:
    description: rotation angle -360 ~ 360
    example: -90
    required: true
    selector:
      number:
        min: -360
        max: 360
        step: 0.1
        mode: box
  auto_detect:
    description: 숫자 영역을 자동으로 감지하여 크롭 (True/False)
    example: true
    required: false
    default: false
    selector:
      boolean:
"""
  """image_crop using pyscript with automatic digit area detection for gas meter OCR."""
  log.info(f"image_crop: got input_image {input_image}, output_image {output_image}, rotation_angle_before {rotation_angle_before}, left {left}, top {top}, right {right}, bottom {bottom}, rotation_angle {rotation_angle}, auto_detect {auto_detect}")

  # 자동 감지 모드인 경우 좌표 검증을 하지 않음
  if auto_detect and (left is not None or top is not None or right is not None or bottom is not None):
      log.warning("Auto detect mode enabled - manual coordinates will be ignored")

  try:
    # Open the input image
    image = Image.open(input_image)

    # Rotate the image before cropping (if specified)
    if rotation_angle_before and rotation_angle_before != 0:
        image = image.rotate(rotation_angle_before)
        log.info(f"이미지를 {rotation_angle_before}도 회전했습니다")

    # 크롭 영역 결정 (자동 감지 또는 수동 설정)
    if auto_detect:
        if cv2 is None:
            raise RuntimeError("auto_detect 기능을 사용하려면 OpenCV(opencv-python)가 필요합니다")
        # 자동 숫자 영역 감지
        crop_box = detect_digit_area(input_image)
        log.info(f"자동 감지된 숫자 영역: {crop_box}")
    else:
        # 수동으로 설정된 좌표 사용
        if not all([left is not None, top is not None, right is not None, bottom is not None]):
            raise ValueError("수동 크롭 모드에서는 left, top, right, bottom 좌표가 모두 필요합니다")
        crop_box = (left, top, right, bottom)
        log.info(f"수동 설정된 크롭 영역: {crop_box}")

    # Crop the image to the specified region
    image = image.crop(crop_box)
    log.info(f"이미지를 크롭했습니다: {crop_box}")

    # Rotate the cropped image (if specified)
    if rotation_angle and rotation_angle != 0:
        image = image.rotate(rotation_angle)
        log.info(f"크롭된 이미지를 {rotation_angle}도 회전했습니다")

    # 출력 이미지 폴더 경로
    output_folder = os.path.dirname(output_image)

    # 폴더가 있는지 확인하고 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the cropped image as a new JPEG file
    image.save(output_image)

  except Exception as e:
    log.error(f"이미지 크롭 중 오류 발생: {e}")


@service
def gas_meter_crop(input_image=None, output_image=None, rotation_angle_before=0, rotation_angle=0):
    """yaml
    name: gas_meter_crop
    description: 가스 검침기 숫자 영역 자동 크롭 서비스 (OCR용)
    fields:
      input_image:
        description: 입력 이미지 경로 (ESP32-CAM 촬영 이미지)
        example: /config/www/gas_latest.jpg
        required: true
        selector:
          text:
      output_image:
        description: 출력 이미지 경로 (크롭된 숫자 영역)
        example: /config/www/gas_crop.jpg
        required: true
        selector:
          text:
      rotation_angle_before:
        description: 크롭 전 회전 각도 (-180 ~ 180)
        example: -90
        default: 0
        required: false
        selector:
          number:
            min: -180
            max: 180
            step: 1
            mode: box
      rotation_angle:
        description: 크롭 후 회전 각도 (-180 ~ 180)
        example: 0
        default: 0
        required: false
        selector:
          number:
            min: -180
            max: 180
            step: 1
            mode: box
    """
    """가스 검침기 숫자 영역을 자동으로 크롭합니다 (OCR용)."""
    log.info(f"가스 검침기 크롭 시작: {input_image} -> {output_image}")

    try:
        # 자동 감지 모드로 크롭 실행
        image_crop(
            input_image=input_image,
            output_image=output_image,
            rotation_angle_before=rotation_angle_before,
            rotation_angle=rotation_angle,
            auto_detect=True
        )

        log.info("가스 검침기 숫자 영역 크롭 완료")
        return True

    except Exception as e:
        log.error(f"가스 검침기 크롭 실패: {e}")
        return False
