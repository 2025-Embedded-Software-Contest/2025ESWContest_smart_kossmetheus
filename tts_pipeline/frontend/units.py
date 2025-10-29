from __future__ import annotations

import re
from typing import Optional

from .numbers import (
    DIGITS_KO,
    read_digits_ko,
    read_number_speech,
    read_price_basic,
    sino_under_10000,
)

ALPHABET_TO_HANGUL = {
    "A": "에이",
    "B": "비",
    "C": "씨",
    "D": "디",
    "E": "이",
    "F": "에프",
    "G": "지",
    "H": "에이치",
    "I": "아이",
    "J": "제이",
    "K": "케이",
    "L": "엘",
    "M": "엠",
    "N": "엔",
    "O": "오",
    "P": "피",
    "Q": "큐",
    "R": "알",
    "S": "에스",
    "T": "티",
    "U": "유",
    "V": "브이",
    "W": "더블유",
    "X": "엑스",
    "Y": "와이",
    "Z": "지",
}

SYMBOL_TO_HANGUL = {
    "/": "슬래시",
    "-": "대시",
    "_": "언더바",
    "·": "닷",
    "µ": "마이크로",
    "μ": "마이크로",
    "Ω": "오옴",
    "‰": "퍼밀",
}

UNIT_READINGS = {
    "a": "암페어",
    "ah": "암페어시",
    "amp": "암프",
    "bps": "비피에스",
    "db": "데시벨",
    "fps": "에프피에스",
    "gbps": "지비피에스",
    "g": "그램",
    "ghz": "기가헤르츠",
    "hz": "헤르츠",
    "kcal": "킬로칼로리",
    "kg": "킬로그램",
    "khz": "킬로헤르츠",
    "km": "킬로미터",
    "kva": "킬로볼트암페어",
    "kw": "킬로와트",
    "kwh": "킬로와트시",
    "l": "리터",
    "lb": "파운드",
    "lbs": "파운드",
    "mah": "밀리암페어시",
    "ma": "밀리암페어",
    "mb": "메가바이트",
    "mbps": "엠비피에스",
    "mg": "밀리그램",
    "mhz": "메가헤르츠",
    "min": "분",
    "ml": "밀리리터",
    "mm": "밀리미터",
    "mph": "엠피에이치",
    "ms": "밀리초",
    "mwh": "메가와트시",
    "nm": "나노미터",
    "pb": "페타바이트",
    "pa": "파스칼",
    "kpa": "킬로파스칼",
    "rpm": "알피엠",
    "s": "초",
    "sec": "초",
    "t": "톤",
    "va": "볼트암페어",
    "v": "볼트",
    "w": "와트",
    "wh": "와트시",
    "psi": "피에스아이",
    "b": "바이트",
    "byte": "바이트",
    "bytes": "바이트",
    "kb": "킬로바이트",
    "kbyte": "킬로바이트",
    "mbit": "메가비트",
    "kbit": "킬로비트",
    "gbit": "기가비트",
    "tbit": "테라비트",
    "gb": "기가바이트",
    "tb": "테라바이트",
    "eb": "엑사바이트",
    "zb": "제타바이트",
    "yb": "요타바이트",
    "cm": "센티미터",
    "cm2": "제곱센티미터",
    "cm3": "세제곱센티미터",
    "m2": "제곱미터",
    "m3": "세제곱미터",
    "kmh": "킬로미터 퍼 시간",
    "fps2": "에프피에스 제곱",
    "n": "뉴턴",
    "kn": "킬로뉴턴",
    "mn": "메가뉴턴",
    "gpa": "기가파스칼",
    "mpa": "메가파스칼",
    "lbf": "파운드포스",
    "ppm": "피피엠",
    "ppb": "피피비",
    "ppt": "피피티",
}

UNIT_VALUE_PATTERN = re.compile(
    r"(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>[A-Za-zµμΩ‰²³⁴⁵⁶⁷⁸⁹/+-]{1,8})"
)

