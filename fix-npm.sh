#!/bin/bash
echo "=== npm uv_cwd 오류 해결 스크립트 ==="

# 1. 안전한 디렉토리로 이동
echo "안전한 디렉토리로 이동 중..."
cd /config || cd ~ || cd /

# 2. 현재 위치 확인
echo "현재 디렉토리: $(pwd)"

# 3. npm 환경 정리
echo "npm 캐시 및 설정 정리 중..."
rm -rf ~/.npm 2>/dev/null || true
rm -f ~/.npmrc 2>/dev/null || true

# 4. Node.js 및 npm 상태 확인
echo "Node.js 버전: $(node --version)"
echo "npm 경로: $(which npm)"

# 5. npm 실행 테스트
if npm --version >/dev/null 2>&1; then
    echo "✅ npm 정상 작동: $(npm --version)"
    echo "=== 해결 완료 ==="
else
    echo "❌ npm 여전히 실행 불가"
    echo "=== 추가 조치 필요 ==="
fi
