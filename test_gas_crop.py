#!/usr/bin/env python3
"""
가스 검침기 숫자 영역 자동 감지 테스트 스크립트
"""

import os
import sys
import cv2
import numpy as np

# 현재 디렉토리를 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pyscript.image_crop import detect_digit_area


def test_gas_meter_detection(image_path):
    """가스 검침기 숫자 영역 감지 테스트"""
    print(f"테스트할 이미지: {image_path}")

    try:
        # 이미지 파일 존재 확인
        if not os.path.exists(image_path):
            print(f"오류: 이미지 파일이 존재하지 않습니다 - {image_path}")
            return None

        # 이미지 로드 및 기본 정보 출력
        image = cv2.imread(image_path)
        if image is None:
            print(f"오류: 이미지를 로드할 수 없습니다 - {image_path}")
            return None

        height, width = image.shape[:2]
        print(f"이미지 크기: {width}x{height}")

        # 숫자 영역 감지
        crop_box = detect_digit_area(image_path)
        print(f"감지된 숫자 영역: {crop_box}")

        if crop_box:
            x, y, right, bottom = crop_box
            crop_width = right - x
            crop_height = bottom - y
            print(f"크롭 영역 크기: {crop_width}x{crop_height}")
            print(f"크롭 영역 비율: {crop_width/width:.2f} x {crop_height/height:.2f}")

            # 감지된 영역에 사각형 그리기
            cv2.rectangle(image, (x, y), (right, bottom), (0, 255, 0), 3)

            # 결과 이미지 저장
            output_path = image_path.replace('.jpg', '_detected.jpg')
            cv2.imwrite(output_path, image)
            print(f"감지 결과 이미지가 저장되었습니다: {output_path}")

            # 크롭된 이미지 저장
            cropped = image[y:bottom, x:right]
            crop_output_path = image_path.replace('.jpg', '_cropped.jpg')
            cv2.imwrite(crop_output_path, cropped)
            print(f"크롭된 이미지가 저장되었습니다: {crop_output_path}")

        return crop_box

    except Exception as e:
        print(f"테스트 중 오류 발생: {e}")
        return None


if __name__ == "__main__":
    # 테스트할 이미지 경로들
    test_images = [
        "www/tmp/gas/gas_latest.jpg",
        # 다른 테스트 이미지들도 추가 가능
    ]

    for image_path in test_images:
        print("\n" + "="*50)
        print(f"테스트: {image_path}")
        print("="*50)

        result = test_gas_meter_detection(image_path)

        if result:
            print("✅ 감지 성공")
        else:
            print("❌ 감지 실패")

        print("="*50)
