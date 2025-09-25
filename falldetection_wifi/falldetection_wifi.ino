#include <WiFi.h>
#include <HTTPClient.h>
#include "DFRobot_HumanDetection.h"

// ====== 하드웨어 연결 ======
#define RX_PIN 16    // 센서 TX -> ESP32 RX_PIN
#define TX_PIN 17    // 센서 RX -> ESP32 TX_PIN

// ====== 네트워크/서버 ======
const char* WIFI_SSID = "wifissid";
const char* WIFI_PW   = "wifi_pw";

const char* API_URL   = "http://192.168.45.33:8000/events"; 

// ====== 센서/전송 ======
DFRobot_HumanDetection hu(&Serial1);
unsigned long lastSendMs = 0;
const unsigned long SEND_INTERVAL_MS = 1000; // 1초마다 전송

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN);

  // Wi-Fi 연결
  WiFi.begin(WIFI_SSID, WIFI_PW);
  Serial.print("WiFi connecting");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());

  // 센서 초기화
  Serial.println("Start initialization");
  while (hu.begin() != 0) {
    Serial.println("init error!!!");
    delay(1000);
  }
  Serial.println("Initialization successful");

  Serial.println("Start switching work mode");
  while (hu.configWorkMode(hu.eFallingMode) != 0) {
    Serial.println("error!!!");
    delay(1000);
  }
  Serial.println("Work mode switch successful");

  // 파라미터 설정 (필요에 맞게 조정)
  hu.configLEDLight(hu.eFALLLed, 1);
  hu.configLEDLight(hu.eHPLed, 1);
  hu.dmInstallHeight(270);
  hu.dmFallTime(5);
  hu.dmUnmannedTime(1);
  hu.dmFallConfig(hu.eResidenceTime, 200);
  hu.dmFallConfig(hu.eFallSensitivityC, 3);
  hu.sensorRet();  // 설정 후 모듈 리셋
  delay(500);

  // 현재 설정 출력
  Serial.print("Current work mode: ");
  Serial.println(hu.getWorkMode());
  Serial.printf("Radar installation height: %d cm\n", hu.dmGetInstallHeight());
  Serial.printf("Fall duration: %d s\n", hu.getFallTime());
  Serial.printf("Unattended: %d s\n", hu.getUnmannedTime());
  Serial.printf("Dwell: %d s\n", hu.getStaticResidencyTime());
  Serial.printf("Fall sensitivity: %d\n", hu.getFallData(hu.eFallSensitivity));
  Serial.println();
}

void loop() {
  // ---- 시리얼 로그(원본 예제 출력 유지) ----
  Serial.print("Existing information:");
  int presence = hu.smHumanData(hu.eHumanPresence);
  switch (presence) {
    case 0: Serial.println("No one is present"); break;
    case 1: Serial.println("Someone is present"); break;
    default: Serial.println("Read error"); break;
  }

  Serial.print("Motion information:");
  int movement = hu.smHumanData(hu.eHumanMovement); // 0:none 1:still 2:active
  switch (movement) {
    case 0: Serial.println("None"); break;
    case 1: Serial.println("Still"); break;
    case 2: Serial.println("Active"); break;
    default: Serial.println("Read error"); break;
  }

  int range  = hu.smHumanData(hu.eHumanMovingRange);
  int fallen = hu.getFallData(hu.eFallState);              // 0/1
  int dwell  = hu.getFallData(hu.estaticResidencyState);   // 0/1
  Serial.printf("Body movement parameters:%d\n", range);
  Serial.print("Fall status:");
  Serial.println(fallen ? "Fallen" : "Not fallen");
  Serial.print("Stationary dwell status:");
  Serial.println(dwell ? "Stationary dwell present" : "No stationary dwell");
  Serial.println();

  // ---- FastAPI로 1초마다 전송 ----
  if (millis() - lastSendMs > SEND_INTERVAL_MS && WiFi.status() == WL_CONNECTED) {
    lastSendMs = millis();

    String payload = "{";
    payload += "\"device_id\":\"esp32_wroom_01\",";
    payload += "\"presence\":"     + String(presence) + ",";
    payload += "\"movement\":"     + String(movement) + ",";
    payload += "\"moving_range\":" + String(range)    + ",";
    payload += "\"fall_state\":"   + String(fallen)   + ",";
    payload += "\"dwell_state\":"  + String(dwell)    + ",";
    payload += "\"ts\":"           + String((unsigned long)(millis()/1000));
    payload += "}";

    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");
    int code = http.POST(payload);
    Serial.printf("POST %d: %s\n", code, payload.c_str());
    http.end();
  }

  delay(50);
}
