from __future__ import annotations

import re
from typing import Match

from .numbers import (
    read_decimal_digits_ko,
    read_digits_ko,
    read_number_speech,
    read_price_basic,
    sino_under_10000,
)

PHONE_PAT = re.compile(r"(0\d{1,2})-(\d{3,4})-(\d{4})(?=\D|$)")
DIGIT_SEQ_PAT = re.compile(r"\b\d{7,}\b")
PERCENT_PAT = re.compile(r"(\d+(?:\.\d+)?)\s*%(?=\D|$)")
DATE_SLASH_PAT = re.compile(r"(1[0-2]|0?[1-9])/(3[01]|[12][0-9]|0?[1-9])")
MONTH_NUM_PAT = re.compile(r"(1[0-2]|0?[1-9])월")
RANGE_TILDE_PAT = re.compile(
    r"(\d+(?:\.\d+)?)\s*~\s*(\d+(?:\.\d+)?)(\s*(?:도|℃|℉|°C|°F|°|%|퍼센트|kg|㎏|g|㎎|mg|mm|㎜|cm|㎝|m|km|시간|분|초))?"
)
GENERAL_TILDE_PAT = re.compile(r"([^\s~]+)\s*~\s*([^\s~]+)")
FRACTION_PAT = re.compile(r"(\d+)\s*/\s*(\d+)")
DECIMAL_PAT = re.compile(r"(\d+\.\d+)(?=\D|$)")
WON_DECIMAL_PAT = re.compile(r"([\d,]+)\.(\d+)\s*원(?=\D|$)")
WON_PAT = re.compile(r"([\d,]+)\s*원(?=\D|$)")


def _month_text(value: int) -> str:
    if value == 10:
        return "시"
    if value == 6:
        return "유"
    return sino_under_10000(value).replace(" ", "")


def format_phone(match: Match[str]) -> str:
    groups = [read_digits_ko(part, sep="") for part in match.groups()]
    return ", ".join(groups)


def format_range_tilde(start: str, end: str, unit: str) -> str:
    start_text = read_number_speech(start)
    end_text = read_number_speech(end)

    if "." not in start:
        start_text = start_text.replace(" ", "")
    if "." not in end:
        end_text = end_text.replace(" ", "")

    suffix_raw = (unit or "").strip()
    if not suffix_raw:
        suffix = ""
    elif suffix_raw in {"도", "℃", "℉", "°C", "°F", "°"}:
        suffix = suffix_raw
    elif suffix_raw in {"%", "퍼센트"}:
        suffix = " 퍼센트"
    else:
        suffix = " " + suffix_raw
    return f"{start_text}에서 {end_text}{suffix}"


def format_general_tilde(match: Match[str]) -> str:
    left = match.group(1)
    right = match.group(2)

    if not left or not right:
        return match.group(0)

    punctuation = ""
    while right and right[-1] in ",.!?)]":
        punctuation = right[-1] + punctuation
        right = right[:-1]

    suffix_word = ""
    for candidate in ("까지", "부터", "에서", "에"):
        if right.endswith(candidate):
            suffix_word = candidate
            right = right[: -len(candidate)]
            break

    if not right:
        return match.group(0)

    return f"{left}에서 {right}{suffix_word}{punctuation}"


def format_fraction(numerator: str, denominator: str) -> str:
    denom_val = int(denominator)
    if denom_val > 16:
        return f"{numerator}/{denominator}"

    numerator_text = read_number_speech(numerator)
    denominator_text = read_number_speech(denominator)
    return f"{denominator_text} 분의 {numerator_text}"


def format_won_decimal(int_part: str, frac_part: str) -> str:
    integer_value = int(int_part.replace(",", ""))
    integer_text = read_price_basic(integer_value)

    frac_clean = frac_part.rstrip("0")
    if not frac_clean:
        return f"{integer_text} 원"

    frac_text = read_decimal_digits_ko(frac_clean)
    return f"{integer_text} 점 {frac_text} 원"


def format_date_slash(match: Match[str]) -> str:
    month, day = match.group(1), match.group(2)
    start = match.start()
    end = match.end()

    context_before = match.string[max(0, start - 30) : start]
    context_after = match.string[end : end + 30]

    month_val = int(month)
    day_val = int(day)

    if month_val > 12 or day_val > 31:
        return match.group(0)

    fraction_cues = (
        "분수",
        "비율",
        "확률",
        "배",
        "중",
        "fraction",
        "ratio",
        "문제",
        "정답",
        "오답",
        "정답률",
        "승률",
        "타율",
        "점유율",
        "달성률",
        "몇",
        "개중",
        "개 중",
    )
    if any(cue in context_before for cue in fraction_cues) or any(
        cue in context_after for cue in fraction_cues
    ):
        return match.group(0)

    date_before_cues = (
        "월",
        "요일",
        "날짜",
        "행사",
        "기념",
        "스케줄",
        "일정",
        "예약",
        "주",
        "마감",
        "기한",
        "출발",
        "도착",
        "회의",
        "미팅",
        "시험",
        "발표",
        "세미나",
        "워크숍",
        "컨퍼런스",
        "공연",
        "전시",
        "축제",
        "파티",
        "모임",
        "약속",
        "내일",
        "어제",
        "오늘",
        "다음주",
        "지난주",
        "이번주",
        "다음달",
        "지난달",
        "이번달",
        "내년",
        "작년",
        "올해",
        "생일",
        "기념일",
        "공휴일",
        "휴일",
        "방학",
        "개강",
        "종강",
        "여행",
        "휴가",
        "출장",
        "귀국",
        "입국",
        "출국",
    )

    date_after_cues = (
        "일",
        "에",
        "까지",
        "부터",
        "입니다",
        "예정",
        "열",
        "진행",
        "날",
        "쯤",
        "경",
        "즈음",
        "무렵",
        "이에요",
        "이었",
        "였",
        "당일",
        "당시",
    )

    has_date_before = any(cue in context_before for cue in date_before_cues)
    has_date_after = any(cue in context_after for cue in date_after_cues)

    if day_val <= 12:
        if not (has_date_before and has_date_after):
            return match.group(0)
    else:
        if not (has_date_before or has_date_after):
            return match.group(0)

    month_text = _month_text(month_val)
    day_text = sino_under_10000(day_val)
    return f"{month_text}월 {day_text}일"


def format_month_numeric(match: Match[str]) -> str:
    value = int(match.group(1))
    return f"{_month_text(value)}월"


__all__ = [
    "PHONE_PAT",
    "DIGIT_SEQ_PAT",
    "PERCENT_PAT",
    "DATE_SLASH_PAT",
    "MONTH_NUM_PAT",
    "RANGE_TILDE_PAT",
    "GENERAL_TILDE_PAT",
    "FRACTION_PAT",
    "DECIMAL_PAT",
    "WON_DECIMAL_PAT",
    "WON_PAT",
    "format_phone",
    "format_range_tilde",
    "format_general_tilde",
    "format_fraction",
    "format_won_decimal",
    "format_date_slash",
    "format_month_numeric",
]
