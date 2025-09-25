#include <WiFi.h>
#include <HTTPClient.h>
#include "DFRobot_HumanDetection.h"

#define RX_PIN 16   // 센서 TX → ESP32 RX
#define TX_PIN 17   // 센서 RX → ESP32 TX

const char* WIFI_SSID = "SK_AEC0_5G";
const char* WIFI_PASS = "HUZ25@9801";

const char* API_URL   = "http://192.168.45.33:8000/events"; // FastAPI 서버 IP

DFRobot_HumanDetection hu(&Serial1);
unsigned long lastSend = 0;
const unsigned long SEND_INTERVAL = 1000;  // 1초마다 전송

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN);

  // WiFi 연결
  Serial.printf("Connecting to %s", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nWiFi connected, IP: %s\n", WiFi.localIP().toString().c_str());

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

  hu.configLEDLight(hu.eFALLLed, 1);
  hu.configLEDLight(hu.eHPLed, 1);
  hu.dmInstallHeight(270);
  hu.dmFallTime(5);
  hu.dmUnmannedTime(1);
  hu.dmFallConfig(hu.eResidenceTime, 200);
  hu.dmFallConfig(hu.eFallSensitivityC, 3);
  hu.sensorRet();
  delay(500);
}

void loop() {
  int presence = hu.smHumanData(hu.eHumanPresence);
  int movement = hu.smHumanData(hu.eHumanMovement);
  int range    = hu.smHumanData(hu.eHumanMovingRange);
  int fallen   = hu.getFallData(hu.eFallState);
  int dwell    = hu.getFallData(hu.estaticResidencyState);

  // ---- 기존 Serial 출력 (그대로 유지) ----
  Serial.print("Existing information:");
  switch (presence) {
    case 0: Serial.println("No one is present"); break;
    case 1: Serial.println("Someone is present"); break;
    default: Serial.println("Read error");
  }

  Serial.print("Motion information:");
  switch (movement) {
    case 0: Serial.println("None"); break;
    case 1: Serial.println("Still"); break;
    case 2: Serial.println("Active"); break;
    default: Serial.println("Read error");
  }

  Serial.printf("Body movement parameters:%d\n", range);
  Serial.print("Fall status:"); Serial.println(fallen ? "Fallen" : "Not fallen");
  Serial.print("Stationary dwell status:"); Serial.println(dwell ? "Stationary dwell present" : "No stationary dwell");
  Serial.println();

  Serial.print("{\"device_id\":\"esp32_wroom_01\"");
  Serial.print(",\"presence\":");      Serial.print(presence);
  Serial.print(",\"movement\":");      Serial.print(movement);
  Serial.print(",\"moving_range\":");  Serial.print(range);
  Serial.print(",\"fall_state\":");    Serial.print(fallen);
  Serial.print(",\"dwell_state\":");   Serial.print(dwell);
  Serial.print(",\"ts\":");            Serial.print((unsigned long)(millis()/1000));
  Serial.println("}");

  // ---- WiFi HTTP POST (1초마다) ----
  if (millis() - lastSend > SEND_INTERVAL && WiFi.status() == WL_CONNECTED) {
    lastSend = millis();

    String payload = "{";
    payload += "\"device_id\":\"esp32_wroom_01\",";
    payload += "\"presence\":" + String(presence) + ",";
    payload += "\"movement\":" + String(movement) + ",";
    payload += "\"moving_range\":" + String(range) + ",";
    payload += "\"fall_state\":" + String(fallen) + ",";
    payload += "\"dwell_state\":" + String(dwell) + ",";
    payload += "\"ts\":" + String((unsigned long)(millis()/1000));
    payload += "}";

    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");
    int code = http.POST(payload);
    Serial.printf("POST %d: %s\n", code, payload.c_str());
    http.end();
  }

  delay(1000);
}
