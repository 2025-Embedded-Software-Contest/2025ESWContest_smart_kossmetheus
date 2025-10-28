#!/bin/bash


# ============================================
# InfluxDB 자동 백업 스크립트
# ============================================


# ------------------------------
# 환경 변수 설정
# ------------------------------
BACKUP_DIR="/share/influxdb_backups"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_NAME="backup_${TIMESTAMP}"
LOG_FILE="$BACKUP_DIR/backup.log"
STATUS_FILE="$BACKUP_DIR/last_backup_status.txt"


# ------------------------------
# 백업 시작 로그 기록
# ------------------------------
echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): Starting backup..." >> "$LOG_FILE"


# ------------------------------
# SSH로 Host OS 접속 및 백업 실행
# ------------------------------
BACKUP_RESULT=$(ssh -i /config/.ssh/id_ed25519 -o StrictHostKeyChecking=no root@localhost -p 22 /bin/bash << 'EOF'

export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

BACKUP_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_PATH="/usr/share/hassio/share/influxdb_backups/backup_${BACKUP_TIMESTAMP}"

# InfluxDB 백업 실행
docker exec addon_a0d7b954_influxdb influxd backup -portable /data/influxdb/backup_temp

if [ $? -ne 0 ]; then
    echo "FAILED:${BACKUP_TIMESTAMP}:docker_backup_failed"
    exit 1
fi

# Host OS에 백업 폴더 생성
mkdir -p "${BACKUP_PATH}"

# 컨테이너에서 Host OS로 백업 파일 복사
docker cp addon_a0d7b954_influxdb:/data/influxdb/backup_temp/. "${BACKUP_PATH}/"

if [ $? -ne 0 ]; then
    echo "FAILED:${BACKUP_TIMESTAMP}:docker_cp_failed"
    exit 1
fi

# 백업 파일 개수 확인 (암호화 전)
FILE_COUNT=$(ls -1 "${BACKUP_PATH}/" 2>/dev/null | wc -l)
if [ "$FILE_COUNT" -eq 0 ]; then
    echo "FAILED:${BACKUP_TIMESTAMP}:no_backup_files"
    exit 1
fi

# 컨테이너 내부의 임시 백업 삭제
docker exec addon_a0d7b954_influxdb rm -rf /data/influxdb/backup_temp

# ============================================
# Host OS에서 직접 암호화
# ============================================
cd /usr/share/hassio/share/influxdb_backups/

BACKUP_FOLDER="backup_${BACKUP_TIMESTAMP}"

if [ -d "${BACKUP_FOLDER}" ]; then
    tar -czf - "${BACKUP_FOLDER}" | \
        openssl enc -aes-256-cbc \
            -salt \
            -pbkdf2 \
            -pass pass:"lifeisgood" \
            -out "${BACKUP_FOLDER}.tar.gz.enc"
    
    if [ $? -eq 0 ] && [ -f "${BACKUP_FOLDER}.tar.gz.enc" ]; then
        rm -rf "${BACKUP_FOLDER}"
        echo "SUCCESS:${BACKUP_TIMESTAMP}"
    else
        echo "FAILED:${BACKUP_TIMESTAMP}:encryption_failed"
        exit 1
    fi
else
    echo "FAILED:${BACKUP_TIMESTAMP}:folder_not_found"
    exit 1
fi
# ============================================

# 60일 이상 된 백업 자동 삭제
find /usr/share/hassio/share/influxdb_backups/ -type d -name "backup_*" -mtime +60 -exec rm -rf {} + 2>/dev/null
find /usr/share/hassio/share/influxdb_backups/ -type f -name "backup_*.tar.gz.enc" -mtime +60 -delete 2>/dev/null

EOF
)


# ------------------------------
# 백업 결과 처리
# ------------------------------    
RESULT_STATUS=$(echo "$BACKUP_RESULT" | grep -o "SUCCESS\|FAILED")


# ------------------------------
# 백업 완료 로그
# ------------------------------
if [ "$RESULT_STATUS" = "SUCCESS" ]; then
    echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): ✅ Backup and encryption completed successfully!" >> "$LOG_FILE"
    echo "success" > "$STATUS_FILE"
else
    ERROR_DETAIL=$(echo "$BACKUP_RESULT" | grep "FAILED" | cut -d':' -f3)
    echo "$(date +'%a %b %d %H:%M:%S %Z %Y'): ❌ Backup FAILED! Error: ${ERROR_DETAIL}" >> "$LOG_FILE"
    echo "failed:${ERROR_DETAIL}" > "$STATUS_FILE"
fi


# ============================================
# 스크립트 종료
# ============================================
