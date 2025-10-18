#!/bin/bash

BACKUP_DIR="/share/influxdb_backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_NAME="backup_${TIMESTAMP}"
LOG_FILE="$BACKUP_DIR/backup.log"
STATUS_FILE="$BACKUP_DIR/last_backup_status.txt"

# 로그 기록
echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): Starting backup..." >> "$LOG_FILE"

# InfluxDB 백업 (컨테이너 내부에서 실행)
docker exec addon_a0d7b954_influxdb influxd backup -portable /data/influxdb/backup_temp >> "$LOG_FILE" 2>&1

# 백업 폴더 생성
mkdir -p "$BACKUP_DIR/$BACKUP_NAME"

# 컨테이너에서 호스트로 백업 파일 복사
docker cp addon_a0d7b954_influxdb:/data/influxdb/backup_temp/. "$BACKUP_DIR/$BACKUP_NAME/" >> "$LOG_FILE" 2>&1

# 컨테이너 내부 임시 백업 삭제
docker exec addon_a0d7b954_influxdb rm -rf /data/influxdb/backup_temp

# 백업 성공 여부 확인: 백업 폴더에 파일이 있는지 확인
FILE_COUNT=$(ls -1 "$BACKUP_DIR/$BACKUP_NAME/" 2>/dev/null | wc -l)

if [ "$FILE_COUNT" -gt 0 ]; then
    echo "success" > "$STATUS_FILE"
    echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): ✅ Backup completed - $BACKUP_DIR/$BACKUP_NAME" >> "$LOG_FILE"
else
    echo "failed" > "$STATUS_FILE"
    echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): ❌ Backup FAILED!" >> "$LOG_FILE"
fi
