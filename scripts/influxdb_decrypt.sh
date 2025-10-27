# /config/scripts/influxdb_decrypt.sh

#!/bin/bash

if [ -z "$1" ]; then
    echo "사용법: $0 <암호화된 파일>"
    exit 1
fi

ENCRYPTED_FILE="$1"
OUTPUT_DIR="${ENCRYPTED_FILE%.tar.gz.enc}"

echo "복호화 중: $ENCRYPTED_FILE"

openssl enc -aes-256-cbc -d \
    -pbkdf2 \
    -pass pass:"lifeisgood" \
    -in "$ENCRYPTED_FILE" | \
    tar -xzf -

if [ -d "$OUTPUT_DIR" ]; then
    echo "복호화 완료: $OUTPUT_DIR"
else
    echo "복호화 실패"
    exit 1
fi
