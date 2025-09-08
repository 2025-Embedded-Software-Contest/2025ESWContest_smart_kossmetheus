import os
from PIL import Image

@service
def image_rotate(input_image=None, output_image=None, rotation_angle=0):
  """yaml
name: image_rotate
description: image_rotate service / pyscript.
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
"""
  """image_crop using pyscript."""
  log.info(f"image_crop: got input_image {input_image}, output_image {output_image}, rotation_angle {rotation_angle}")
  try:
    # Open the input image
    image = Image.open(input_image)

    # Rotate the image (90 degrees clockwise)
    if (rotation_angle > 0) :
      image = image.rotate(rotation_angle, expand=True)

    # 출력 이미지 폴더 경로
    output_folder = os.path.dirname(output_image)

    # 폴더가 있는지 확인하고 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the cropped image as a new JPEG file
    image.save(output_image)

  except Exception as e:
    log.info("Error: ", e)
