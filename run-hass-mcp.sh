#!/usr/bin/env bash
set -euo pipefail

# .env.hass-mcp 파일에서 환경변수를 불러옵니다 (있을 경우)
if [ -f "$(dirname "$0")/.env.hass-mcp" ]; then
  # shellcheck disable=SC1090
  source "$(dirname "$0")/.env.hass-mcp"
fi

# Home Assistant URL/토큰이 환경변수로 주어지지 않았다면 기본값 사용
HA_URL="${HA_URL:-http://homeassistant.local:8123}"
HA_TOKEN="${HA_TOKEN:-}"

if [ -z "$HA_TOKEN" ]; then
  echo "[hass-mcp] HA_TOKEN이 비어 있습니다. .env.hass-mcp에 설정하거나 환경변수로 전달하세요." >&2
  exit 1
fi

# 필요 시 --network host 를 추가하세요 (동일 머신 Docker/HA 조합에서 네트워크 이슈 시)
# Mac/Windows Docker Desktop에선 host 네트워크가 제한적이므로, HA_URL에 host.docker.internal 사용 권장

docker run -i --rm \
  -e HA_URL="$HA_URL" \
  -e HA_TOKEN="$HA_TOKEN" \
  voska/hass-mcp
