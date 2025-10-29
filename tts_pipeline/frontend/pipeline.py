from __future__ import annotations

import re
from typing import Optional

from .english import convert_english_to_korean, english_to_korean_auto
from .morph import KIWI_AVAILABLE, get_kiwi
from .numbers import (
    convert_number_korean,
    native_korean_counter,
    read_digits_ko,
    read_number_speech,
    read_price_basic,
)
from .patterns import (
    DATE_SLASH_PAT,
    DECIMAL_PAT,
    DIGIT_SEQ_PAT,
    FRACTION_PAT,
    GENERAL_TILDE_PAT,
    MONTH_NUM_PAT,
    PERCENT_PAT,
    PHONE_PAT,
    RANGE_TILDE_PAT,
    WON_DECIMAL_PAT,
    WON_PAT,
    format_date_slash,
    format_fraction,
    format_general_tilde,
    format_month_numeric,
    format_phone,
    format_range_tilde,
    format_won_decimal,
)
from .units import autopatch_temperature, autopatch_time_ko, expand_units, read_unit_text

try:
    from g2pk import G2p  # type: ignore

    _g2pk_instance: Optional[G2p] = None
    G2PK_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    G2PK_AVAILABLE = False
    _g2pk_instance = None

try:
    from kss import split_sentences  # type: ignore

    KSS_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    KSS_AVAILABLE = False


ELLIPSIS_PATTERN = re.compile(r"\.{3,}")
PROSODY_MARKERS = {
    "!": " ! ",
    "?": " ? ",
    "~": " ~ ",
    "…": " … ",
}
SAFE_QUOTATION_MARKS = {'"', "'", "“", "”", "‘", "’"}
PUNCTUATION_TO_SPACE = set(",;:@#$%^&*_+=`|\\/")


def get_g2pk() -> G2p:
    if not G2PK_AVAILABLE:
        raise RuntimeError("g2pK is not installed")
    global _g2pk_instance
    if _g2pk_instance is None:  # pragma: no branch - simple cache
        _g2pk_instance = G2p()
    return _g2pk_instance


def apply_g2pk_safe(text: str) -> str:
    if not G2PK_AVAILABLE:
        return text
    try:
        return get_g2pk()(text)
    except Exception:
        return text


def remove_punctuation(text: str) -> str:
    if not text:
        return text

    normalized = ELLIPSIS_PATTERN.sub(" … ", text)
    out: list[str] = []

    for idx, ch in enumerate(normalized):
        prev_char = normalized[idx - 1] if idx > 0 else ""
        next_char = normalized[idx + 1] if idx + 1 < len(normalized) else ""

        if ch in PROSODY_MARKERS:
            out.append(PROSODY_MARKERS[ch])
        elif ch in SAFE_QUOTATION_MARKS:
            out.append(ch)
        elif ch in PUNCTUATION_TO_SPACE:
            out.append(" ")
        elif ch == ".":
            if prev_char.isdigit() and next_char.isdigit():
                out.append(".")
            else:
                out.append(" ")
        elif ch == ",":
            if prev_char.isdigit() and next_char.isdigit():
                out.append(",")
            else:
                out.append(" ")
        elif ch in {";", ":"}:
            out.append(" ")
        else:
            out.append(ch)

    cleaned = "".join(out)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned


def autopatch_numbers(text: str) -> str:
    def _percent(match: re.Match[str]) -> str:
        return f"{read_number_speech(match.group(1))} 퍼센트"

    t = convert_english_to_korean(text)
    t = expand_units(t)
    t = PHONE_PAT.sub(format_phone, t)
    t = DATE_SLASH_PAT.sub(format_date_slash, t)
    t = RANGE_TILDE_PAT.sub(lambda m: format_range_tilde(m.group(1), m.group(2), m.group(3) or ""), t)
    t = GENERAL_TILDE_PAT.sub(format_general_tilde, t)
    t = MONTH_NUM_PAT.sub(format_month_numeric, t)
    t = FRACTION_PAT.sub(lambda m: format_fraction(m.group(1), m.group(2)), t)
    t = WON_DECIMAL_PAT.sub(lambda m: format_won_decimal(m.group(1), m.group(2)), t)
    t = PERCENT_PAT.sub(_percent, t)
    t = DECIMAL_PAT.sub(lambda m: read_number_speech(m.group(1)), t)
    t = WON_PAT.sub(lambda m: f"{read_price_basic(int(m.group(1).replace(',', '')))} 원", t)
    t = DIGIT_SEQ_PAT.sub(lambda m: read_digits_ko(m.group(0)), t)
    return t


