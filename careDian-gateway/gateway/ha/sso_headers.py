from typing import Dict # 타입 힌트

from gateway.core.settings import Settings


# HA 프록시 통신 SSO 헤더 생성
def build_sso_headers(s: Settings, username: str) -> Dict[str, str]:
    # 기본 사용자 헤더 추가
    headers = { s.ha_sso_header: username }
    # 그룹 헤더 추가 (옵션)
    if s.ha_sso_groups_header and s.ha_sso_default_groups:
        headers[s.ha_sso_groups_header] = s.ha_sso_default_groups
        
    return headers
