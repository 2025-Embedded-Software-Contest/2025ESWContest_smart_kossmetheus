#!/bin/bash

set -e

BACKUP_TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_PATH="/tmp/backup_test_${BACKUP_TIMESTAMP}"

echo "[Test] InfluxDB 백업 컨테이너 내 생성..."
docker exec addon_a0d7b954_influxdb influxd backup -portable /data/influxdb/backup_temp

echo "[Test] 백업 temp폴더에 파일 생성 대기(최대 15초)..."
for i in {1..15}; do
    FILE_COUNT=$(docker exec addon_a0d7b954_influxdb ls -1 /data/influxdb/backup_temp 2>/dev/null | wc -l)
    echo "  [Test] 현재 파일 개수: $FILE_COUNT"
    if [ "$FILE_COUNT" -gt 0 ]; then
        break
    fi
    sleep 1
done

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "[ERROR] 컨테이너 내 백업파일 생성 실패!"
    exit 1
fi

echo "[Test] Host로 임시 백업 복사: $BACKUP_PATH"
mkdir -p "$BACKUP_PATH"
docker cp addon_a0d7b954_influxdb:/data/influxdb/backup_temp/. "$BACKUP_PATH/"
if [ $? -ne 0 ]; then
    echo "[ERROR] docker cp 실패!"
    exit 1
fi

echo "[Test] 복사된 파일 리스트:"
ls -l "$BACKUP_PATH"

echo "[Test] 컨테이너 임시 backup_temp 폴더 삭제"
docker exec addon_a0d7b954_influxdb rm -rf /data/influxdb/backup_temp

echo "[Test] 완료!"