def kiwi_enhanced_frontend(text: str) -> str:
    if not KIWI_AVAILABLE:
        return autopatch_numbers(text)

    preprocessed = autopatch_temperature(text)
    preprocessed = autopatch_time_ko(preprocessed)

    kiwi = get_kiwi()
    tokens = kiwi.tokenize(preprocessed)

    rebuilt: list[str] = []
    cursor = 0
    i = 0
    total = len(tokens)

    while i < total:
        token = tokens[i]
        if token.start < cursor:
            i += 1
            continue

        token_text = preprocessed[token.start : token.end]
        replacement: Optional[str] = None
        advance = 1

        if token.tag == "SL":
            hangul = english_to_korean_auto(token_text)
            if hangul != token_text:
                replacement = hangul

        elif token.tag == "SN":
            digit_clean = token_text.replace(",", "")
            next_token = tokens[i + 1] if i + 1 < total else None
            local_replacement: Optional[str] = None
            advance = 1

            if (
                next_token
                and next_token.tag == "NNB"
                and next_token.start >= token.end
                and digit_clean.isdigit()
            ):
                number_val = int(digit_clean)
                unit_text = preprocessed[next_token.start : next_token.end]
                local_replacement = native_korean_counter(number_val, unit_text)
                advance = 2

            elif next_token and next_token.tag == "SL" and next_token.start >= token.end:
                unit_candidate = preprocessed[next_token.start : next_token.end]
                unit_reading = read_unit_text(unit_candidate)
                if unit_reading:
                    try:
                        number_text = read_number_speech(digit_clean)
                    except Exception:
                        number_text = digit_clean
                    local_replacement = f"{number_text} {unit_reading}"
                    advance = 2

            if local_replacement is None and digit_clean.isdigit():
                number_val = int(digit_clean)
                if number_val >= 10000:
                    local_replacement = read_price_basic(number_val)
                elif number_val >= 100:
                    local_replacement = convert_number_korean(number_val)

            if local_replacement is not None:
                rebuilt.append(preprocessed[cursor : token.start])
                rebuilt.append(local_replacement)
                cursor = tokens[i + advance - 1].end
                i += advance
                continue
            else:
                rebuilt.append(preprocessed[cursor : token.start])
                rebuilt.append(token_text)
                cursor = token.end
                i += 1
                continue

        if replacement is not None:
            rebuilt.append(preprocessed[cursor : token.start])
            rebuilt.append(replacement)
            cursor = tokens[i + advance - 1].end

        i += advance

    rebuilt.append(preprocessed[cursor:])
    processed_text = "".join(rebuilt)
    processed_text = expand_units(processed_text)

    processed_text = PHONE_PAT.sub(format_phone, processed_text)
    processed_text = DATE_SLASH_PAT.sub(format_date_slash, processed_text)
    processed_text = RANGE_TILDE_PAT.sub(lambda m: format_range_tilde(m.group(1), m.group(2), m.group(3) or ""), processed_text)
    processed_text = GENERAL_TILDE_PAT.sub(format_general_tilde, processed_text)
    processed_text = MONTH_NUM_PAT.sub(format_month_numeric, processed_text)
    processed_text = FRACTION_PAT.sub(lambda m: format_fraction(m.group(1), m.group(2)), processed_text)
    processed_text = WON_DECIMAL_PAT.sub(lambda m: format_won_decimal(m.group(1), m.group(2)), processed_text)
    processed_text = PERCENT_PAT.sub(lambda m: f"{read_number_speech(m.group(1))} 퍼센트", processed_text)
    processed_text = DECIMAL_PAT.sub(lambda m: read_number_speech(m.group(1)), processed_text)
    processed_text = WON_PAT.sub(lambda m: f"{read_price_basic(int(m.group(1).replace(',', '')))} 원", processed_text)
    processed_text = DIGIT_SEQ_PAT.sub(lambda m: read_digits_ko(m.group(0)), processed_text)

    processed_text = re.sub(r"\s+", " ", processed_text).strip()
    return processed_text


def _process_single_sentence(text: str, use_g2pk: bool = False) -> str:
    if KIWI_AVAILABLE:
        text = kiwi_enhanced_frontend(text)
    else:
        text = autopatch_numbers(text)
        text = autopatch_temperature(text)
        text = autopatch_time_ko(text)

    if use_g2pk:
        text = apply_g2pk_safe(text)
    return text


def ko_text_frontend(
    text: str,
    use_g2pk: bool = False,
    use_sentence_split: bool = False,
) -> str:
    text = remove_punctuation(text)

    if use_sentence_split and KSS_AVAILABLE:
        try:
            sentences = split_sentences(text)
        except Exception:
            sentences = [text]

        processed = [_process_single_sentence(sent, use_g2pk=use_g2pk) for sent in sentences]
        return " ".join(processed)

    return _process_single_sentence(text, use_g2pk=use_g2pk)


__all__ = [
    "apply_g2pk_safe",
    "autopatch_numbers",
    "kiwi_enhanced_frontend",
    "ko_text_frontend",
    "remove_punctuation",
]
