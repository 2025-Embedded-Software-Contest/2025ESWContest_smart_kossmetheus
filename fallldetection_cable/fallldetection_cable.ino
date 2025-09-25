/**！
 * @file basics.ino
 * @brief This is the fall detection usage routine of the C1001 mmWave Human Detection Sensor.
 * @copyright  Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [tangjie](jie.tang@dfrobot.com)
 * @version  V1.0
 * @date  2024-06-03
 * @url https://github.com/DFRobot/DFRobot_HumanDetection
 */

#include "DFRobot_HumanDetection.h"

DFRobot_HumanDetection hu(&Serial1);

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1, 4, 5);

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

  hu.configLEDLight(hu.eFALLLed, 1);         // Set HP LED switch, it will not light up even if the sensor detects a person present when set to 0.
  hu.configLEDLight(hu.eHPLed, 1);           // Set FALL LED switch, it will not light up even if the sensor detects a person falling when set to 0.
  hu.dmInstallHeight(270);                   // Set installation height, it needs to be set according to the actual height of the surface from the sensor, unit: CM.
  hu.dmFallTime(5);                          // Set fall time, the sensor needs to delay the current set time after detecting a person falling before outputting the detected fall, this can avoid false triggering, unit: seconds.
  hu.dmUnmannedTime(1);                      // Set unattended time, when a person leaves the sensor detection range, the sensor delays a period of time before outputting a no person status, unit: seconds.
  hu.dmFallConfig(hu.eResidenceTime, 200);   // Set dwell time, when a person remains still within the sensor detection range for more than the set time, the sensor outputs a stationary dwell status. Unit: seconds.
  hu.dmFallConfig(hu.eFallSensitivityC, 3);  // Set fall sensitivity, range 0~3, the larger the value, the more sensitive.
  hu.sensorRet();                            // Module reset, must perform sensorRet after setting data, otherwise the sensor may not be usable.

  Serial.print("Current work mode:");
  switch (hu.getWorkMode()) {
    case 1:
      Serial.println("Fall detection mode");
      break;
    case 2:
      Serial.println("Sleep detection mode");
      break;
    default:
      Serial.println("Read error");
  }

  Serial.print("HP LED status:");
  switch (hu.getLEDLightState(hu.eHPLed)) {
    case 0:
      Serial.println("Off");
      break;
    case 1:
      Serial.println("On");
      break;
    default:
      Serial.println("Read error");
  }
  Serial.print("FALL status:");
  switch (hu.getLEDLightState(hu.eFALLLed)) {
    case 0:
      Serial.println("Off");
      break;
    case 1:
      Serial.println("On");
      break;
    default:
      Serial.println("Read error");
  }

  Serial.printf("Radar installation height: %d cm\n", hu.dmGetInstallHeight());
  Serial.printf("Fall duration: %d seconds\n", hu.getFallTime());
  Serial.printf("Unattended duration: %d seconds\n", hu.getUnmannedTime());
  Serial.printf("Dwell duration: %d seconds\n", hu.getStaticResidencyTime());
  Serial.printf("Fall sensitivity: %d \n", hu.getFallData(hu.eFallSensitivity));
  Serial.println();
  Serial.println();
}


void loop() {
  Serial.print("Existing information:");
  int presence = hu.smHumanData(hu.eHumanPresence);
  switch (presence) {
    case 0: Serial.println("No one is present"); break;
    case 1: Serial.println("Someone is present"); break;
    default: Serial.println("Read error");
  }

  Serial.print("Motion information:");
  int movement = hu.smHumanData(hu.eHumanMovement);
  switch (movement) {
    case 0: Serial.println("None"); break;
    case 1: Serial.println("Still"); break;
    case 2: Serial.println("Active"); break;
    default: Serial.println("Read error");
  }

  int range  = hu.smHumanData(hu.eHumanMovingRange);
  int fallen = hu.getFallData(hu.eFallState);
  int dwell  = hu.getFallData(hu.estaticResidencyState);

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
  // -----------------------------------------------

  delay(1000);
}


