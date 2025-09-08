"""
/auth/oauth/verify: 클라이언트가 준 id_token(구글 등)을 OIDC(JWKS)로 검증 → 내부 JWT access/refresh 발급 → Access는 세션쿠키 저장

/ha/: 세션쿠키의 내부 JWT를 검증 → X-Remote-User 등 SSO 헤더를 붙여 HA로 프록시 → HA는 헤더 인증 컴포넌트로 자동 로그인

/v1/alerts/fall: 낙상 알림을 받아 FCM + HA notify 모두 발송
"""