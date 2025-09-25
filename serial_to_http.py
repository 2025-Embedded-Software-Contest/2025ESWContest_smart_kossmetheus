#mmwave센서 유선으로 연결했을 시 사용하는 코드
import json, requests, serial

SERIAL_PORT = "/dev/cu.usbserial-2120"  
BAUD = 115200
API_URL = "http://127.0.0.1:8000/events"

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=2)
    print("listening:", SERIAL_PORT)
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line: 
            continue
        if not (line.startswith("{") and line.endswith("}")):
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        try:
            r = requests.post(API_URL, json=data, timeout=2)
            print("POST", r.status_code, data)
        except Exception as e:
            print("POST error:", e)

if __name__ == "__main__":
    main()
