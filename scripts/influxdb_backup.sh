#!/bin/bash

# ============================================
# InfluxDB 자동 백업 스크립트
# ============================================
# 작성자: Home Assistant 사용자
# 최초 작성: 2025-10-27
# 마지막 수정: 2025-10-27
#
# 용도:
#   - InfluxDB 데이터베이스 자동 백업
#   - 격주 일요일 새벽 3시에 실행
#   - 60일 이상 된 백업 자동 삭제
#
# 백업 방식:
#   - SSH를 통해 Host OS 접속
#   - Docker exec로 InfluxDB 컨테이너 접근
#   - influxd backup -portable 명령 실행
#   - 파일 시스템 레벨 백업 (사용자 인증 우회)
#
# 저장 위치:
#   - Host OS: /usr/share/hassio/share/influxdb_backups/
#   - Home Assistant: /share/influxdb_backups/ (마운트됨)
#
# 보안:
#   - SSH 키 인증 사용
#   - InfluxDB v1.x portable 백업은 사용자 인증 미지원
#   - backup 사용자는 Grafana 등 다른 용도로 활용
#
# 참고:
#   - InfluxDB 애드온 버전: v5.0.2
#   - 실제 InfluxDB 버전: v1.8.x
# ============================================

# ------------------------------
# 환경 변수 설정
# ------------------------------
BACKUP_DIR="/share/influxdb_backups"           # Home Assistant 내 백업 디렉토리
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")            # 백업 타임스탬프 (예: 2025-10-27_03-00)
BACKUP_NAME="backup_${TIMESTAMP}"              # 백업 폴더 이름
LOG_FILE="$BACKUP_DIR/backup.log"              # 백업 로그 파일
STATUS_FILE="$BACKUP_DIR/last_backup_status.txt"  # 마지막 백업 상태 파일

# ------------------------------
# 백업 시작 로그 기록
# ------------------------------
echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): Starting backup..." >> "$LOG_FILE"

# ------------------------------
# SSH로 Host OS 접속 및 백업 실행
# ------------------------------
# SSH 키를 사용하여 Host OS (localhost:22)에 root 계정으로 접속
# heredoc (EOF)을 사용하여 원격 스크립트 실행
BACKUP_RESULT=$(ssh -i /config/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@localhost -p 22 /bin/bash << 'EOF'

# PATH 설정 (docker 명령어 위치 명시)
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Host OS에서 사용할 타임스탬프 생성
BACKUP_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_PATH="/usr/share/hassio/share/influxdb_backups/backup_${BACKUP_TIMESTAMP}"

# InfluxDB 백업 실행
# - addon_a0d7b954_influxdb: InfluxDB 컨테이너 이름
# - influxd backup -portable: InfluxDB v1.x 백업 명령
# - /data/influxdb/backup_temp: 컨테이너 내부 임시 백업 위치
docker exec addon_a0d7b954_influxdb influxd backup -portable /data/influxdb/backup_temp

# Host OS에 백업 폴더 생성
mkdir -p "${BACKUP_PATH}"

# 컨테이너에서 Host OS로 백업 파일 복사
docker cp addon_a0d7b954_influxdb:/data/influxdb/backup_temp/. "${BACKUP_PATH}/"

# 컨테이너 내부의 임시 백업 삭제 (정리)
docker exec addon_a0d7b954_influxdb rm -rf /data/influxdb/backup_temp

# 60일(2달) 이상 된 백업 자동 삭제
# - find: 파일 검색 명령
# - -type d: 디렉토리만 검색
# - -name "backup_*": backup_으로 시작하는 폴더
# - -mtime +60: 60일 이상 된 파일
# - -exec rm -rf {} +: 찾은 파일 삭제
find /usr/share/hassio/share/influxdb_backups/ -type d -name "backup_*" -mtime +60 -exec rm -rf {} + 2>/dev/null

# 백업 성공 여부 확인
FILE_COUNT=$(ls -1 "${BACKUP_PATH}/" 2>/dev/null | wc -l)
if [ "$FILE_COUNT" -gt 0 ]; then
    # 백업 파일이 존재하면 성공
    echo "SUCCESS:${BACKUP_TIMESTAMP}"
else
    # 백업 파일이 없으면 실패
    echo "FAILED:${BACKUP_TIMESTAMP}"
fi
EOF
)

# ------------------------------
# 백업 결과 처리
# ------------------------------
# SSH 실행 결과에서 상태와 타임스탬프 추출
RESULT_STATUS=$(echo "$BACKUP_RESULT" | grep -o "SUCCESS\|FAILED")
RESULT_TIMESTAMP=$(echo "$BACKUP_RESULT" | cut -d':' -f2)

# 결과에 따라 상태 파일 및 로그 업데이트
if [ "$RESULT_STATUS" = "SUCCESS" ]; then
    # 백업 성공
    echo "success" > "$STATUS_FILE"
    echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): ✅ Backup completed - $BACKUP_DIR/$BACKUP_NAME" >> "$LOG_FILE"
else
    # 백업 실패
    echo "failed" > "$STATUS_FILE"
    echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): ❌ Backup FAILED!" >> "$LOG_FILE"
fi

# ============================================
# 스크립트 종료
# ============================================
