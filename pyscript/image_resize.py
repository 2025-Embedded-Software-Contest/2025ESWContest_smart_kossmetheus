import os
from PIL import Image

@service
def image_resize(input_image=None, output_image=None, width=0, height=0):
  """yaml
name: image_resize
description: image_resize service / pyscript.
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
  width:
    description: resize witdh
    example: 100
    required: true
    selector:
      number:
        min: 0
        step: 1
        mode: box
  height:
    description: resize height
    example: 100
    required: true
    selector:
      number:
        min: 0
        step: 1
        mode: box
"""
  """image_resize using pyscript."""
  log.info(f"image_resize: got input_image {input_image}, output_image {output_image}, width {width}, height {height}")
  try:
    # Open the input image
    image = Image.open(input_image)

    # resize image
    if width > 0 and height == 0:
      original_width, original_height = image.size
      height = int((original_height * width) / original_width)
    elif  width == 0 and height > 0 :
      original_width, original_height = image.size
      width = int((original_width * height) / original_height)

    image = image.resize((width,height))

    # 출력 이미지 폴더 경로
    output_folder = os.path.dirname(output_image)

    # 폴더가 있는지 확인하고 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the cropped image as a new JPEG file
    image.save(output_image)

  except Exception as e:
    log.info("Error: ", e)