TEMP_C_SYMBOL = re.compile(r"(\d+(?:\.\d+)?)\s*℃")
TEMP_F_SYMBOL = re.compile(r"(\d+(?:\.\d+)?)\s*℉")
TEMP_C_LATIN = re.compile(r"(\d+(?:\.\d+)?)\s*(?:°\s*)?c(?=$|[^A-Za-z])", re.IGNORECASE)
TEMP_F_LATIN = re.compile(r"(\d+(?:\.\d+)?)\s*(?:°\s*)?f(?=$|[^A-Za-z])", re.IGNORECASE)
TIME_COLON_PAT = re.compile(r"(\d{1,2})\s*:\s*(\d{2})(?=\D|$)")

HOUR_NATIVE = {
    0: "영 시",
    1: "한 시",
    2: "두 시",
    3: "세 시",
    4: "네 시",
    5: "다섯 시",
    6: "여섯 시",
    7: "일곱 시",
    8: "여덟 시",
    9: "아홉 시",
    10: "열 시",
    11: "열한 시",
    12: "열두 시",
}


def _normalize_unit_key(unit: str) -> str:
    return (
        unit.replace("-", "")
        .replace("_", "")
        .replace(".", "")
        .replace("/", "")
        .lower()
    )


def _spell_out_unit(unit: str) -> str:
    parts: list[str] = []
    for ch in unit:
        if ch.isalpha():
            parts.append(ALPHABET_TO_HANGUL.get(ch.upper(), ch))
        elif ch.isdigit():
            parts.append(DIGITS_KO.get(ch, ch))
        else:
            label = SYMBOL_TO_HANGUL.get(ch)
            if label:
                parts.append(label)
    return " ".join(parts).strip()


def read_unit_text(unit: str) -> Optional[str]:
    key = _normalize_unit_key(unit)
    if key in UNIT_READINGS:
        return UNIT_READINGS[key]
    if key.endswith("s") and key[:-1] in UNIT_READINGS:
        return UNIT_READINGS[key[:-1]]
    if any(c.isupper() for c in unit) or any(c in "/+-" for c in unit):
        spelled = _spell_out_unit(unit)
        return spelled or None
    return None


def expand_units(text: str) -> str:
    def _repl(match: re.Match[str]) -> str:
        value_raw = match.group("value")
        unit_raw = match.group("unit")
        unit_text = read_unit_text(unit_raw)
        if not unit_text:
            return match.group(0)
        value_clean = value_raw.replace(",", "")
        try:
            number_text = read_number_speech(value_clean)
        except Exception:
            return match.group(0)
        return f"{number_text} {unit_text}"

    return UNIT_VALUE_PATTERN.sub(_repl, text)


def _ko_hour(n: int) -> str:
    if n in HOUR_NATIVE:
        return HOUR_NATIVE[n]
    return f"{sino_under_10000(n)} 시"


def _ko_min(n: int) -> str:
    return f"{sino_under_10000(n) or '영'} 분"


def autopatch_time_ko(text: str) -> str:
    def _colon_repl(match: re.Match[str]) -> str:
        hour = int(match.group(1))
        minute = int(match.group(2))
        return f"{_ko_hour(hour)} {_ko_min(minute)}"

    t = TIME_COLON_PAT.sub(_colon_repl, text)
    t = re.sub(r"(\d{1,2})\s*시(?=\D|$)", lambda m: _ko_hour(int(m.group(1))), t)
    t = re.sub(r"(\d{1,2})\s*분(?=\D|$)", lambda m: _ko_min(int(m.group(1))), t)
    return t


def _format_temperature(value: str, unit_label: str) -> str:
    return f"{unit_label} {read_number_speech(value)} 도"


def autopatch_temperature(text: str) -> str:
    t = TEMP_C_SYMBOL.sub(lambda m: _format_temperature(m.group(1), "섭씨"), text)
    t = TEMP_F_SYMBOL.sub(lambda m: _format_temperature(m.group(1), "화씨"), t)
    t = TEMP_C_LATIN.sub(lambda m: _format_temperature(m.group(1), "섭씨"), t)
    t = TEMP_F_LATIN.sub(lambda m: _format_temperature(m.group(1), "화씨"), t)
    return t


__all__ = [
    "UNIT_VALUE_PATTERN",
    "read_unit_text",
    "expand_units",
    "autopatch_time_ko",
    "autopatch_temperature",
]
