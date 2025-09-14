"""
주의/개선 포인트 (실운영 기준)

필수 클레임 강제 (권장)
현재는 exp/nbf/iss/aud가 없어도 통과 가능(검증 인자 안 주면).

액세스 토큰: sub, iat, nbf, exp, typ="access" 필수 권장

리프레시 토큰: sub, iat, nbf, exp, typ="refresh", jti 필수 권장
→ 미존재 시 명확히 JWTError 반환하도록 옵션 제공 고려.

시크릿 빈값 방지
이미 Empty secret not allowed로 막고 있어 좋습니다. 운영에선 32바이트 이상 랜덤 권장.

타입/캐스팅 안전성
_to_int로 숫자 캐스팅 실패 대응 좋은데, iat 등도 동일 정책으로 점검하고 싶으면 확장하세요.

토큰 길이 상한(선택)
과도하게 큰 토큰에 대한 방어(DoS 완화)를 위해 len(token) 상한선(예: 8KB) 체크 고려.

파이썬 버전 주의
Sequence[str] | str는 Python 3.10+ 문법입니다. 3.9 이하 호환이 필요하면:

from __future__ import annotations
# 또는
from typing import Union
aud: Optional[Union[Sequence[str], str]] = None
"""