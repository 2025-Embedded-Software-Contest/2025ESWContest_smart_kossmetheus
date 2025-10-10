import os
from PIL import Image, ImageOps

# 일부 환경에서는 Pillow 부가 모듈이 누락될 수 있으므로 예외 처리 후 선택적으로 사용한다.
try:
    from PIL import ImageEnhance, ImageFilter
except (ImportError, AttributeError):
    ImageEnhance = None
    ImageFilter = None


@service
def gas_ocr_prepare(
    input_image: str = None,
    crop_output: str = "/config/www/tmp/gas/gas_latest-crop.jpg",
    resize_output: str = "/config/www/tmp/gas/gas_latest-crop-resize.jpg",
    int_output: str = "/config/www/tmp/gas/gas_latest-crop-resize1.jpg",
    frac_output: str = "/config/www/tmp/gas/gas_latest-crop-resize2.jpg",
    # 추가: 향상 처리(고대비/선명) 버전도 생성
    int_output_alt: str = "/config/www/tmp/gas/gas_latest-crop-resize1_hc.jpg",
    frac_output_alt: str = "/config/www/tmp/gas/gas_latest-crop-resize2_hc.jpg",
    # geometry defaults tuned for DS G1.6L sample (1600x1200 snapshot)
    rotation_angle_before: float = 0.0,
    # 새 기본값: success 예시에 맞춘 좌표(좌:420, 우:1220, 상:720, 하:880)
    crop_left: int = 420,
    crop_top: int = 720,
    crop_right: int = 1220,
    crop_bottom: int = 880,
    resize_width: int = 300,
    # split boundaries on resized image
    # 리사이즈 폭 300 기준 정수부 3자리 영역
    split_int_left: int = 10,
    split_int_right: int = 155,
    split_top: int = 0,
    split_bottom: int = 70,
    # 소수부 4자리 영역
    split_frac_left: int = 156,
    split_frac_right: int = 300,
    # 자동 분할 사용 (7자리 숫자 가정: 앞 3자리 정수, 뒤 4자리 소수)
    auto_split: bool = True,
    split_margin: int = 0,
    autocontrast: bool = True,
    denoise_median_size: int = 0,
    to_grayscale: bool = False,
    generate_alt: bool = True,
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
        if denoise_median_size and denoise_median_size >= 3:
            try:
                resized = resized.filter(ImageFilter.MedianFilter(size=denoise_median_size))
            except Exception as _:
                pass
        if to_grayscale:
            resized = resized.convert("L")

        _ensure_dir(resize_output)
        resized.save(resize_output)

        # Validate split bottom within height
        h = resized.height
        bottom = split_bottom if (split_bottom and split_bottom > 0 and split_bottom <= h) else h
        top = split_top if (split_top and split_top >= 0) else 0

        # 자동 분할: 세로 투영 최소치를 이용해 7자리 각 칸 경계 추정
        if auto_split:
            try:
                bnds = _auto_digit_splits(resized, top, bottom, expected_digits=7)
                # 3자리 정수 / 4자리 소수 경계
                x0, x3, x7 = 0, bnds[3], resized.width
                if split_margin:
                    x0 = max(0, x0 + split_margin)
                    x3 = max(0, x3 - split_margin)
                    x7 = min(resized.width, x7 - split_margin)
                split_int_left, split_int_right = x0, x3
                split_frac_left, split_frac_right = x3, x7
                log.info(
                    f"auto_split: bounds={bnds}, int=({split_int_left},{split_int_right}), frac=({split_frac_left},{split_frac_right})"
                )
            except Exception as exc:  # noqa: BLE001
                log.warning(f"auto_split 실패, 수동 분할로 진행: {exc}")

        # Integer part crop
        int_img = resized.crop((split_int_left, top, split_int_right, bottom))
        _ensure_dir(int_output)
        int_img.save(int_output)

        # Fractional part crop
        frac_img = resized.crop((split_frac_left, top, split_frac_right, bottom))
        _ensure_dir(frac_output)
        frac_img.save(frac_output)

        # 고대비/선명 버전 생성(선택)
        if generate_alt:
            if not (ImageEnhance and ImageFilter):
                log.warning(
                    "gas_ocr_prepare: Pillow ImageEnhance/ImageFilter 미존재로 기본 이미지를 복제해 *_hc.jpg 를 생성합니다"
                )
                _ensure_dir(int_output_alt)
                int_img.save(int_output_alt)
                _ensure_dir(frac_output_alt)
                frac_img.save(frac_output_alt)
            else:
                enh = resized
                # 밝기/대비/선명도 조정 후 약한 샤프닝
                enh = ImageEnhance.Brightness(enh).enhance(1.15)
                enh = ImageEnhance.Contrast(enh).enhance(1.8)
                enh = ImageEnhance.Sharpness(enh).enhance(1.6)
                enh = enh.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))

                int_alt = enh.crop((split_int_left, top, split_int_right, bottom))
                _ensure_dir(int_output_alt)
                int_alt.save(int_output_alt)

                frac_alt = enh.crop((split_frac_left, top, split_frac_right, bottom))
                _ensure_dir(frac_output_alt)
                frac_alt.save(frac_output_alt)

    except Exception as e:
        log.error(f"gas_ocr_prepare error: {e}")
        _save_placeholder(
            [
                crop_output,
                resize_output,
                int_output,
                frac_output,
                int_output_alt,
                frac_output_alt,
            ]
        )


