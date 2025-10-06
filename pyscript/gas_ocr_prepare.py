import os
from PIL import Image, ImageOps


@service
def gas_ocr_prepare(
    input_image: str = None,
    crop_output: str = "/config/www/tmp/gas/gas_latest-crop.jpg",
    resize_output: str = "/config/www/tmp/gas/gas_latest-crop-resize.jpg",
    int_output: str = "/config/www/tmp/gas/gas_latest-crop-resize1.jpg",
    frac_output: str = "/config/www/tmp/gas/gas_latest-crop-resize2.jpg",
    # geometry defaults tuned for DS G1.6L sample (1600x1200 snapshot)
    rotation_angle_before: float = 0.0,
    crop_left: int = 280,
    crop_top: int = 700,
    crop_right: int = 920,
    crop_bottom: int = 860,
    resize_width: int = 300,
    # split boundaries on resized image
    split_int_left: int = 5,
    split_int_right: int = 140,
    split_top: int = 0,
    split_bottom: int = 70,
    split_frac_left: int = 141,
    split_frac_right: int = 300,
    autocontrast: bool = True,
):
    """yaml
name: gas_ocr_prepare
description: Crop/resize/split gas meter image for OCR using pyscript.
fields:
  input_image:
    description: Source snapshot path
    example: /config/www/tmp/gas/gas_latest.jpg
    required: true
    selector:
      text:
  crop_output:
    description: Output path for cropped digits area
    example: /config/www/tmp/gas/gas_latest-crop.jpg
    required: true
    selector:
      text:
  resize_output:
    description: Output path for resized image (kept aspect ratio)
    example: /config/www/tmp/gas/gas_latest-crop-resize.jpg
    required: true
    selector:
      text:
  int_output:
    description: Output path for integer part crop
    example: /config/www/tmp/gas/gas_latest-crop-resize1.jpg
    required: true
    selector:
      text:
  frac_output:
    description: Output path for fractional part crop
    example: /config/www/tmp/gas/gas_latest-crop-resize2.jpg
    required: true
    selector:
      text:
  rotation_angle_before:
    description: Optional rotation (degrees) before cropping
    example: 0
    selector:
      number:
        min: -360
        max: 360
        step: 0.1
        mode: box
  crop_left:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  crop_top:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  crop_right:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  crop_bottom:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  resize_width:
    description: Resize width (height auto-preserved)
    example: 300
    selector:
      number:
        min: 50
        max: 1000
        step: 10
        mode: slider
  split_int_left:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  split_int_right:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  split_top:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  split_bottom:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  split_frac_left:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  split_frac_right:
    selector:
      number:
        min: 0
        step: 1
        mode: box
  autocontrast:
    description: Apply auto-contrast on resized image
    example: true
    selector:
      boolean:
"""
    log.info(
        f"gas_ocr_prepare: input={input_image}, crop=({crop_left},{crop_top},{crop_right},{crop_bottom}), "
        f"resize_w={resize_width}, split int=({split_int_left}-{split_int_right}), frac=({split_frac_left}-{split_frac_right})"
    )

    try:
        img = Image.open(input_image)

        if rotation_angle_before and rotation_angle_before != 0:
            img = img.rotate(rotation_angle_before, expand=True)

        # Crop full digits band
        crop = img.crop((crop_left, crop_top, crop_right, crop_bottom))
        _ensure_dir(crop_output)
        crop.save(crop_output)

        # Resize, keep aspect ratio
        if resize_width and resize_width > 0:
            w = resize_width
            h = int(crop.height * w / crop.width)
            resized = crop.resize((w, h))
        else:
            resized = crop

        if autocontrast:
            resized = ImageOps.autocontrast(resized)

        _ensure_dir(resize_output)
        resized.save(resize_output)

        # Validate split bottom within height
        h = resized.height
        bottom = split_bottom if (split_bottom and split_bottom > 0 and split_bottom <= h) else h
        top = split_top if (split_top and split_top >= 0) else 0

        # Integer part crop
        int_img = resized.crop((split_int_left, top, split_int_right, bottom))
        _ensure_dir(int_output)
        int_img.save(int_output)

        # Fractional part crop
        frac_img = resized.crop((split_frac_left, top, split_frac_right, bottom))
        _ensure_dir(frac_output)
        frac_img.save(frac_output)

    except Exception as e:
        log.error(f"gas_ocr_prepare error: {e}")


def _ensure_dir(path: str):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

