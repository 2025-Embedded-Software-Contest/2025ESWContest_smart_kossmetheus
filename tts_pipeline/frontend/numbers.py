from __future__ import annotations

from typing import Optional

try:
    from num2words import num2words

    NUM2WORDS_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    NUM2WORDS_AVAILABLE = False


DIGITS_KO = {
    "0": "공",
    "1": "일",
    "2": "이",
    "3": "삼",
    "4": "사",
    "5": "오",
    "6": "육",
    "7": "칠",
    "8": "팔",
    "9": "구",
}

DECIMAL_DIGITS_KO = dict(DIGITS_KO)
DECIMAL_DIGITS_KO["0"] = "영"

UNITS = [(10000, "만"), (1000, "천"), (100, "백"), (10, "십")]
NUM_SINO = {
    0: "영",
    1: "일",
    2: "이",
    3: "삼",
    4: "사",
    5: "오",
    6: "육",
    7: "칠",
    8: "팔",
    9: "구",
}


def read_digits_ko(s: str, sep: str = " ") -> str:
    digits = [DIGITS_KO.get(ch, ch) for ch in s if ch.isdigit()]
    return sep.join(digits)


def read_decimal_digits_ko(s: str, sep: str = " ") -> str:
    digits = [DECIMAL_DIGITS_KO.get(ch, ch) for ch in s if ch.isdigit()]
    return sep.join(digits)


def sino_under_10000(n: int) -> str:
    if n == 0:
        return ""
    out: list[str] = []
    for val, name in UNITS[1:]:
        d = n // val
        if d:
            out.append(("" if d == 1 else NUM_SINO[d]) + name)
            n %= val
    if n:
        out.append(NUM_SINO[n])
    return " ".join(out).strip()


def read_price_basic(n: int) -> str:
    if n == 0:
        return "영"
    man, rest = divmod(n, 10000)
    parts: list[str] = []
    if man:
        parts.append(sino_under_10000(man) + "만")
    if rest:
        parts.append(sino_under_10000(rest))
    return " ".join(p for p in parts if p)


def convert_number_korean(n: int) -> str:
    """숫자를 한국어로 변환 (하드코딩 우선 → num2words → 커스텀)"""
    if n in SINO_NUMBERS_0_100:
        return SINO_NUMBERS_0_100[n]

    if NUM2WORDS_AVAILABLE:
        try:
            return num2words(n, lang="ko")
        except Exception:
            pass

    if n >= 10000:
        return read_price_basic(n)
    return sino_under_10000(n) or "영"


SINO_NUMBERS_0_100 = {
    0: "영",
    1: "일",
    2: "이",
    3: "삼",
    4: "사",
    5: "오",
    6: "육",
    7: "칠",
    8: "팔",
    9: "구",
    10: "십",
    11: "십일",
    12: "십이",
    13: "십삼",
    14: "십사",
    15: "십오",
    16: "십육",
    17: "십칠",
    18: "십팔",
    19: "십구",
    20: "이십",
    21: "이십일",
    22: "이십이",
    23: "이십삼",
    24: "이십사",
    25: "이십오",
    26: "이십육",
    27: "이십칠",
    28: "이십팔",
    29: "이십구",
    30: "삼십",
    31: "삼십일",
    32: "삼십이",
    33: "삼십삼",
    34: "삼십사",
    35: "삼십오",
    36: "삼십육",
    37: "삼십칠",
    38: "삼십팔",
    39: "삼십구",
    40: "사십",
    41: "사십일",
    42: "사십이",
    43: "사십삼",
    44: "사십사",
    45: "사십오",
    46: "사십육",
    47: "사십칠",
    48: "사십팔",
    49: "사십구",
    50: "오십",
    51: "오십일",
    52: "오십이",
    53: "오십삼",
    54: "오십사",
    55: "오십오",
    56: "오십육",
    57: "오십칠",
    58: "오십팔",
    59: "오십구",
    60: "육십",
    61: "육십일",
    62: "육십이",
    63: "육십삼",
    64: "육십사",
    65: "육십오",
    66: "육십육",
    67: "육십칠",
    68: "육십팔",
    69: "육십구",
    70: "칠십",
    71: "칠십일",
    72: "칠십이",
    73: "칠십삼",
    74: "칠십사",
    75: "칠십오",
    76: "칠십육",
    77: "칠십칠",
    78: "칠십팔",
    79: "칠십구",
    80: "팔십",
    81: "팔십일",
    82: "팔십이",
    83: "팔십삼",
    84: "팔십사",
    85: "팔십오",
    86: "팔십육",
    87: "팔십칠",
    88: "팔십팔",
    89: "팔십구",
    90: "구십",
    91: "구십일",
    92: "구십이",
    93: "구십삼",
    94: "구십사",
    95: "구십오",
    96: "구십육",
    97: "구십칠",
    98: "구십팔",
    99: "구십구",
    100: "백",
}

