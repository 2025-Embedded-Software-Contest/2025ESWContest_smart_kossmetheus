from __future__ import annotations

import re
from typing import List

try:
    from g2p_en import G2p as G2pEN

    _g2p_en_instance: G2pEN | None = None
    G2P_EN_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    _g2p_en_instance = None
    G2P_EN_AVAILABLE = False


ENGLISH_TO_KOREAN = {
    # 일반 단어
    "happy": "해피",
    "okay": "오케이",
    "ok": "오케이",
    "thanks": "땡스",
    "thank you": "땡큐",
    "hello": "헬로",
    "hi": "하이",
    "bye": "바이",
    "please": "플리즈",
    "sorry": "쏘리",
    "yes": "예스",
    "no": "노",
    # 기술 용어
    "ai": "에이아이",
    "tts": "티티에스",
    "api": "에이피아이",
    "app": "앱",
    "web": "웹",
    "email": "이메일",
    "phone": "폰",
    "mobile": "모바일",
    "online": "온라인",
    "offline": "오프라인",
    "file": "파일",
    "data": "데이터",
    "server": "서버",
    "client": "클라이언트",
    "system": "시스템",
    "program": "프로그램",
    "software": "소프트웨어",
    "hardware": "하드웨어",
    # 브랜드/서비스
    "google": "구글",
    "apple": "애플",
    "iphone": "아이폰",
    "amazon": "아마존",
    "facebook": "페이스북",
    "youtube": "유튜브",
    "twitter": "트위터",
    "instagram": "인스타그램",
    "netflix": "넷플릭스",
    "github": "깃허브",
    "gitlab": "깃랩",
    # 일상 용어
    "coffee": "커피",
    "cafe": "카페",
    "restaurant": "레스토랑",
    "hotel": "호텔",
    "taxi": "택시",
    "bus": "버스",
    "train": "트레인",
    "metro": "메트로",
    "ticket": "티켓",
    "menu": "메뉴",
    "service": "서비스",
    "shopping": "쇼핑",
    "sale": "세일",
    "discount": "디스카운트",
    # 시간/날짜
    "am": "에이엠",
    "pm": "피엠",
    "monday": "먼데이",
    "tuesday": "튜즈데이",
    "wednesday": "웬즈데이",
    "thursday": "써스데이",
    "friday": "프라이데이",
    "saturday": "새터데이",
    "sunday": "선데이",
    # 추가 기술/IT 용어
    "computer": "컴퓨터",
    "internet": "인터넷",
    "smartphone": "스마트폰",
    "website": "웹사이트",
    "application": "애플리케이션",
    "database": "데이터베이스",
    "network": "네트워크",
    "cloud": "클라우드",
    "security": "시큐리티",
    "password": "패스워드",
    "login": "로그인",
    "logout": "로그아웃",
    "download": "다운로드",
    "upload": "업로드",
    "update": "업데이트",
    "backup": "백업",
    "battery": "배터리",
    "storage": "스토리지",
    # 비즈니스/업무 용어
    "meeting": "미팅",
    "schedule": "스케줄",
    "project": "프로젝트",
    "team": "팀",
    "manager": "매니저",
    "office": "오피스",
    "contract": "컨트랙트",
    "deadline": "데드라인",
    "report": "리포트",
    "presentation": "프레젠테이션",
    # 동작/상태 단어
    "start": "스타트",
    "stop": "스톱",
    "check": "체크",
    "test": "테스트",
    "cancel": "캔슬",
    "confirm": "컨펌",
    "send": "센드",
    "save": "세이브",
    "delete": "딜리트",
    "edit": "에디트",
    # 쇼핑/결제
    "cart": "카트",
    "payment": "페이먼트",
    "delivery": "딜리버리",
    "shipping": "쉬핑",
    "order": "오더",
    "coupon": "쿠폰",
    "point": "포인트",
    "membership": "멤버십",
    "card": "카드",
    "cash": "캐시",
    # 소셜/미디어
    "like": "라이크",
    "share": "쉐어",
    "comment": "코멘트",
    "follow": "팔로우",
    "message": "메시지",
    "post": "포스트",
    "video": "비디오",
    "photo": "포토",
    "live": "라이브",
    "streaming": "스트리밍",
    # 기타 자주 쓰는 단어
    "news": "뉴스",
    "game": "게임",
    "music": "뮤직",
    "movie": "무비",
    "book": "북",
    "link": "링크",
    "page": "페이지",
    "list": "리스트",
    "home": "홈",
    "menu": "메뉴",
}


ARPABET_TO_HANGUL = {
    # 모음
    "AA": "아",
    "AE": "애",
    "AH": "어",
    "AO": "오",
    "AW": "아우",
    "AY": "아이",
    "EH": "에",
    "ER": "어",
    "EY": "에이",
    "IH": "이",
    "IY": "이",
    "OW": "오",
    "OY": "오이",
    "UH": "우",
    "UW": "우",
    # 자음 (초성)
    "B": "ㅂ",
    "CH": "ㅊ",
    "D": "ㄷ",
    "DH": "ㄷ",
    "F": "ㅍ",
    "G": "ㄱ",
    "HH": "ㅎ",
    "JH": "ㅈ",
    "K": "ㅋ",
    "L": "ㄹ",
    "M": "ㅁ",
    "N": "ㄴ",
    "NG": "ㅇ",
    "P": "ㅍ",
    "R": "ㄹ",
    "S": "ㅅ",
    "SH": "ㅅ",
    "T": "ㅌ",
    "TH": "ㅅ",
    "V": "ㅂ",
    "W": "ㅜ",
    "Y": "ㅣ",
    "Z": "ㅈ",
    "ZH": "ㅈ",
}


def get_g2p_en() -> G2pEN | None:
    global _g2p_en_instance
    if not G2P_EN_AVAILABLE:
        return None
    if _g2p_en_instance is None:
        _g2p_en_instance = G2pEN()
    return _g2p_en_instance


def arpabet_to_hangul(arpabet_seq: List[str]) -> str:
    result: list[str] = []
    syllable_parts: list[str] = []

    for phone in arpabet_seq:
        phone_clean = "".join(c for c in phone if not c.isdigit())
        hangul = ARPABET_TO_HANGUL.get(phone_clean)
        if hangul is None:
            continue
        syllable_parts.append(hangul)
        if phone_clean in {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}:
            result.append("".join(syllable_parts))
            syllable_parts = []

    if syllable_parts:
        result.append("".join(syllable_parts))

    return "".join(result)


def english_to_korean_auto(word: str) -> str:
    lower = word.lower()
    if lower in ENGLISH_TO_KOREAN:
        return ENGLISH_TO_KOREAN[lower]

    g2p = get_g2p_en()
    if not g2p:
        return word

    try:
        arpabet_seq = g2p(word)
    except Exception:
        return word

    hangul = arpabet_to_hangul(arpabet_seq)
    return hangul or word


def convert_english_to_korean(text: str) -> str:
    """사전과 g2p-en을 활용해 문장 내 영어를 한글 발음으로 치환"""
    result = text
    # 긴 구문부터 적용
    sorted_phrases = sorted(ENGLISH_TO_KOREAN.items(), key=lambda x: len(x[0]), reverse=True)

    for eng, kor in sorted_phrases:
        pattern = r"(?<![A-Za-z])" + re.escape(eng) + r"(?![A-Za-z])"
        result = re.sub(pattern, kor, result, flags=re.IGNORECASE)

    return result


__all__ = [
    "ENGLISH_TO_KOREAN",
    "G2P_EN_AVAILABLE",
    "english_to_korean_auto",
    "convert_english_to_korean",
    "get_g2p_en",
]