def _ensure_dir(path: str):
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)


def _save_placeholder(paths: list[str]):
    """Ensure downstream automation has files even on failure."""
    try:
        placeholder = Image.new("RGB", (10, 10), color=(0, 0, 0))
    except Exception as exc:  # pragma: no cover - Pillow unavailable
        log.error(f"gas_ocr_prepare: placeholder image 생성 실패: {exc}")
        return

    for path in filter(None, paths):
        try:
            _ensure_dir(path)
            placeholder.save(path)
        except Exception as exc:
            log.error(f"gas_ocr_prepare: placeholder 저장 실패 ({path}): {exc}")


def _auto_digit_splits(img: Image.Image, top: int, bottom: int, expected_digits: int = 7):
    """세로 투영을 이용해 expected_digits 자리의 경계 x 좌표들을 반환.
    반환값: 경계 리스트 길이 expected_digits+1 (0 포함, width 포함)
    """
    from statistics import mean

    gray = img.convert("L")
    w, h = gray.width, gray.height
    top = max(0, min(top, h - 1))
    bottom = max(top + 1, min(bottom, h))

    # 세로 투영(밝기 반전 합) 계산
    proj = []
    crop_height = bottom - top
    px = gray.load()
    for x in range(w):
        s = 0
        for y in range(top, bottom):
            s += 255 - px[x, y]
        proj.append(s / crop_height)

    # 이동 평균으로 평활화
    window = max(3, int(w * 0.01))
    sm = []
    acc = 0
    for i, v in enumerate(proj):
        acc += v
        if i >= window:
            acc -= proj[i - window]
        sm.append(acc / min(i + 1, window))

    # 각 자리 사이 경계를 대략 w/expected_digits 간격으로 탐색, 로컬 최소값 선택
    approx = w / expected_digits
    radius = max(3, int(approx * 0.25))
    cuts = [0]
    for k in range(1, expected_digits):
        center = int(round(k * approx))
        left = max(1, center - radius)
        right = min(w - 2, center + radius)
        # 최소값 위치
        local = min(range(left, right + 1), key=lambda x: sm[x])
        cuts.append(local)
    cuts.append(w)

    # 단조 증가 보정
    for i in range(1, len(cuts)):
        if cuts[i] <= cuts[i - 1]:
            cuts[i] = min(w, cuts[i - 1] + 1)

    return cuts