NATIVE_NUMBERS = {
    1: "한",
    2: "두",
    3: "세",
    4: "네",
    5: "다섯",
    6: "여섯",
    7: "일곱",
    8: "여덟",
    9: "아홉",
    10: "열",
    20: "스물",
    30: "서른",
    40: "마흔",
    50: "쉰",
    60: "예순",
    70: "일흔",
    80: "여든",
    90: "아흔",
}

NATIVE_COUNTER_UNITS = {
    "개",
    "명",
    "살",
    "마리",
    "그루",
    "송이",
    "자루",
    "켤레",
    "벌",
    "채",
    "척",
    "대",
    "권",
    "장",
    "잔",
    "병",
    "포기",
}

SINO_COUNTER_UNITS = {
    "원",
    "달러",
    "엔",
    "위안",
    "유로",
    "파운드",
    "천",
    "만",
    "억",
    "조",
    "미터",
    "센티미터",
    "킬로미터",
    "그램",
    "킬로그램",
    "시간",
    "분",
    "초",
    "년",
    "월",
    "일",
    "퍼센트",
    "도",
    "층",
}


def native_korean_number(n: int) -> str:
    if n < 1 or n > 99:
        return str(n)
    if n in NATIVE_NUMBERS:
        return NATIVE_NUMBERS[n]
    tens = (n // 10) * 10
    ones = n % 10
    if ones == 0:
        return NATIVE_NUMBERS[tens]
    return NATIVE_NUMBERS[tens] + NATIVE_NUMBERS[ones]


def native_korean_counter(n: int, unit: str) -> str:
    if unit in SINO_COUNTER_UNITS:
        if n >= 10000:
            return f"{read_price_basic(n)} {unit}"
        return f"{sino_under_10000(n) or '영'} {unit}"

    if unit in NATIVE_COUNTER_UNITS:
        if n >= 100:
            if n >= 10000:
                return f"{read_price_basic(n)} {unit}"
            return f"{sino_under_10000(n)} {unit}"
        return f"{native_korean_number(n)} {unit}"

    if n >= 10000:
        return f"{read_price_basic(n)} {unit}"
    return f"{sino_under_10000(n) or '영'} {unit}"


def read_number_speech(s: str) -> str:
    if "." in s:
        a, b = s.split(".", 1)
        left_text = ""
        if a:
            left_value = int(a)
            if len(a) >= 4:
                left_text = read_digits_ko(a)
            else:
                left_text = sino_under_10000(left_value)
        if not left_text:
            left_text = "영"
        right_raw = b.rstrip("0") or "0"
        right_text = read_decimal_digits_ko(right_raw)
        return f"{left_text} 점 {right_text}"

    n = int(s)
    if n >= 10000:
        return read_price_basic(n)
    return sino_under_10000(n) or "영"


def minute_to_text(n: int) -> str:
    return sino_under_10000(n) or "영"

