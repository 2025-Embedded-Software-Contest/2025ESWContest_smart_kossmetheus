from typing import Dict # 타입 힌트

from gateway.core.settings import Settings


def build_sso_headers(s: Settings, username: str) -> Dict[str, str]:
    headers = { s.ha_sso_header: username }
    if s.ha_sso_groups_header and s.ha_sso_default_groups:
        headers[s.ha_sso_groups_header] = s.ha_sso_default_groups
        
    return headers
