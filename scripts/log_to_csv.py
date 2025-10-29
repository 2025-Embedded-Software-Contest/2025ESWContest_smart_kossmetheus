import csv
import json
import re
import datetime
import time
import ast


LOG_FILE = "server.log"
CSV_PATH = "fall_realtime_log.csv"
SCENARIO = "낙상_움직임o"

json_pattern = re.compile(r"\{.*\}")

def main():
    print(f"🚀 실시간 로그 수집 시작 (시나리오: {SCENARIO})")
    print("💾 server.log를 모니터링 중... (중단: Ctrl + C)\n")

    with open(CSV_PATH, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "device_id", "presence", "movement",
            "moving_range", "fall_state", "dwell_state", "scenario"
        ])

    with open(LOG_FILE, "r") as log:
        log.seek(0, 2)  # 파일 끝으로 이동 (기존 로그 무시)
        while True:
            line = log.readline()
            if not line:
                time.sleep(0.3)
                continue

            if "[RECEIVED] Fall event data:" in line:
                match = json_pattern.search(line)
                if match:
                    try:
                        data = ast.literal_eval(match.group())
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        with open(CSV_PATH, mode="a", newline="") as f:
                            writer = csv.writer(f)
                            writer.writerow([
                                now,
                                data.get("device_id"),
                                data.get("presence"),
                                data.get("movement"),
                                data.get("moving_range"),
                                data.get("fall_state"),
                                data.get("dwell_state"),
                                SCENARIO
                            ])
                        print(f"저장 완료: {data}")

                    except json.JSONDecodeError:
                        print("⚠️ JSON 파싱 실패:", line)
                    except Exception as e:
                        print("❌ 저장 오류:", e)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 로그 수집 종료")
