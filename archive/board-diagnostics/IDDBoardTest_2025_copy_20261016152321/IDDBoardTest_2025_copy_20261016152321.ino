#define USE_MPR121Control

#define USE_SH1106Control

// #include <Adafruit_SSD1306.h>

#define USE_SSD1306Control

#define USE_AddrLEDControl

#define USE_WiFiControl

#define USE_HTTPClientControl

#define USE_DFPlayerMP3Control

#define USE_UltraSonicControl

#define USE_VL53L0XControl

// #define USE_LiquidCrystal

#include <IO_Control.h>
#include <LittleFS.h>
#include <ArduinoJson.h>
#include <WebServer.h>
#include <WebSocketsServer.h>
#include <WebSocketsClient.h>
#include <PubSubClient.h>
#include <MQTTPubSubClient.h>
#include <WiFiUdp.h>
#ifdef USE_LiquidCrystal
#include <LiquidCrystal_I2C.h>
#endif
#include <algorithm>  // Include for std::min


#ifdef USE_NTP
#include <NTPClient.h>
#endif
#include "userDefSeq.h"

#define NUMFLAKES 10
#define XPOS 0
#define YPOS 1
#define DELTAY 2
#define LOGO16_GLCD_HEIGHT 16
#define LOGO16_GLCD_WIDTH 16

static const unsigned char PROGMEM logo16_glcd_bmp[] = { B00000000, B11000000,
                                                         B00000001, B11000000,
                                                         B00000001, B11000000,
                                                         B00000011, B11100000,
                                                         B11110011, B11100000,
                                                         B11111110, B11111000,
                                                         B01111110, B11111111,
                                                         B00110011, B10011111,
                                                         B00011111, B11111100,
                                                         B00001101, B01110000,
                                                         B00011011, B10100000,
                                                         B00111111, B11100000,
                                                         B00111111, B11110000,
                                                         B01111100, B11110000,
                                                         B01110000, B01110000,
                                                         B00000000, B00110000 };

uint8_t icons[NUMFLAKES][3];

I2CMasterControl i2cCtrl;

MPR121Control mpr121Ctrl;

#ifdef USE_SH1106Control

SH1106Control sh1106Ctrl;

#endif

#ifdef USE_SSD1306Control

SSD1306Control ssd1306Ctrl;

#endif

AddrLEDControl addrLedCtrl;

ServoControl servoCtrl[6];

uint8_t noOfActiveServo = 0;

ToneControl toneCtrl;

ADCControl adcCtrl;

BinInControl binInCtrl;

BinOutControl binOutCtrl;

PWMControl pwmCtrl[6];

uint8_t noOfActivePWM = 0;

int currentChoice = 0;

bool waitingUserInput = false;

String storedUserInput = "";

typedef void (*FuncPtr_testcase)(String);

FuncPtr_testcase funcPtr_testcase = nullptr;

bool addr_waitingSecondInput = false;

uint8_t addr_firstInput = 0;

bool http_waitingSecondInput = false;

uint8_t http_firstInput = 0;

#ifdef USE_SH1106Control

bool sh1106Ready = false;

#endif

#ifdef USE_SSD1306Control

bool ssd1306Ready = false;

#endif

uint8_t displayType = 1;  // 0: not specified, 1: SH1106, 2:SSD1306

WiFiControl wifiCtrl;

#ifdef USE_HTTPClientControl
HTTPClientControl httpClientCtrl;
#endif

#ifdef USE_UltraSonicControl
UltraSonicControl ultraSonicCtrl;
#endif

String httpTargetLink = "";

uint16_t httpTargetPort = 0;

bool hasGotHeader = false;

bool hasGotResponse = false;

uint16_t wsDisplayMenuCountDown = 0;

String mac = "";

String wifi_ssid = "";

String wifi_pass = "";

String mqtt_server = "";

uint16_t mqtt_port;

String mqtt_topic = "";

bool mqtt_waitingSecondInput = false;

std::vector<String> mqtt_topics;

uint8_t mqtt_firstInput = 0;

String brokerAddr = "";

uint16_t brokerPort = 80;

bool mqttHasSubscribeTopic = false;

WiFiClient espClient;

PubSubClient client(espClient);

bool shouldMqttConnect = false;

WebSocketsClient wsClient;

MQTTPubSubClient wsMqttClient;

bool shouldMqttConnect_WS = false;

bool mqtt_ws_waitingSecondInput = false;

uint8_t mqtt_ws_firstInput = 0;

uint16_t mqttInputState = 0;  //used for hdlsecInput_mqtt. 0: waiting second input / 1: waiting additional topics / 2: waiting content to publish / 3: waiting for should retained

String mqtt_publish_topic = "";

String mqtt_publish_content = "";

bool mqtt_publish_retained = false;

String topic_head("sd/esp32c3");
String shared_pubTopic = topic_head + String("/shared/pub");
String shared_subTopic = topic_head + String("/shared/sub");
String self_pubTopic;
String self_subTopic;

WebServer server(80);

WebSocketsServer* webSocketServer = new WebSocketsServer(81);

bool isWsConnected = false;

unsigned long previousMillis = 0;

String httpReceivedBody = "";

UARTControl hwUartCtrl;

DFPlayerMP3Control mp3Ctrl;

#ifdef USE_VL53L0XControl
VL53L0XControl vl53l0xCtrl;
#endif


ServoSequence servoSeq0;

ServoSequence servoSeq1;

ServoSequence servoSeq2;

ServoSequence servoSeq3;

AddrLEDSequence addrSeq0;

AddrLEDSequence addrSeq1;

AddrLEDSequence addrSeq2;

AddrLEDSequence addrSeq3;

std::vector<int> addrTarget;

DFPlayerSequence mp3Seq0;

DFPlayerSequence mp3Seq1;

DFPlayerSequence mp3Seq2;

DFPlayerSequence mp3Seq3;

BinInControl bootButtonCtrl;

bool isBootButtonPressed = false;

uint32_t bootButtonPressedCount = 0;

bool isPlayingSeq = false;

uint32_t playSeqCount = 0;

uint8_t sequence_firstInput = 0;

bool sequence_waitingSecondInput = false;

uint8_t sequenceInputState = 0;

// std::map<int, int> mpr121_seq_map;

uint8_t mp3_firstInput = 0;

bool mp3_waitingSecondInput = false;

uint8_t mp3_currentVolume = 30;

DFPlayerSequence mp3Seq_advance;

int mpr121_seq_mapping[12];

uint8_t mpr121_seq_mode = 1;  // 1: wait until finish. 2: abort current and play next

int8_t playingSeq_testMode = -1;

AddrLEDSequence addrLedSeq_advance;

#ifdef USE_NTP
WiFiUDP ntpUDP;

NTPClient timeClient(ntpUDP);
#endif

bool shouldDisplayTime = false;

uint8_t displayTimeCount = 500;

String httpResponse = "";

#ifdef USE_LiquidCrystal
LiquidCrystal_I2C* lcd;
#endif

#ifdef USE_HTTPClientControl
DeclareHandler(httpTestModeHandler, _ctrl, HTTPClientControl, {
  if (_ctrl.isBodyIncomplete()) {
    httpResponse += _ctrl.getBody();
  }

  if (_ctrl.isBodyAvailable()) {
    httpResponse += _ctrl.getBody();

    JsonDocument doc;

    DeserializationError error = deserializeJson(doc, httpResponse);

    if (error) {
      Serial.print("deserializeJson() failed: ");
      Serial.println(error.c_str());
      return;
    }

    uint8_t currentTemp = 0;

    for (JsonObject temperature_data_item : doc["temperature"]["data"].as<JsonArray>()) {
      String temperature_data_item_place = temperature_data_item["place"].as<const char*>();
      int temperature_data_item_value = temperature_data_item["value"];

      if (temperature_data_item_place == "Kowloon City") {
        currentTemp = temperature_data_item_value;
      }
    }

    String updateTime = doc["updateTime"].as<const char*>();
    // sh1106Ctrl.getDisplay().clearDisplay();
    if (displayType == 1) {
      sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
      sh1106Ctrl.getDisplay().setCursor(0, 28);
      sh1106Ctrl.getDisplay().print("Temp: ");
      sh1106Ctrl.getDisplay().println(currentTemp);
      Serial.print("Temp: ");
      Serial.println(currentTemp);
      sh1106Ctrl.getDisplay().setCursor(0, 40);
      sh1106Ctrl.getDisplay().print("update time: ");
      sh1106Ctrl.getDisplay().println(updateTime);
      Serial.print("update time: ");
      Serial.println(updateTime);
      sh1106Ctrl.getDisplay().display();
    } else if (displayType == 2) {
      ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
      ssd1306Ctrl.getDisplay().setCursor(0, 28);
      ssd1306Ctrl.getDisplay().print("Temp: ");
      ssd1306Ctrl.getDisplay().println(currentTemp);
      Serial.print("Temp: ");
      Serial.println(currentTemp);
      ssd1306Ctrl.getDisplay().setCursor(0, 40);
      ssd1306Ctrl.getDisplay().print("update time: ");
      ssd1306Ctrl.getDisplay().println(updateTime);
      Serial.print("update time: ");
      Serial.println(updateTime);
      ssd1306Ctrl.getDisplay().display();
    }
  }
});
#endif

DeclareHandler(bootButtonHandler, _ctrl, BinInControl, {
  if (isBootButtonPressed) {
    bootButtonPressedCount++;
    if (bootButtonPressedCount >= 100) {
      bootButtonPressedCount = 0;
      // testcase_testMode();
      // currentChoice = 19;
      testcase_sequence();
      currentChoice = 20;
      handleInput_sequence("1");


      // sh1106Ctrl.getDisplay().display();
      // sh1106Ctrl.getDisplay().clearDisplay();
      // sh1106Ctrl.getDisplay().setTextSize(1);
      // sh1106Ctrl.getDisplay().setTextColor(SH110X_WHITE);
      // sh1106Ctrl.getDisplay().setTextWrap(true);
      // sh1106Ctrl.getDisplay().setCursor(0, 0);
      // sh1106Ctrl.getDisplay().println("Test Mode Activated");
      // sh1106Ctrl.getDisplay().display();
    }
  } else {
    bootButtonPressedCount = 0;
  }

  if (_ctrl.isBinInTriggered()) {
    if (_ctrl.getInterruptState()) {
      // Serial.println(" from LOW to HIGH");
      isBootButtonPressed = false;
    } else {
      // Serial.println(" from HIGH to LOW");
      isBootButtonPressed = true;
    }
  }
});

void displayMenu(bool wsOnly = false) {
  if (!wsOnly) {
    if (!bootButtonCtrl.isInit()) {
      bootButtonCtrl.init(9, INPUT);
      bootButtonCtrl.enableScheduler(0, 10, bootButtonHandler);
      bootButtonCtrl.enableInterrupt(CHANGE);
    }
    printlnMsg();
    printlnMsg("Menu:");
    printlnMsg("1: Download init file");
    printlnMsg("2: MPR121");
    if (displayType == 1) {
      printlnMsg("3: SH1106");
    } else {
      printlnMsg("3: SH1106 (disabled)");
    }
    if (displayType == 2) {
      printlnMsg("4: SSD1306");
    } else {
      printlnMsg("4: SSD1306 (disabled)");
    }
    printlnMsg("5: Neo Pixel");
    printlnMsg("6: Servo");
    printlnMsg("7: Tone");
    printlnMsg("8: PWM");
    printlnMsg("9: ADC");
    printlnMsg("10: GPIO IN");
    printlnMsg("11: GPIO OUT");
    if (wifiCtrl.isConnected()) {
      IPAddress ip = WiFi.localIP();
      String ip_str = String(ip[0]) + "." + String(ip[1]) + "." + String(ip[2]) + "." + String(ip[3]);
      // printlnMsg(ip_str);
      printMsg("12: WiFi (connected: ");
      printlnMsg(ip_str + ")");
    } else {
      printlnMsg("12: WiFi (not connected)");
    }
#ifdef USE_HTTPClientControl
    printlnMsg("13: HTTP Client");
#else
    printlnMsg("13: HTTP Client (disabled)");
#endif
    printlnMsg("14: MQTT(TCP)");
    printlnMsg("15: MQTT(WebSocket)");
    printlnMsg("16: MP3(DFPlayer mini)");
#ifdef USE_VL53L0XControl
    printlnMsg("17: VL53L0X");
#else
    printlnMsg("17: VL53L0X (disabled)");
#endif
    printlnMsg("18: List File");
    printlnMsg("19: Test Mode");
    printlnMsg("20: play sequence");
#ifdef USE_LiquidCrystal
    printlnMsg("21: LCD1602");
#else
    printlnMsg("21: LCD1602 (disabled)");
#endif
#ifdef USE_UltraSonicControl
    printlnMsg("22: Ultrasonic Sensor");
#else
    printlnMsg("22: Ultrasonic Sensor (disabled)");
#endif
    if (displayType == 1) {
      printlnMsg("23: Select Display Type (Current: SH1106)");
    } else {
      printlnMsg("23: Select Display Type (Current: SSD1306)");
    }
    printlnMsg("Enter your choice:");
  } else {
    webSocketServer->broadcastTXT("\n");
    webSocketServer->broadcastTXT("Menu:\n");
    webSocketServer->broadcastTXT("1: Download init file\n");
    webSocketServer->broadcastTXT("2: MPR121\n");
#ifdef USE_SH1106Control
    webSocketServer->broadcastTXT("3: SH1106\n");
#else
    webSocketServer->broadcastTXT("3: SH1106 (disabled)\n");
#endif
#ifdef USE_SSD1306Control
    webSocketServer->broadcastTXT("4: SSD1306\n");
#else
    webSocketServer->broadcastTXT("4: SSD1306 (disabled)\n");
#endif
    webSocketServer->broadcastTXT("5: Neo Pixel\n");
    webSocketServer->broadcastTXT("6: Servo\n");
    webSocketServer->broadcastTXT("7: Tone\n");
    webSocketServer->broadcastTXT("8: PWM\n");
    webSocketServer->broadcastTXT("9: ADC\n");
    webSocketServer->broadcastTXT("10: GPIO IN\n");
    webSocketServer->broadcastTXT("11: GPIO OUT\n");
    if (wifiCtrl.isConnected()) {
      webSocketServer->broadcastTXT("12: WiFi (connected)\n");
    } else {
      webSocketServer->broadcastTXT("12: WiFi (not connected)\n");
    }
#ifdef USE_HTTPClientControl
    webSocketServer->broadcastTXT("13: HTTP Client\n");
#else
    webSocketServer->broadcastTXT("13: HTTP Client (disabled)\n");
#endif
    webSocketServer->broadcastTXT("14: MQTT(TCP)\n");
    webSocketServer->broadcastTXT("15: MQTT(WebSocket)\n");
    webSocketServer->broadcastTXT("16: MP3(DFPlayer mini)\n");
#ifdef USE_VL53L0XControl
    webSocketServer->broadcastTXT("17: VL53L0X\n");
#else
    webSocketServer->broadcastTXT("17: VL53L0X (disabled)\n");
#endif
    webSocketServer->broadcastTXT("18: List File\n");
    webSocketServer->broadcastTXT("19: Test Mode\n");
    webSocketServer->broadcastTXT("20: play sequence\n");
#ifdef USE_LiquidCrystal
    webSocketServer->broadcastTXT("21: LCD1602\n");
#else
    webSocketServer->broadcastTXT("21: LCD1602 (disabled)\n");
#endif
#ifdef USE_UltraSonicControl
    webSocketServer->broadcastTXT("22: Ultrasonic Sensor\n");
#else
    webSocketServer->broadcastTXT("22: Ultrasonic Sensor (disabled)\n");
#endif
    if (displayType == 1) {
      webSocketServer->broadcastTXT("23: Select Display Type (Current: SH1106)\n");
    } else {
      webSocketServer->broadcastTXT("23: Select Display Type (Current: SSD1306)\n");
    }
    webSocketServer->broadcastTXT("Enter your choice:\n");
  }
}

void listDir(const char* dirname, uint8_t levels) {
  // Serial.printf("Listing directory: %s\r\n", dirname);
  printMsg("Listing directory: ");
  printlnMsg(dirname);

  File root = LittleFS.open(dirname);
  if (!root) {
    printlnMsg("- failed to open directory");
    return;
  }
  if (!root.isDirectory()) {
    printlnMsg(" - not a directory");
    return;
  }

  File file = root.openNextFile();
  while (file) {
    if (file.isDirectory()) {
      printMsg("  DIR : ");
      printlnMsg(file.name());
      if (levels) {
        listDir(file.path(), levels - 1);
      }
    } else {
      printMsg("  FILE: ");
      printMsg(file.name());
      printMsg("\tSIZE: ");
      printlnMsg(String(file.size()));
    }
    file = root.openNextFile();
  }
}

void downloadHTML(String hostname, String api, const char* fileName) {
  printlnMsg("Downloading init file...");
  NetworkClientSecure ncs;
  ncs.setInsecure();
  String getHeader = "GET " + api + " HTTP/1.0";
  String hostHeader = "Host: " + hostname;
  if (ncs.connect(hostname.c_str(), 443)) {
    ncs.println(getHeader);
    ncs.println(hostHeader);
    ncs.println("Connection: close");
    ncs.println();

    // Open file to save content
    File file = LittleFS.open(fileName, "w");
    if (!file) {
      Serial.println("Failed to open file for writing.");
      return;
    }

    // Skip headers and start saving body content
    bool headersEnded = false;
    while (ncs.connected()) {
      String line = ncs.readStringUntil('\n');
      if (line == "\r") {
        headersEnded = true;
        continue;
      }
      if (headersEnded) {
        file.print(line);  // Save the content into the file
      }
    }

    file.close();  // Close file after saving
    // Serial.println("HTML file downloaded and saved.");
    ncs.stop();
    printlnMsg("Download finished. You may check whether the file is in the file system using \"List File\" function");
    // currentChoice = 0;
    displayMenu();
  } else {
    Serial.println("Failed to connect to server.");
    // currentChoice = 0;
    displayMenu();
  }
}

void connectMQTT_WS(String& host, uint16_t port) {
  // Serial.println("connecting to host...");
  wsClient.disconnect();
  wsClient.begin(host, port, "/", "mqtt");  // "mqtt" is required
  wsClient.setReconnectInterval(2000);

  uint8_t retryCount = 0;
  // Serial.print("connecting to mqtt broker...");
  while (!wsMqttClient.connect(mac, "publicuser", "sharepassword") && retryCount < 4) {
    // Serial.print(".");
    delay(1000);
    if (!wsClient.isConnected()) {
      // Serial.println("WebSocketsClient disconnected");
    }
    retryCount++;
  }
  if (wsMqttClient.isConnected()) {
    String clientID = "ESP32Client-" + mac;
    self_pubTopic = topic_head + String("/devices/") + clientID + String("/pub");
    self_subTopic = topic_head + String("/devices/") + clientID + String("/sub");
    // JsonObject obj = doc.to<JsonObject>();
    DynamicJsonDocument doc(128);
    doc["msg"] = "startup";
    doc["id"] = clientID.c_str();
    String initMsg = "";
    int len = serializeJson(doc, initMsg);
    int status = wsMqttClient.publish(shared_pubTopic, initMsg);
    // client.subscribe(shared_subTopic.c_str());
    // client.subscribe(self_subTopic.c_str());
    // Serial.println(" connected!");
  }
}

#ifdef USE_VL53L0XControl
DeclareHandler(vl53l0xHandler, _ctrl, VL53L0XControl, {
  printMsg("value of VL53L0X: ");
  printlnMsg(_ctrl.measureDistance());
});
#endif

#ifdef USE_HTTPClientControl
DeclareHandler(httpClientCtrlEventHandler, _ctrl, HTTPClientControl, {
  if (_ctrl.isHeaderAvailable()) {
    String headerName = _ctrl.getHeaderName();
    if (headerName == "Content-Type") {
      printMsg("value of Content-Type is: ");
      printlnMsg(_ctrl.getHeaderValue());
      hasGotHeader = true;
      printMsg("Body is: ");
    }
  }

  if (_ctrl.isBodyIncomplete() && hasGotHeader) {
    // httpReceivedBody += _ctrl.getBody();
    printMsg(_ctrl.getBody());
  }

  if (_ctrl.isBodyAvailable() && hasGotHeader) {
    // httpReceivedBody += _ctrl.getBody();
    // printMsg("Body is: ");
    // printlnMsg(httpReceivedBody);
    printMsg(_ctrl.getBody());
    printlnMsg();
    hasGotHeader = false;
    currentChoice = 0;
    displayMenu();
  }
});
#endif

DeclareHandler(mpr121CtrlEventHandler, _ctrl, MPR121Control, {
  if (_ctrl.status & MPR121ControlEventHandler_TouchReleaseEvent) {

    for (uint8_t i = 0; i < 12; i++) {
      if (mpr121Ctrl.touchedTimeMS[i] != 0) {
        //implement touch event here.
        printMsg("touched i=");
        printMsg(i);
        printMsg(" at time=");
        printlnMsg(mpr121Ctrl.touchedTimeMS[i]);
      }

      if (mpr121Ctrl.releasedTimeMS[i] != 0) {
        //implement release event here
        printMsg("released i=");
        printMsg(i);
        printMsg(" at time=");
        printlnMsg(mpr121Ctrl.releasedTimeMS[i]);
      }
    }
  }
});

DeclareHandler(mpr121CtrlEventHandler_testMode, _ctrl, MPR121Control, {
  if (_ctrl.status & MPR121ControlEventHandler_TouchReleaseEvent) {

    for (uint8_t i = 0; i < 12; i++) {
      if (mpr121Ctrl.touchedTimeMS[i] != 0 && isAllFinish_testMode()) {
        //implement touch event here.
        printMsg("touched i=");
        printMsg(i);
        printMsg(" at time=");
        printlnMsg(mpr121Ctrl.touchedTimeMS[i]);

        if (displayType == 1) {
          sh1106Ctrl.getDisplay().display();
          sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
          sh1106Ctrl.getDisplay().setTextSize(1);
          sh1106Ctrl.getDisplay().setTextWrap(true);
          sh1106Ctrl.getDisplay().setCursor(0, 8);
          sh1106Ctrl.getDisplay().print("touched i=");
          sh1106Ctrl.getDisplay().print(i);
          sh1106Ctrl.getDisplay().print(" at time=");
          sh1106Ctrl.getDisplay().println(mpr121Ctrl.touchedTimeMS[i]);
          sh1106Ctrl.getDisplay().display();
        } else if (displayType == 2) {
          ssd1306Ctrl.getDisplay().display();
          ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
          ssd1306Ctrl.getDisplay().setTextSize(1);
          ssd1306Ctrl.getDisplay().setTextWrap(true);
          ssd1306Ctrl.getDisplay().setCursor(0, 8);
          ssd1306Ctrl.getDisplay().print("touched i=");
          ssd1306Ctrl.getDisplay().print(i);
          ssd1306Ctrl.getDisplay().print(" at time=");
          ssd1306Ctrl.getDisplay().println(mpr121Ctrl.touchedTimeMS[i]);
          ssd1306Ctrl.getDisplay().display();
        }

        switch (i) {
          case 0:
            {
              if (displayType == 1) {
                sh1106Ctrl.getDisplay().display();
                // sh1106Ctrl.getDisplay().clearDisplay();
                sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                sh1106Ctrl.getDisplay().setTextSize(1);
                // sh1106Ctrl.getDisplay().setTextColor(SH110X_WHITE);
                sh1106Ctrl.getDisplay().setTextWrap(true);
                sh1106Ctrl.getDisplay().setCursor(0, 0);
                sh1106Ctrl.getDisplay().println("Playing Sequence 0...");
                sh1106Ctrl.getDisplay().display();
              } else if (displayType == 2) {
                ssd1306Ctrl.getDisplay().display();
                // sh1106Ctrl.getDisplay().clearDisplay();
                ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                ssd1306Ctrl.getDisplay().setTextSize(1);
                // sh1106Ctrl.getDisplay().setTextColor(SH110X_WHITE);
                ssd1306Ctrl.getDisplay().setTextWrap(true);
                ssd1306Ctrl.getDisplay().setCursor(0, 0);
                ssd1306Ctrl.getDisplay().println("Playing Sequence 0...");
                ssd1306Ctrl.getDisplay().display();
              }

              addrLedCtrl.playRelTime(addrTarget, addrSeq0, 0, 1);
              mp3Ctrl.playRelTime(mp3Seq0, 0, 1);
              servoCtrl[0].playRelTime(servoSeq0, 0, 1);
              servoCtrl[1].playRelTime(servoSeq0, 0, 1);

              isPlayingSeq = true;
              playingSeq_testMode = 0;
              break;
            }

          case 1:
            {
              if (displayType == 1) {
                sh1106Ctrl.getDisplay().display();
                // sh1106Ctrl.getDisplay().clearDisplay();
                sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                sh1106Ctrl.getDisplay().setTextSize(1);
                // sh1106Ctrl.getDisplay().setTextColor(SH110X_WHITE);
                sh1106Ctrl.getDisplay().setTextWrap(true);
                sh1106Ctrl.getDisplay().setCursor(0, 0);
                sh1106Ctrl.getDisplay().println("Playing Sequence 1...");
                sh1106Ctrl.getDisplay().display();
              } else if (displayType == 2) {
                ssd1306Ctrl.getDisplay().display();
                ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                ssd1306Ctrl.getDisplay().setTextSize(1);
                ssd1306Ctrl.getDisplay().setTextWrap(true);
                ssd1306Ctrl.getDisplay().setCursor(0, 0);
                ssd1306Ctrl.getDisplay().println("Playing Sequence 1...");
                ssd1306Ctrl.getDisplay().display();
              }

              addrLedCtrl.playRelTime(addrTarget, addrSeq1, 0, 1);
              mp3Ctrl.playRelTime(mp3Seq1, 0, 1);
              servoCtrl[0].playRelTime(servoSeq1, 0, 1);
              servoCtrl[1].playRelTime(servoSeq1, 0, 1);

              isPlayingSeq = true;
              playingSeq_testMode = 1;
              break;
            }

          case 2:
            {
              if (displayType == 1) {
                sh1106Ctrl.getDisplay().display();
                // sh1106Ctrl.getDisplay().clearDisplay();
                sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                sh1106Ctrl.getDisplay().setTextSize(1);
                // sh1106Ctrl.getDisplay().setTextColor(SH110X_WHITE);
                sh1106Ctrl.getDisplay().setTextWrap(true);
                sh1106Ctrl.getDisplay().setCursor(0, 0);
                sh1106Ctrl.getDisplay().println("Playing Sequence 2...");
                sh1106Ctrl.getDisplay().display();
              } else if (displayType == 2) {
                ssd1306Ctrl.getDisplay().display();
                ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                ssd1306Ctrl.getDisplay().setTextSize(1);
                ssd1306Ctrl.getDisplay().setTextWrap(true);
                ssd1306Ctrl.getDisplay().setCursor(0, 0);
                ssd1306Ctrl.getDisplay().println("Playing Sequence 2...");
                ssd1306Ctrl.getDisplay().display();
              }

              addrLedCtrl.playRelTime(addrTarget, addrSeq2, 0, 1);
              mp3Ctrl.playRelTime(mp3Seq2, 0, 1);
              servoCtrl[0].playRelTime(servoSeq2, 0, 1);
              servoCtrl[1].playRelTime(servoSeq2, 0, 1);

              isPlayingSeq = true;
              playingSeq_testMode = 2;
              break;
            }

          case 3:
            {
              if (displayType == 1) {
                sh1106Ctrl.getDisplay().display();
                // sh1106Ctrl.getDisplay().clearDisplay();
                sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                sh1106Ctrl.getDisplay().setTextSize(1);
                // sh1106Ctrl.getDisplay().setTextColor(SH110X_WHITE);
                sh1106Ctrl.getDisplay().setTextWrap(true);
                sh1106Ctrl.getDisplay().setCursor(0, 0);
                sh1106Ctrl.getDisplay().println("Playing Sequence 3...");
                sh1106Ctrl.getDisplay().display();
              } else if (displayType == 2) {
                ssd1306Ctrl.getDisplay().display();
                ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
                ssd1306Ctrl.getDisplay().setTextSize(1);
                ssd1306Ctrl.getDisplay().setTextWrap(true);
                ssd1306Ctrl.getDisplay().setCursor(0, 0);
                ssd1306Ctrl.getDisplay().println("Playing Sequence 3...");
                ssd1306Ctrl.getDisplay().display();
              }
              addrLedCtrl.playRelTime(addrTarget, addrSeq3, 0, 1);
              mp3Ctrl.playRelTime(mp3Seq3, 0, 1);
              servoCtrl[0].playRelTime(servoSeq3, 0, 1);
              servoCtrl[1].playRelTime(servoSeq3, 0, 1);

              isPlayingSeq = true;
              playingSeq_testMode = 3;
              break;
            }
        }
      }

      if (mpr121Ctrl.releasedTimeMS[i] != 0) {
        // implement release event here
        printMsg("released i=");
        printMsg(i);
        printMsg(" at time=");
        printlnMsg(mpr121Ctrl.releasedTimeMS[i]);

        if (displayType == 1) {
          sh1106Ctrl.getDisplay().display();
          sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
          sh1106Ctrl.getDisplay().setTextSize(1);
          sh1106Ctrl.getDisplay().setTextWrap(true);
          sh1106Ctrl.getDisplay().setCursor(0, 8);
          sh1106Ctrl.getDisplay().print("released i=");
          sh1106Ctrl.getDisplay().print(i);
          sh1106Ctrl.getDisplay().print(" at time=");
          sh1106Ctrl.getDisplay().println(mpr121Ctrl.releasedTimeMS[i]);
          sh1106Ctrl.getDisplay().display();
        } else if (displayType == 2) {
          ssd1306Ctrl.getDisplay().display();
          ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
          ssd1306Ctrl.getDisplay().setTextSize(1);
          ssd1306Ctrl.getDisplay().setTextWrap(true);
          ssd1306Ctrl.getDisplay().setCursor(0, 8);
          ssd1306Ctrl.getDisplay().print("released i=");
          ssd1306Ctrl.getDisplay().print(i);
          ssd1306Ctrl.getDisplay().print(" at time=");
          ssd1306Ctrl.getDisplay().println(mpr121Ctrl.releasedTimeMS[i]);
          ssd1306Ctrl.getDisplay().display();
        }
      }
    }
  }
});

DeclareHandler(mpr121CtrlEventHandler_sequence, _ctrl, MPR121Control, {
  if (_ctrl.status & MPR121ControlEventHandler_TouchReleaseEvent) {

    for (uint8_t i = 0; i < 12; i++) {
      if (mpr121Ctrl.touchedTimeMS[i] != 0) {
        //implement touch event here.
        printMsg("touched i=");
        printMsg(i);
        printMsg(" at time=");
        printlnMsg(mpr121Ctrl.touchedTimeMS[i]);

        if (mpr121_seq_mode == 1) {
          Serial.println("current mpr121_seq_mode is 1");
          if (isAllFinish()) {
            if (mpr121_seq_mapping[i] != -1) {
              playSetSequence(mpr121_seq_mapping[i]);
            } else {
              playSetSequence(i);
            }
          }
        } else if (mpr121_seq_mode == 2) {
          Serial.println("current mpr121_seq_mode is 2");
          addrLedCtrl_0.abortAllSequences();
          if (mpr121_seq_mapping[i] != -1) {
            playSetSequence(mpr121_seq_mapping[i]);
          } else {
            playSetSequence(i);
          }
        }
      }

      if (mpr121Ctrl.releasedTimeMS[i] != 0) {
        //implement release event here
        printMsg("released i=");
        printMsg(i);
        printMsg(" at time=");
        printlnMsg(mpr121Ctrl.releasedTimeMS[i]);
      }
    }
  }
});

DeclareHandler(handler, _ctrl, IOControl, {
  if (playingSeq_testMode != -1) {
    if (isAllFinish_testMode()) {
      if (displayType == 1) {
        sh1106Ctrl.getDisplay().display();
        sh1106Ctrl.getDisplay().setTextColor(WHITE, BLACK);
        sh1106Ctrl.getDisplay().setTextSize(1);
        sh1106Ctrl.getDisplay().setTextWrap(true);
        sh1106Ctrl.getDisplay().setCursor(0, 0);
        sh1106Ctrl.getDisplay().print("Sequence ");
        sh1106Ctrl.getDisplay().print(playingSeq_testMode);
        sh1106Ctrl.getDisplay().println(" ended     ");
        sh1106Ctrl.getDisplay().display();
      } else if (displayType == 2) {
        ssd1306Ctrl.getDisplay().display();
        ssd1306Ctrl.getDisplay().setTextColor(WHITE, BLACK);
        ssd1306Ctrl.getDisplay().setTextSize(1);
        ssd1306Ctrl.getDisplay().setTextWrap(true);
        ssd1306Ctrl.getDisplay().setCursor(0, 0);
        ssd1306Ctrl.getDisplay().print("Sequence ");
        ssd1306Ctrl.getDisplay().print(playingSeq_testMode);
        ssd1306Ctrl.getDisplay().println(" ended     ");
        ssd1306Ctrl.getDisplay().display();
      }
      playingSeq_testMode = -1;
    }
  }

  if (isPlayingSeq) {
    playSeqCount++;
    if (playSeqCount >= 1000) {
      isPlayingSeq = false;
      playSeqCount = 0;
    }
  }

#ifdef USE_NTP
  if (shouldDisplayTime) {
    if (displayTimeCount > 0) {
      displayTimeCount--;
      if (displayTimeCount == 0) {
        if (displayType == 1) {
          sh1106Ctrl.getDisplay().setCursor(0, 0);
          sh1106Ctrl.getDisplay().println(timeClient.getFormattedTime());
          sh1106Ctrl.getDisplay().display();
        } else if (displayType == 2) {
          ssd1306Ctrl.getDisplay().setCursor(0, 0);
          ssd1306Ctrl.getDisplay().println(timeClient.getFormattedTime());
          ssd1306Ctrl.getDisplay().display();
        }
      }
    }
  }
#endif

#ifdef USE_HTTPClientControl
  if (shouldDisplayTime && wifiCtrl.isConnected()) {
    if (displayTimeCount > 0) {
      displayTimeCount--;
      if (displayTimeCount == 0) {
        httpClientCtrl.setInsecure();
        httpClientCtrl.connect("data.weather.gov.hk", 443);
        httpClientCtrl.get("/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en");
        httpClientCtrl.setReqHeaderConnClose();
        httpClientCtrl.sendRequest();
        // Serial.println("?????????");
        displayTimeCount = 500;
      }
    }
  }
#endif

  if (wsDisplayMenuCountDown > 0) {
    wsDisplayMenuCountDown--;
    if (wsDisplayMenuCountDown == 0) {
      displayMenu(true);
    }
  }
  if (_ctrl.isSchedulerTimeEvent()) {
    if (Serial.available() > 0) {
      String input = Serial.readStringUntil('\n');
      printMsg("You entered: ");
      printlnMsg(input);
      if (waitingUserInput) {
        waitingUserInput = false;
        funcPtr_testcase(input);
        if (!waitingUserInput) {
          funcPtr_testcase = nullptr;
        }
      } else if (addr_waitingSecondInput) {
        handleSecondInput_addrLed(input);
        addr_waitingSecondInput = false;
        addr_firstInput = 0;
      } else if (http_waitingSecondInput) {
#ifdef USE_HTTPClientControl
        handleSecondInput_http(input);
        http_waitingSecondInput = false;
        http_firstInput = 0;
#endif
      } else if (mqtt_waitingSecondInput) {
        handleSecondInput_mqtt(input);
        // mqtt_waitingSecondInput = false;
        // mqtt_firstInput = 0;
      } else if (mqtt_ws_waitingSecondInput) {
        handleSecondInput_mqtt_ws(input);
        // mqtt_ws_waitingSecondInput = false;
        // mqtt_ws_firstInput = 0;
      } else if (sequence_waitingSecondInput) {
        handleSecondInput_sequence(input);
      } else if (mp3_waitingSecondInput) {
        handleSecondInput_dfPlayer(input);
      } else {
        handleMsg(input);
      }
    }
    if (displayType == 1) {
      if ((currentChoice == 3 && sh1106Ready) || (currentChoice == 20 && sh1106Ready)) {
        drawBitMap_sh1106();
      }
    }

    if (displayType == 2) {
      if ((currentChoice == 4 && ssd1306Ready) || (currentChoice == 20 && ssd1306Ready)) {
        drawBitMap_ssd1306();
      }
    }
  }
});

DeclareHandler(adcHandler, _ctrl, ADCControl, {
  // if (_ctrl.isSchedulerTimeEvent())
  //   Serial.println("BinOutControl - SchedulerTimerEvent");
  int val0 = _ctrl.read();
  printMsg("time=");
  printMsg(_ctrl.handlerCurrentMillis);
  printMsg(" adc0=");
  printlnMsg(val0);
});

DeclareHandler(binInHandler, _ctrl, BinInControl, {
  if (_ctrl.isBinInTriggered()) {
    printMsg("event time=");
    printMsg(_ctrl.getInterruptTime());
    if (_ctrl.getInterruptState())
      printlnMsg(" from LOW to HIGH");
    else
      printlnMsg(" from HIGH to LOW");
  }
});
//========================================================



void streamStaticFSFile(String filename, String contentType) {
  File targetFile = LittleFS.open(filename, "r");
  if (!targetFile) {  //  file not found
    server.send(200, "text/html", "<html><body>" + filename + " not found </body></html>");
  } else {
    size_t sent = server.streamFile(targetFile, contentType);  // Send it to the client
    targetFile.close();
  }
}

//=================================================================
// Web: /setting
//=================================================================
void web_debugPage() {
  streamStaticFSFile("/esp_serial_monitor.html", "text/html");
}



void webSocketServerEvent(uint8_t num, WStype_t wtype, uint8_t* payload, size_t length) {

  //Serial.printf("[%u] get Message: %s\r\n", num, payload);
  switch (wtype) {
    case WStype_DISCONNECTED:
      Serial.printf("Websocket [%u] Disconnected!\n", num);
      isWsConnected = false;
      break;

    case WStype_CONNECTED:
      {
        // displayMenu();
        wsDisplayMenuCountDown = 200;
        isWsConnected = true;
        IPAddress ip = webSocketServer->remoteIP(num);
        Serial.printf("Websocket [%u] Connected from %d.%d.%d.%d url: %s\r\n", num, ip[0], ip[1], ip[2], ip[3], payload);
      }

      break;

    case WStype_TEXT:
      {
        DynamicJsonDocument doc(1024);  //Memory pool
        DeserializationError error = deserializeJson(doc, payload);
        if (error) {
          Serial.println("Failed to read payload");
          switch (error.code()) {
            case DeserializationError::InvalidInput:
              {
                Serial.print(F("Invalid input!"));
                DynamicJsonDocument errDoc(128);
                errDoc["msg"] = "deserializationErr";
                errDoc["err"] = "invalidInput";
                String errStr = "";
                serializeJson(errDoc, errStr);
                webSocketServer->broadcastTXT(errStr);
                break;
              }
            case DeserializationError::NoMemory:
              {
                Serial.print(F("Not enough memory"));
                DynamicJsonDocument errDoc(128);
                errDoc["msg"] = "deserializationErr";
                errDoc["err"] = "noMemory";
                String errStr = "";
                serializeJson(errDoc, errStr);
                webSocketServer->broadcastTXT(errStr);
                break;
              }
            default:
              {
                Serial.print(F("Deserialization failed"));
                break;
              }
          }
        } else {  //message is deserialized successfully
          // Serial.print("Message received: ");
          serializeJson(doc, Serial);
          Serial.println("");
          String input = doc["input"].as<const char*>();
          printMsg("You entered: ");
          printlnMsg(input);

          if (waitingUserInput) {
            funcPtr_testcase(input);
            waitingUserInput = false;
            funcPtr_testcase = nullptr;
            return;
          } else if (addr_waitingSecondInput) {
            handleSecondInput_addrLed(input);
            addr_waitingSecondInput = false;
            addr_firstInput = 0;
            return;
          } else if (http_waitingSecondInput) {
#ifdef USE_HTTPClientControl
            handleSecondInput_http(input);
            http_waitingSecondInput = false;
            http_firstInput = 0;
#endif
            return;
          } else if (mqtt_waitingSecondInput) {
            handleSecondInput_mqtt(input);
            // mqtt_waitingSecondInput = false;
            // mqtt_firstInput = 0;
            return;
          } else if (mqtt_ws_waitingSecondInput) {
            handleSecondInput_mqtt_ws(input);
            // mqtt_ws_waitingSecondInput = false;
            // mqtt_ws_firstInput = 0;
            return;
          } else if (sequence_waitingSecondInput) {
            handleSecondInput_sequence(input);
            return;
          } else if (mp3_waitingSecondInput) {
            handleSecondInput_dfPlayer(input);
            return;
          }
          // String replyHead = "Message received: ";
          // String reply = replyHead + input;
          // webSocketServer->broadcastTXT(reply);
          handleMsg(input);
          //String name = doc["name"].as<const char*>();
        }
        break;
      }  //end of WStype_TEXT
  }
}

#ifdef USE_UltraSonicControl
DeclareHandler(ultraSonicCtrlHandler, _ioCtrl, UltraSonicControl, {
  Serial.print("ultrasonic sensor detected distance = ");
  Serial.print(_ioCtrl.getDistance());
  Serial.println(" cm");
});
#endif

void setup() {
  // put your setup code here, to run once:
  IO_Control.begin();

  Serial.begin(115200);

  Serial.println("chip started: IDDBoardTest_2025_20260120");

  if (!LittleFS.begin()) {
    Serial.println("LittleFS mount failed. Now create partition for LittleFS");
    LittleFS.begin(true);
  }

  File wifiFile = LittleFS.open("/wifi.json", "r");  // {"wifi1":{"ssid":"_IOT Roaming", "pass":"iot213213213"},"wifi2":{"ssid":"_IOT Roaming2", "pass":"iot213213213"}, "wifi3":{"ssid":"_IOT Roaming3", "pass":"iot213213213"}}
  if (wifiFile) {
    DynamicJsonDocument wifiDoc(256);
    DeserializationError err = deserializeJson(wifiDoc, wifiFile);
    wifiFile.close();
    if (!err) {
      if (wifiDoc.containsKey("wifi1")) {
        String ssid1 = wifiDoc["wifi1"]["ssid"].as<const char*>();
        String password1 = wifiDoc["wifi1"]["pass"].as<const char*>();
        err_t err = wifiCtrl.init(WiFiControlWiFiModeAPSTA);

        if (err != Control_OK) {
          printMsg("Error: Fail to initialize WiFiControl. Reason is: ");
          printlnMsg(err);
          wifiCtrl.release();
          return;
        } else {
          wifiCtrl.connect(ssid1, password1);
          printMsg("Connecting to WiFi ");
          printMsg(ssid1);
          int retryCount = 0;
          while (!wifiCtrl.isConnected() && retryCount < 3) {
            printMsg(".");
            retryCount++;
            delay(1000);
          }
          if (wifiCtrl.isConnected()) {
            printlnMsg();
            printlnMsg("WiFi is connected successfully");
            printMsg("IP Address is: ");
            IPAddress ip = WiFi.localIP();
            String ip_str = String(ip[0]) + "." + String(ip[1]) + "." + String(ip[2]) + "." + String(ip[3]);
            printlnMsg(ip_str);
          } else {
            printlnMsg();
            printlnMsg("Failed to connect WiFi. Please retry.");
            wifiCtrl.release();
          }
        }
      }
    }
  }

  File displayTypeFile = LittleFS.open("/display.json", "r");
  if (displayTypeFile) {
    JsonDocument displayDoc;
    DeserializationError displayDsErr = deserializeJson(displayDoc, displayTypeFile);
    if (!displayDsErr) {
      displayType = displayDoc["type"].as<uint8_t>();
    }
    displayTypeFile.close();
  }

  for (uint8_t i = 0; i < 12; i++) {
    mpr121_seq_mapping[i] = -1;
  }

  loadSequenceSetting();


  displayMenu();  // Display menu initially

  WiFi.mode(WIFI_AP_STA);
  // WiFi.begin(wifi_ssid, wifi_pass);

  // client.setServer(mqtt_server, mqtt_port);

  client.setCallback(callback);

  mac = WiFi.macAddress();
  mac.replace(":", "");
  String ssid = "Device-" + mac;
  WiFi.softAP(ssid, "12345678");

  server.onNotFound([]() {
    if (server.method() == HTTP_OPTIONS) {
      server.sendHeader("Access-Control-Allow-Origin", "*");
      server.sendHeader("Access-Control-Allow-Methods", "POST, GET, OPTIONS");
      server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
      server.send(200);
    } else {
      server.send(404, "text/plain", "Not found");
    }
  });

  server.on("/", web_debugPage);

  server.begin();

  webSocketServer->begin();

  webSocketServer->onEvent(webSocketServerEvent);

  wsMqttClient.begin(wsClient);

  // subscribe callback which is called when every packet has come
  wsMqttClient.subscribe([](const String& topic, const String& payload, const size_t size) {
    printMsg("Message arrived on topic: ");
    printMsg(topic);
    printlnMsg(". Message: ");
    printlnMsg(payload);

    if (String(topic) == mqtt_topic) {
      DynamicJsonDocument doc(512);
      DeserializationError error = deserializeJson(doc, payload);
      String command = doc["command"].as<const char*>();
    }
  });

  IO_Control.enableScheduler(0, 10, handler);

  servoSeq0.addMoveFromToAngle(2000, 55, 110, servoCtrl[0]);
  servoSeq0.addMoveFromToAngle(2000, 110, 55, servoCtrl[0]);
  servoSeq0.addMoveFromToAngle(2000, 55, 110, servoCtrl[0]);
  servoSeq0.addMoveFromToAngle(2000, 110, 55, servoCtrl[0]);
  servoSeq0.addMoveFromToAngle(2000, 55, 110, servoCtrl[0]);

  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 55, 110, servoCtrl[0]);
  servoSeq1.addMoveFromToAngle(500, 110, 55, servoCtrl[0]);

  servoSeq2.addMoveFromToAngle(5000, 55, 110, servoCtrl[0]);
  servoSeq2.addMoveFromToAngle(5000, 110, 55, servoCtrl[0]);

  servoSeq3.addMoveFromToAngle(10000, 55, 110, servoCtrl[0]);

  for (int i = 0; i < 68; i++) {
    addrTarget.push_back(i);
  }

  addrSeq0.addSetRGB(2000, 255, 0, 0);
  addrSeq0.addSetRGB(2000, 0, 255, 0);
  addrSeq0.addSetRGB(2000, 0, 0, 255);
  addrSeq0.addSetRGB(2000, 255, 255, 0);
  addrSeq0.addSetRGB(2000, 0, 255, 255);
  // addrSeq0.addInterpolateRGB(2000, 255, 255, 0, 0, 0, 255);

  // addrSeq1.addSetHSV(1000, 0, 80, 80);
  addrSeq1.addInterpolateHSV(2000, 0, 80, 80, 350, 80, 80);
  addrSeq1.addInterpolateHSV(2000, 350, 80, 80, 0, 80, 80);
  addrSeq1.addInterpolateHSV(2000, 0, 80, 80, 350, 80, 80);
  addrSeq1.addInterpolateHSV(2000, 350, 80, 80, 0, 80, 80);
  addrSeq1.addInterpolateHSV(2000, 0, 80, 80, 350, 80, 80);

  addrSeq2.addSetHSV(1000, 0, 50, 50);
  addrSeq2.addSetHSV(1000, 30, 50, 50);
  addrSeq2.addSetHSV(1000, 60, 50, 50);
  addrSeq2.addSetHSV(1000, 90, 50, 50);
  addrSeq2.addSetHSV(1000, 120, 50, 50);
  addrSeq2.addSetHSV(1000, 150, 50, 50);
  addrSeq2.addSetHSV(1000, 180, 50, 50);
  addrSeq2.addSetHSV(1000, 210, 50, 50);
  addrSeq2.addSetHSV(1000, 240, 50, 50);
  addrSeq2.addSetHSV(1000, 270, 50, 50);
  // addrSeq2.addInterpolateHSV(2000, 10, 80, 80, 270, 50, 80);

  addrSeq3.addInterpolateHSV(10000, 0, 60, 60, 350, 60, 60);

  // mp3Seq0.addCommand(1, 30, 2500, true);
  // mp3Seq0.addCommand(2, 30, 2500, true);
  // mp3Seq0.addCommand(3, 30, 2500, true);
  // mp3Seq0.addCommand(1, 30, 2500, true);

  mp3Seq0.addCommand(1, 30, 10000, true, 2000, 1000);

  mp3Seq1.addCommand(3, 30, 5000, true);
  mp3Seq1.addCommand(2, 30, 5000, true);

  mp3Seq2.addCommand(2, 30, 5000, true);
  mp3Seq2.addCommand(1, 30, 2500, true);
  mp3Seq2.addCommand(3, 30, 2500, true);

  mp3Seq3.addCommand(1, 30, 3000, true);
  mp3Seq3.addCommand(2, 30, 2000, true);
  mp3Seq3.addCommand(1, 30, 5000, true);

// bootButtonCtrl.init(9, INPUT);

// bootButtonCtrl.enableScheduler(0, 10, bootButtonHandler);
// bootButtonCtrl.enableInterrupt(CHANGE);
#ifdef USE_NTP
  timeClient.setTimeOffset(28800);
#endif
}

void loop() {
  // put your main code here, to run repeatedly:
  IO_Control.execute();

  server.handleClient();

  webSocketServer->loop();

  if (shouldMqttConnect) {
    if (!client.connected()) {
      reconnect();
    } else {
      client.loop();
    }
  }

  if (shouldMqttConnect_WS) {
    if (!wsMqttClient.isConnected()) {
      // Serial.println("Calling connectMQTT_WS in loop");
      connectMQTT_WS(brokerAddr, brokerPort);
    } else {
      wsMqttClient.update();
    }
  }

#ifdef USE_NTP
  if (wifiCtrl.isConnected()) {
    timeClient.update();
  }
#endif

  // uint32_t currentMillis = millis();
  // if (currentMillis - previousMillis > 2000) {
  //   Serial.print("httpReceivedBody is: ");
  //   Serial.println(httpReceivedBody);
  //   previousMillis = currentMillis;
  // }
}

void callback(char* topic, byte* message, unsigned int length) {
  printMsg("Message arrived on topic: ");
  printMsg(topic);
  printlnMsg(". Message: ");
  String messageTemp;

  for (int i = 0; i < length; i++) {
    messageTemp += (char)message[i];
  }

  Serial.println(messageTemp);

  if (String(topic) == mqtt_topic) {
    DynamicJsonDocument doc(512);
    DeserializationError error = deserializeJson(doc, messageTemp);
    String command = doc["command"].as<const char*>();
  }
}

void reconnect() {
  // Loop until we're reconnected
  int retryCount = 3;
  bool isReconnectSuccess = false;
  while (!client.connected() && retryCount > 0) {
    printMsg("Attempting MQTT connection to ");
    printMsg(brokerAddr);
    printMsg(" port");
    printlnMsg(brokerPort);
    // Attempt to connect
    if (client.connect(mac.c_str(), "publicuser", "sharepassword")) {
      String clientID = "ESP32Client-" + mac;
      self_pubTopic = topic_head + String("/devices/") + clientID + String("/pub");
      self_subTopic = topic_head + String("/devices/") + clientID + String("/sub");
      // JsonObject obj = doc.to<JsonObject>();
      DynamicJsonDocument doc(128);
      doc["msg"] = "startup";
      doc["id"] = clientID.c_str();
      String initMsg = "";
      int len = serializeJson(doc, initMsg);
      int status = client.publish(shared_pubTopic.c_str(), initMsg.c_str());
      // client.subscribe(shared_subTopic.c_str());
      // client.subscribe(self_subTopic.c_str());

      isReconnectSuccess = true;
      printlnMsg("connected");
      displayMenu_mqtt();
      // Subscribe
      // client.subscribe(mqtt_topic.c_str());
    } else {
      printMsg("failed, rc=");
      printMsg(client.state());
      printlnMsg(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
    retryCount--;
  }

  if (!isReconnectSuccess) {
    printlnMsg("Failed to connect to MQTT server. Please retry later.");
    currentChoice = 0;
    client.disconnect();
    shouldMqttConnect = false;
    displayMenu();
  }
}



void displayMenu_addrLed() {
  printlnMsg();
  printlnMsg("Menu:");
  printlnMsg("1: setRGB");
  printlnMsg("2: setHSV");
  printlnMsg("3: Interpolate RGB");
  printlnMsg("4: Interpolate HSV");
  printlnMsg("x: leave AddrLEDControl Menu");
  printlnMsg("Enter your choice:");
}

void displayMenu_servo() {
  printlnMsg();
  printlnMsg("Menu:");
  printMsg("Enter angle for # of servo=");
  printMsg(noOfActiveServo);
  printlnMsg(" OR enter 'x' to go back main menu");
}

#ifdef USE_LiquidCrystal
void displayMenu_lcd1602() {
  printlnMsg();
  printlnMsg("Menu:");
  printlnMsg("Enter text to be printed on LCD1602 OR enter 'x' to go back main menu");
}
#endif

void displayMenu_tone() {
  printlnMsg();
  printlnMsg("Menu:");
  printMsg("Enter frequency & duty (max=");
  printMsg(toneCtrl.getMaxDuty());
  printlnMsg(") & duration (in ms) OR enter 'x' to go back main menu");
}

void displayMenu_pwm() {
  printlnMsg();
  printlnMsg("Menu:");
  printMsg("Enter PWM value (max=");
  printMsg(pwmCtrl[0].getMaxDuty());
  printMsg(") and for # of pins=");
  printMsg(noOfActivePWM);
  printlnMsg(" OR enter 'x' to go back main menu");
}

void displayMenu_adc() {
  printlnMsg();
  printlnMsg("Showing value of ADC. Enter 'x' to leave and go back main menu");
}

void displayMenu_gpioIn() {
  printlnMsg();
  printlnMsg("The value of selected pin will be shown when input is received. Enter 'x' to leave and go back main menu");
}

void displayMenu_gpioOut() {
  printlnMsg();
  printlnMsg("Menu:");
  printlnMsg("Enter value (0 or 1) OR enter 'x' to go back main menu");
}

void displayMenu_http() {
  printlnMsg();
  printlnMsg("Menu:");
  printlnMsg("1: GET");
  printlnMsg("2: POST");
  printlnMsg("x: leave HTTPClientControl Menu");
  printlnMsg("Enter your choice:");
}

void displayMenu_mqtt() {
  printlnMsg();
  printlnMsg("Menu:");
  printlnMsg("1: Subscribe");
  printlnMsg("2: Publish");
  printlnMsg("x: leave MQTT Menu");
  printlnMsg("Enter your choice:");
}

void displayMenu_mpr121() {
  printlnMsg();
  printlnMsg("Touch and Release MPR121 to see the result. Enter 'x' to leave MPR121 testing.");
}

void displayMenu_testMode() {
  printlnMsg();
  printlnMsg("Touch and Release MPR121 to play different sequences.");
}

void displayMenu_sequence() {
  printlnMsg();
  printlnMsg("Select action: ");
  printlnMsg("1: Play sequence with MPR121");
  printlnMsg("2: Change setting");
  printlnMsg("x: go back main menu");
}

void displayMenu_sequence_noMPR121() {
  printlnMsg("\n");
  printlnMsg("Enter index of sequence set to be played OR enter \"x\" to go back sequence menu");
}

void displayMenu_dfPlayer() {
  printlnMsg();
  printlnMsg("Menu:");
  // printlnMsg("Enter the \"index\" of the MP3 file to be played & \"volume\" (optional, 0 to 30, default is 30, separated by comma) OR enter \"x\" to go back main menu:");
  printlnMsg("1: play MP3");
  printlnMsg("2: set volume");
  printlnMsg("3: advance");
  printlnMsg("x: leave MP3 menu");
}

void displaySecondMenu_dfPlayer() {
  printlnMsg();
  if (mp3_firstInput == 1) {
    printlnMsg("Enter the \"index\" of the MP3 file to be played OR enter \"x\" to go back MP3 menu");
  } else if (mp3_firstInput == 2) {
    printlnMsg("Enter the \"volume\" to set OR enter \"x\" to go back MP3 menu");
  } else if (mp3_firstInput == 3) {
    printlnMsg("Enter the \"index\", \"volume\", \"duration\", \"loop after end (true OR false)\", \"fade in time\"(optional), \"fade out time\"(optional) (separated in comma) OR enter \"x\" to go back MP3 menu:");
  }
}

#ifdef USE_VL53L0XControl
void displayMenu_vl53l0x() {
  printlnMsg();
  printlnMsg("Values of VL53L0X will be displayed. Enter 'x' to go back main menu.");
}
#endif

#ifdef USE_UltraSonicControl
void displayMenu_ultrasonic() {
  printlnMsg();
  printlnMsg("Values of ultrasonic sensor will be displayed. Enter 'x' to go back main menu.");
}
#endif

void testcase_listFile() {
  listDir("/", 1);
  displayMenu();
}

void testcase_downloadInitFile() {
  if (!wifiCtrl.isInit()) {
    printlnMsg("WiFiControl is not initialized. Please use function 12 to connect WiFi first.");
    // currentChoice = 0;
    displayMenu();
    return;
  } else {
    if (!wifiCtrl.isConnected()) {
      printlnMsg("WiFi is not connected. Cannot download file.");
      // currentChoice = 0;
      displayMenu();
      return;
    }
  }

  //downloadHTML("www.designandmake.org", "/download/attachments/260375561/esp_serial_monitor.html?version=1&modificationDate=1738818338105&api=v2&download=true", "/esp_serial_monitor.html");
  downloadHTML("www.designandmake.org", "/display/shareit/260375561/OUT37c1ce2750af45f88661082b48f749ceMCL/esp_serial_monitor_html?version=1", "/esp_serial_monitor.html");
}

void testcase_mpr121() {
  // Implement Test Case 1 logic here
  printlnMsg("\nRunning testcase_mpr121...");
  err_t err;

  //err = i2cCtrl.init(0, 6, 10);
  err = i2cCtrl.init(0, 10, 6);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize I2CMasterControl. Reason is: ");
    switch (err) {
      case I2CMasterControl_InvalidI2CIndex:
        printlnMsg("I2C index is invalid. Only 0 is allowed");
        break;
      case I2CMasterControl_InvalidSCL:
        printlnMsg("SCL pin is invalid");
        break;
      case I2CMasterControl_InvalidSDA:
        printlnMsg("SDA pin is invalid");
        break;
      case I2CMasterControl_InvalidClkFreq:
        printlnMsg("Clock Frequency is invalid");
        break;
    }
  } else {
    printlnMsg("I2CMasterControl is initialized successfully");
  }

  err = mpr121Ctrl.init(i2cCtrl, 0x5A, 7, 1000, 10, mpr121CtrlEventHandler);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize MPR121Control. Reason is: ");
    switch (err) {
      case MPR121Control_I2CNotActive:
        printlnMsg("I2CMasterControl is not active");
        break;
      case Control_NullEventHandler:
        printlnMsg("MPR121Control Event Handler is null");
        break;
      case MPR121Control_I2CAddrError:
        printlnMsg("I2C address is invalid for MPR121Control");
        break;
      case MPR121Control_IRQInvalid:
        printlnMsg("IRQ pin is invalid for MPR121Control");
        break;
    }
  } else {
    printlnMsg("MPR121Control is initialized successfully");
    displayMenu_mpr121();
  }
}

void testcase_testMode() {
  // Implement Test Case 1 logic here
  bool isAllSuccess = true;
  printlnMsg("\nRunning testcase_testMode...");
  err_t err;

  //err = i2cCtrl.init(0, 6, 10);
  err = i2cCtrl.init(0, 10, 6);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize I2CMasterControl. Reason is: ");
    switch (err) {
      case I2CMasterControl_InvalidI2CIndex:
        printlnMsg("I2C index is invalid. Only 0 is allowed");
        break;
      case I2CMasterControl_InvalidSCL:
        printlnMsg("SCL pin is invalid");
        break;
      case I2CMasterControl_InvalidSDA:
        printlnMsg("SDA pin is invalid");
        break;
      case I2CMasterControl_InvalidClkFreq:
        printlnMsg("Clock Frequency is invalid");
        break;
    }

    printlnMsg();

    isAllSuccess = false;
  } else {
    printlnMsg("I2CMasterControl is initialized successfully");
  }

  err = mpr121Ctrl.init(i2cCtrl, 0x5A, 7, 1000, 10, mpr121CtrlEventHandler_testMode);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize MPR121Control. Reason is: ");
    switch (err) {
      case MPR121Control_I2CNotActive:
        printlnMsg("I2CMasterControl is not active");
        break;
      case Control_NullEventHandler:
        printlnMsg("MPR121Control Event Handler is null");
        break;
      case MPR121Control_I2CAddrError:
        printlnMsg("I2C address is invalid for MPR121Control");
        break;
      case MPR121Control_IRQInvalid:
        printlnMsg("IRQ pin is invalid for MPR121Control");
        break;
    }

    printlnMsg();

    isAllSuccess = false;
  } else {
    printlnMsg("MPR121Control is initialized successfully");
  }
  // printlnMsg("\nRunning testcase_neopixel...");
  err = addrLedCtrl.init(5, 68, true);  //just need to test whether it can light up. Do not need sequence function.

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize AddrLEDControl. Reason is: ");
    switch (err) {
      case AddrLEDControl_InvalidPinIndex:
        printlnMsg("Pin is invalid");
        break;
    }

    printlnMsg();
    // return;
    isAllSuccess = false;
  } else {
    // printlnMsg("AddrLEDControl is requested successfully");
    addrLedCtrl.enableScheduler(0, 100, nullptr);
  }

  // printlnMsg("Running testcase_servo...");
  err = servoCtrl[0].init(12, true);
  if (err != Control_OK) {
    // isAllServoInitSuccessful = false;
    printMsg("Error: Fail to initialize ServoControl. Reason is: ");
    switch (err) {
      case ServoControl_InvalidPinIndex:
        printlnMsg("Pin is invalid");
        break;
    }

    printlnMsg();
    isAllSuccess = false;
  } else {
    servoCtrl[0].setAngle(55);
    servoCtrl[0].enableScheduler(0, 100, nullptr);
  }

  err = servoCtrl[1].init(13, true);
  if (err != Control_OK) {
    // isAllServoInitSuccessful = false;
    printMsg("Error: Fail to initialize ServoControl. Reason is: ");
    switch (err) {
      case ServoControl_InvalidPinIndex:
        printlnMsg("Pin is invalid");
        break;
    }
    printlnMsg();
    isAllSuccess = false;
  } else {
    servoCtrl[1].setAngle(55);
    servoCtrl[1].enableScheduler(0, 100, nullptr);
  }

  err = hwUartCtrl.init(1, 19, 18, -1, -1, 9600, UART_8N1);

  if (err != Control_OK) {
    Serial.print("Failed to init UARTControl (HW). Reason is: ");
    switch (err) {
      case Control_ActiveAlready:
        {
          Serial.println("UARTControl is active already");
          break;
        }
    }
  }

  err = mp3Ctrl.init(hwUartCtrl, 8);
  if (err != Control_OK) {
    Serial.print("Failed to init MP3Control. Reason is: ");
    switch (err) {
      case Control_ActiveAlready:
        {
          printlnMsg("MP3Control is active already");
          break;
        }
      case DFPlayerMP3Control_PlayerFailedToBegin:
        {
          printlnMsg("DFPlayer failed to begin");
          break;
        }
    }

    printlnMsg();
    isAllSuccess = false;
  } else {
    mp3Ctrl.getPlayer().volume(mp3_currentVolume);
    mp3Ctrl.enableScheduler(0, 200, nullptr);
  }

  if (displayType == 1) {
    err = sh1106Ctrl.init(i2cCtrl, 0X3C, 128, 64, -1);

    if (err != Control_OK) {
      printMsg("Error: Fail to initialize SH1106Control. Reason is: ");
      switch (err) {
        case SH1106Control_I2CNotActive:
          printlnMsg("I2CMasterControl is not active");
          break;
        case SH1106Control_I2CAddrError:
          printlnMsg("I2C address is invalid for SH1106Control");
          break;
      }
      printlnMsg();
      isAllSuccess = false;
    } else {
      printlnMsg("Successfully request sh1106Ctrl");
      sh1106Ctrl.getDisplay().display();
      sh1106Ctrl.getDisplay().clearDisplay();
      sh1106Ctrl.getDisplay().setTextSize(1);
      sh1106Ctrl.getDisplay().setTextColor(WHITE);
      sh1106Ctrl.getDisplay().setTextWrap(true);
      sh1106Ctrl.getDisplay().setCursor(0, 0);
      sh1106Ctrl.getDisplay().println("Successfully request sh1106Ctrl");
      sh1106Ctrl.getDisplay().display();
      sh1106Ctrl.getDisplay().clearDisplay();
      // printlnMsg("Enter 'x' to go back to Menu");
    }
  } else if (displayType == 2) {
    err = ssd1306Ctrl.init(i2cCtrl, 0X3C, 128, 64, -1);
    if (err != Control_OK) {
      printMsg("Error: Fail to initialize SSD1306Control. Reason is: ");
      switch (err) {
        case SSD1306Control_I2CNotActive:
          printlnMsg("I2CMasterControl is not active");
          break;
        case SSD1306Control_I2CAddrError:
          printlnMsg("I2C address is invalid for SH1106Control");
          break;
      }
      isAllSuccess = false;
    } else {
      printlnMsg("Successfully request ssd1306Ctrl");
      ssd1306Ctrl.getDisplay().display();
      ssd1306Ctrl.getDisplay().clearDisplay();
      ssd1306Ctrl.getDisplay().setTextSize(1);
      ssd1306Ctrl.getDisplay().setTextColor(WHITE);
      ssd1306Ctrl.getDisplay().setTextWrap(true);
      ssd1306Ctrl.getDisplay().setCursor(0, 0);
      ssd1306Ctrl.getDisplay().println("Successfully request sh1106Ctrl");
      ssd1306Ctrl.getDisplay().display();
      ssd1306Ctrl.getDisplay().clearDisplay();
    }
  }
  if (!isAllSuccess) {
    currentChoice = 0;
    handleInput_testMode("x");
    return;
  }
#ifdef USE_HTTPClientControl
  if (wifiCtrl.isConnected()) {
    // timeClient.begin();
    httpClientCtrl.init(wifiCtrl, true, 1024);
    httpClientCtrl.enableScheduler(0, 10, httpTestModeHandler);
    displayTimeCount = 500;
    shouldDisplayTime = true;
  }
#endif
  if (displayType == 1) {
    sh1106Ctrl.getDisplay().display();
    sh1106Ctrl.getDisplay().clearDisplay();
    sh1106Ctrl.getDisplay().setTextSize(1);
    sh1106Ctrl.getDisplay().setTextColor(WHITE);
    sh1106Ctrl.getDisplay().setTextWrap(true);
    sh1106Ctrl.getDisplay().setCursor(0, 0);
    sh1106Ctrl.getDisplay().println("Test Mode Activated");
    sh1106Ctrl.getDisplay().display();
  } else if (displayType == 2) {
    ssd1306Ctrl.getDisplay().display();
    ssd1306Ctrl.getDisplay().clearDisplay();
    ssd1306Ctrl.getDisplay().setTextSize(1);
    ssd1306Ctrl.getDisplay().setTextColor(WHITE);
    ssd1306Ctrl.getDisplay().setTextWrap(true);
    ssd1306Ctrl.getDisplay().setCursor(0, 0);
    ssd1306Ctrl.getDisplay().println("Test Mode Activated");
    ssd1306Ctrl.getDisplay().display();
  }
  currentChoice = 19;
  displayMenu_testMode();
}

void testcase_sequence() {
  err_t err = initCtrlObjs();

  if (err) {
    currentChoice = 0;
    releaseCtrlObjs();
    printMsg("Error occurs when initializing control objects: ");
    printlnMsg(err);
    displayMenu();
    return;
  }

  err = setupSequences();

  if (err) {
    currentChoice = 0;
    printMsg("Error occurs when initializing control objects: ");
    printlnMsg(err);
    displayMenu();
    return;
  }

  currentChoice = 20;
  displayMenu_sequence();
}

#ifdef USE_LiquidCrystal
void testcase_lcd1602(String inputs) {
  printlnMsg("\nRunning testcase_lcd1602...");
  err_t err;
  String params = inputs;
  params.replace(" ", "");
  int8_t commaIndex = params.indexOf(",");
  if (commaIndex == -1) {
    printlnMsg("Invalid Input");
    currentChoice = 0;
    return;
  }

  uint8_t scl = params.substring(0, commaIndex).toInt();
  uint8_t sda = params.substring(commaIndex + 1).toInt();
  // err = i2cCtrl.init(0, scl, sda);

  if (/*err != Control_OK*/ !Wire.begin(sda, scl)) {
    printMsg("I2C failed to begin");
  } else {
    printlnMsg("I2CMasterControl is initialized successfully");
    lcd = new LiquidCrystal_I2C(0x27, 16, 2);
    lcd->init();
    lcd->backlight();  // Turn on backlight
    lcd->setCursor(0, 0);
    lcd->print("Enter text:");
    lcd->setCursor(0, 1);
    lcd->print("Waiting...");
    currentChoice = 21;
    displayMenu_lcd1602();
  }
}
#endif

// #ifdef USE_SH1106Control
void testcase_sh1106(/*uint16_t width, uint16_t height, int i2cAddr*/ String _params) {
  String params = _params;
  params.replace(" ", "");
  int commaIndex1 = params.indexOf(',');
  int commaIndex2 = params.indexOf(',', commaIndex1 + 1);

  if (commaIndex1 == -1 || commaIndex2 == -1) {
    printlnMsg("Invalid Input. Failed to run testcase_sh1106.");
    return;
  }

  // Extract the three parts
  String widthStr = params.substring(0, commaIndex1);
  String heightStr = params.substring(commaIndex1 + 1, commaIndex2);
  String i2cAddrStr = params.substring(commaIndex2 + 1);

  // Convert the extracted strings to the corresponding types
  uint16_t width = widthStr.toInt();
  uint16_t height = heightStr.toInt();
  unsigned int i2cAddr = (unsigned int)strtol(i2cAddrStr.c_str(), NULL, 16);
  // Implement Test Case 2 logic here
  printlnMsg("\nRunning testcase_sh1106...");

  err_t err;

  err = i2cCtrl.init(0, 10, 6);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize I2CMasterControl. Reason is: ");
    switch (err) {
      case I2CMasterControl_InvalidI2CIndex:
        printlnMsg("I2C index is invalid. Only 0 is allowed");
        break;
      case I2CMasterControl_InvalidSCL:
        printlnMsg("SCL pin is invalid");
        break;
      case I2CMasterControl_InvalidSDA:
        printlnMsg("SDA pin is invalid");
        break;
      case I2CMasterControl_InvalidClkFreq:
        printlnMsg("Clock Frequency is invalid");
        break;
    }
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    printlnMsg("I2CMasterControl is initialized successfully");
  }


  err = sh1106Ctrl.init(i2cCtrl, i2cAddr, width, height, -1);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize SH1106Control. Reason is: ");
    switch (err) {
      case SH1106Control_I2CNotActive:
        printlnMsg("I2CMasterControl is not active");
        break;
      case SH1106Control_I2CAddrError:
        printlnMsg("I2C address is invalid for SH1106Control");
        break;
    }
    printlnMsg("Enter 'x' to go back to Menu");
    sh1106Ready = false;
    return;
  } else {
    printlnMsg("Successfully request sh1106Ctrl");
    sh1106Ctrl.getDisplay().display();
    sh1106Ctrl.getDisplay().clearDisplay();
    sh1106Ctrl.getDisplay().setTextSize(1);
    sh1106Ctrl.getDisplay().setTextColor(WHITE);
    sh1106Ctrl.getDisplay().setTextWrap(true);
    sh1106Ctrl.getDisplay().setCursor(0, 0);
    sh1106Ctrl.getDisplay().println("Successfully request sh1106Ctrl");
    sh1106Ctrl.getDisplay().display();
    sh1106Ctrl.getDisplay().clearDisplay();
    initTestdrawbitmap_sh1106(logo16_glcd_bmp, LOGO16_GLCD_HEIGHT, LOGO16_GLCD_WIDTH);

    printlnMsg("Enter 'x' to go back to Menu");
    sh1106Ready = true;
    return;
  }
}
// #endif


// #ifdef USE_SSD1306Control
void testcase_ssd1306(/*uint16_t width, uint16_t height, int i2cAddr*/ String _params) {
  String params = _params;
  params.replace(" ", "");
  int commaIndex1 = params.indexOf(',');
  int commaIndex2 = params.indexOf(',', commaIndex1 + 1);

  if (commaIndex1 == -1 || commaIndex2 == -1) {
    printlnMsg("Invalid Input. Failed to run testcase_sh1106.");
    return;
  }

  // Extract the three parts
  String widthStr = params.substring(0, commaIndex1);
  String heightStr = params.substring(commaIndex1 + 1, commaIndex2);
  String i2cAddrStr = params.substring(commaIndex2 + 1);

  // Convert the extracted strings to the corresponding types
  uint16_t width = widthStr.toInt();
  uint16_t height = heightStr.toInt();
  int i2cAddr = (unsigned int)strtol(i2cAddrStr.c_str(), NULL, 16);
  // Implement Test Case 2 logic here
  printlnMsg("\nRunning testcase_ssd1306...");

  err_t err;

  err = i2cCtrl.init(0, 10, 6);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize I2CMasterControl. Reason is: ");
    switch (err) {
      case I2CMasterControl_InvalidI2CIndex:
        printlnMsg("I2C index is invalid. Only 0 is allowed");
        break;
      case I2CMasterControl_InvalidSCL:
        printlnMsg("SCL pin is invalid");
        break;
      case I2CMasterControl_InvalidSDA:
        printlnMsg("SDA pin is invalid");
        break;
      case I2CMasterControl_InvalidClkFreq:
        printlnMsg("Clock Frequency is invalid");
        break;
    }
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    printlnMsg("I2CMasterControl is initialized successfully");
  }

  err = ssd1306Ctrl.init(i2cCtrl, i2cAddr, width, height, -1);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize SSD1306Control. Reason is: ");
    switch (err) {
      case SSD1306Control_I2CNotActive:
        printlnMsg("I2CMasterControl is not active");
        break;
      case SSD1306Control_I2CAddrError:
        printlnMsg("I2C address is invalid for SSD1306Control");
        break;
    }
    printlnMsg("Enter 'x' to go back to Menu");
    ssd1306Ready = false;
    return;
  } else {
    printlnMsg("Successfully request ssd1306Ctrl");
    ssd1306Ctrl.getDisplay().display();
    ssd1306Ctrl.getDisplay().clearDisplay();
    ssd1306Ctrl.getDisplay().setTextSize(1);
    ssd1306Ctrl.getDisplay().setTextColor(WHITE);
    ssd1306Ctrl.getDisplay().setTextWrap(true);
    ssd1306Ctrl.getDisplay().setCursor(0, 0);
    ssd1306Ctrl.getDisplay().println("Successfully request ssd1306Ctrl");
    ssd1306Ctrl.getDisplay().display();
    ssd1306Ctrl.getDisplay().clearDisplay();
    initTestdrawbitmap_ssd1306(logo16_glcd_bmp, LOGO16_GLCD_HEIGHT, LOGO16_GLCD_WIDTH);

    printlnMsg("Enter 'x' to go back to Menu");
    ssd1306Ready = true;
    return;
  }
}
// #endif

void testcase_neopixel(/*int pinNum, int noOfLed*/ String _params) {
  String params = _params;
  params.replace(" ", "");
  int commaIndex = params.indexOf(',');

  if (commaIndex == -1) {
    printlnMsg("Invalid input");
    return;
  }

  // Extract the two parts
  String pinNumStr = params.substring(0, commaIndex);
  String noOfLedStr = params.substring(commaIndex + 1);

  // Convert the extracted strings to the corresponding types
  int pinNum = pinNumStr.toInt();
  int noOfLed = noOfLedStr.toInt();
  // Implement Test Case 3 logic here
  err_t err;
  printlnMsg("\nRunning testcase_neopixel...");
  err = addrLedCtrl.init(pinNum, noOfLed, true);

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize AddrLEDControl. Reason is: ");
    switch (err) {
      case AddrLEDControl_InvalidPinIndex:
        printlnMsg("Pin is invalid");
        break;
    }

    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    printlnMsg("AddrLEDControl is requested successfully");
    addrLedCtrl.enableScheduler(0, 100, nullptr);
    // std::vector<int> targets;
    // for (uint8_t i = 0; i < noOfLed; i++) {
    //   targets.push_back(i);
    // }
    displayMenu_addrLed();

    printlnMsg("Enter 'x' to go back to Menu");
    return;
  }
}


void testcase_servo(String _pinNums) {
  int pinNums[6];
  int numOfInput = extractValues_int(_pinNums, ',', pinNums, 6);
  bool isAllServoInitSuccessful = true;

  for (int i = 0; i < numOfInput; i++) {
    err_t err;
    printlnMsg("Running testcase_servo...");
    err = servoCtrl[i].init(pinNums[i], false);
    if (err != Control_OK) {
      isAllServoInitSuccessful = false;
      printMsg("Error: Fail to initialize ServoControl. Reason is: ");
      switch (err) {
        case ServoControl_InvalidPinIndex:
          printlnMsg("Pin is invalid");
          break;
      }
    }
  }

  if (isAllServoInitSuccessful) {
    noOfActiveServo = numOfInput;
    printMsg("ServoControl is requested successfully (no of servo=");
    printlnMsg(numOfInput);
    displayMenu_servo();
  } else {
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  }
}

void testcase_tone(/*int pinNum*/ String pinNum_str) {
  int pinNum = pinNum_str.toInt();
  err_t err;
  printlnMsg("\nRunning testcase_tone...");
  err = toneCtrl.init(pinNum, false);
  if (err != Control_OK) {
    printMsg("Error: Fail to initialize ToneControl. Reason is: ");
    switch (err) {
      case ToneControl_InvalidPinIndex:
        printlnMsg("Pin is invalid");
        break;
    }
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    printlnMsg("ToneControl is requested successfully");
    displayMenu_tone();
  }
}

void testcase_pwm(String _pinNums) {
  int pinNums[6];
  int numOfInput = extractValues_int(_pinNums, ',', pinNums, 6);
  bool isAllPWMInitSuccessful = true;

  for (int i = 0; i < numOfInput; i++) {
    err_t err;
    printlnMsg("Running testcase_pwm...");
    err = pwmCtrl[i].init(pinNums[i], false);
    if (err != Control_OK) {
      isAllPWMInitSuccessful = false;
      printMsg("Error: Fail to initialize PWMControl. Reason is: ");
      switch (err) {
        case PWMControl_InvalidPinIndex:
          printlnMsg("Pin is invalid");
          break;
      }
    }
  }

  if (isAllPWMInitSuccessful) {
    noOfActivePWM = numOfInput;
    printlnMsg("PWMControl is requested successfully");
    displayMenu_pwm();
  }
}

void testcase_adc(/*int pinNum*/ String pinNum_str) {
  int pinNum = pinNum_str.toInt();
  err_t err;
  printlnMsg("\nRunning testcase_adc...");
  err = adcCtrl.init(1, pinNum, true);
  if (err != Control_OK) {
    printMsg("Error: Fail to initialize ADCControl. Reason is: ");
    switch (err) {
      case ADCControl_InvalidADC:
        printlnMsg("Pin is invalid");
        break;
    }
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    printlnMsg("ADCControl is requested successfully");
    adcCtrl.enableScheduler(0, 500, adcHandler);
    displayMenu_adc();
  }
}

void testcase_gpioIn(String _inputs) {
  bootButtonCtrl.release();
  int inputs[2];
  int numOfInput = extractValues_int(_inputs, ',', inputs, 2);
  err_t err = -40;
  printlnMsg("\nRunning testcase_gpioIn...");
  if (numOfInput == 1) {
    err = binInCtrl.init(inputs[0], INPUT);
  } else if (numOfInput == 2) {
    if (inputs[1] == 0) {
      err = binInCtrl.init(inputs[0], INPUT);
    } else if (inputs[1] == 1) {
      err = binInCtrl.init(inputs[0], INPUT_PULLUP);
    }
  }
  if (err != Control_OK) {
    printMsg("Error: Fail to initialize BinInControl. Reason is: ");
    switch (err) {
      case BinInControl_InvalidPinMode:
        printlnMsg("Pin Mode is invalid");
        break;
      case BinInControl_InvalidPinIndex:
        printlnMsg("Pin Index is invalid");
        break;
      case BinInControl_InterruptNotEnabled:
        printlnMsg("Interrupt is not enabled");
        break;
      default:
        printlnMsg("Invalid input");
    }
    Serial.println(err);
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    printlnMsg("BinInControl is requested successfully");
    binInCtrl.enableScheduler(0, 200, binInHandler);
    binInCtrl.enableInterrupt(CHANGE);
    displayMenu_gpioIn();
  }
}

void testcase_gpioOut(String _inputs) {
  int inputs[2];
  int numOfInput = extractValues_int(_inputs, ',', inputs, 2);
  err_t err = -40;
  printlnMsg("\nRunning testcase_gpioOut...");
  if (numOfInput == 1) {
    err = binOutCtrl.init(inputs[0], LOW);
  } else if (numOfInput == 2) {
    if (inputs[1] == 0) {
      err = binOutCtrl.init(inputs[0], LOW);
    } else if (inputs[1] == 1) {
      err = binOutCtrl.init(inputs[0], HIGH);
    }
  }

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize BinOutControl. Reason is: ");
    switch (err) {
      case BinOutControl_InvalidPinIndex:
        printlnMsg("Pin Index is invalid");
        break;
      default:
        printlnMsg("Invalid input");
    }
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    printlnMsg("BinOutControl is requested successfully");
    displayMenu_gpioOut();
  }
}

void testcase_wifi(String _params) {
  String params = _params;
  // params.replace(" ", "");
  int commaIndex = params.indexOf(',');

  if (commaIndex == -1) {
    printlnMsg("Invalid input");
    return;
  }

  // Extract the two parts
  String wifi_ssid = params.substring(0, commaIndex);
  String wifi_pass = params.substring(commaIndex + 1);

  printlnMsg("\nRunning testcase_wifi...");
  err_t err = wifiCtrl.init(WiFiControlWiFiModeAPSTA);

  if (err != Control_OK && err != Control_ActiveAlready) {
    printMsg("Error: Fail to initialize WiFiControl. Reason is: ");
    printlnMsg(err);
    wifiCtrl.release();
    printlnMsg("Enter 'x' to go back to Menu");
    return;
  } else {
    wifiCtrl.connect(wifi_ssid, wifi_pass);
    printMsg("Connecting to WiFi ");
    printMsg(wifi_ssid);
    int retryCount = 0;
    while (!wifiCtrl.isConnected() && retryCount < 5) {
      printMsg(".");
      retryCount++;
      delay(1000);
    }
    if (wifiCtrl.isConnected()) {
      printlnMsg();
      printlnMsg("WiFi is connected successfully");
      printMsg("IP Address is: ");
      IPAddress ip = WiFi.localIP();
      String ip_str = String(ip[0]) + "." + String(ip[1]) + "." + String(ip[2]) + "." + String(ip[3]);
      printlnMsg(ip_str);
      DynamicJsonDocument wifiDoc(256);
      wifiDoc["wifi1"]["ssid"] = wifi_ssid;
      wifiDoc["wifi1"]["pass"] = wifi_pass;
      File wifiFile = LittleFS.open("/wifi.json", "w");
      serializeJson(wifiDoc, wifiFile);
      wifiFile.close();
      currentChoice = 0;
      displayMenu();
    } else {
      printlnMsg();
      printlnMsg("Failed to connect WiFi. Please retry.");
      wifiCtrl.release();
      currentChoice = 0;
      displayMenu();
    }
  }
}

#ifdef USE_HTTPClientControl
void testcase_http(String _inputs) {
  String params = _inputs;
  params.replace(" ", "");
  int commaIndex = params.indexOf(',');
  int commaIndex2 = params.indexOf(',', commaIndex + 1);

  bool isHTTPS = false;

  if (commaIndex2 != -1) {
    String isHTTPS_str = params.substring(commaIndex2 + 1);
    if (isHTTPS_str == "true") {
      isHTTPS = true;
    }
  } else {
    String isHTTPS_str = params.substring(commaIndex + 1);
    if (isHTTPS_str == "true") {
      isHTTPS = true;
    }
  }

  // Extract the three parts
  // String link = params.substring(0, commaIndex);
  // String port = params.substring(commaIndex + 1);
  printlnMsg("\nRunning testcase_http...");
  err_t err;

  if (isHTTPS) {
    err = httpClientCtrl.init(wifiCtrl, true, 1024);
  } else {
    err = httpClientCtrl.init(wifiCtrl, false, 1024);
  }

  if (err != Control_OK) {
    printMsg("Error: Fail to initialize HTTPClientControl. Reason is: ");
    switch (err) {
      case HTTPClientControl_WiFiControlNotInit:
        printlnMsg("WiFiControl is not initialized. Please use function 12 to connect WiFi first.");
        break;
      case HTTPClientControl_ConnectionFailed:
        printlnMsg("Failed to connect to HTTP server");
        break;
      default:
        printlnMsg("Invalid input");
    }
    currentChoice = 0;
    displayMenu();
    return;
  } else {
    printlnMsg("HTTPClientControl is requested successfully");
    Serial.println(isHTTPS);
    if (isHTTPS) {
      httpClientCtrl.setInsecure();
    }
    if (commaIndex2 == -1) {  //port is not provided
      String link = params.substring(0, commaIndex);
      // err = httpClientCtrl.connect(link);
      httpTargetLink = link;
      httpTargetPort = 0;
    } else {
      String link = params.substring(0, commaIndex);
      uint16_t port = params.substring(commaIndex + 1).toInt();
      // err = httpClientCtrl.connect(link, port);
      httpTargetLink = link;
      httpTargetPort = port;
    }
    // if (err) {
    //   printlnMsg("Failed to connect to HTTP server");
    //   printMsg("Error code is: ");
    //   printlnMsg(err);
    //   currentChoice = 0;
    //   httpClientCtrl.release();
    //   displayMenu();
    // } else {
    httpClientCtrl.enableScheduler(0, 10, httpClientCtrlEventHandler);
    displayMenu_http();
    // }
  }
}
#endif

void testcase_mqtt(String _inputs) {
  String params = _inputs;
  params.replace(" ", "");
  int commaIndex = params.indexOf(',');

  // Extract the three parts
  // String link = params.substring(0, commaIndex);
  // String port = params.substring(commaIndex + 1);
  printlnMsg("\nRunning testcase_mqtt...");

  brokerAddr = params.substring(0, commaIndex);
  brokerPort = params.substring(commaIndex + 1).toInt();
  client.setServer(brokerAddr.c_str(), brokerPort);
  shouldMqttConnect = true;

  // displayMenu_mqtt();
}

void testcase_mqtt_ws(String _inputs) {
  String params = _inputs;
  params.replace(" ", "");
  int commaIndex = params.indexOf(',');

  // Extract the three parts
  // String link = params.substring(0, commaIndex);
  // String port = params.substring(commaIndex + 1);
  printlnMsg("\nRunning testcase_mqtt_ws...");

  brokerAddr = params.substring(0, commaIndex);
  brokerPort = params.substring(commaIndex + 1).toInt();
  // wsMqttClient.connect(brokerAddr, brokerPort);
  // Serial.println("Calling connectMQTT_WS in testcase_mqtt_ws");
  connectMQTT_WS(brokerAddr, brokerPort);
  if (wsMqttClient.isConnected()) {
    displayMenu_mqtt();
    shouldMqttConnect_WS = true;
  } else {
    currentChoice = 0;
    wsMqttClient.disconnect();
    shouldMqttConnect_WS = false;
    displayMenu();
  }

  // displayMenu_mqtt();
}

void testcase_dfPlayer(String _inputs) {
  String params = _inputs;
  params.replace(" ", "");
  int commaIndex = params.indexOf(',');
  int commaIndex2 = params.indexOf(',', commaIndex + 1);

  printlnMsg("\nRunning testcase_dfPlayer...");

  uint8_t rxPin = params.substring(0, commaIndex).toInt();
  uint8_t txPin = params.substring(commaIndex + 1, commaIndex2).toInt();
  uint8_t busyPin = params.substring(commaIndex2 + 1).toInt();

  err_t err = hwUartCtrl.init(1, rxPin, txPin, -1, -1, 9600, UART_8N1);
  if (err != Control_OK) {
    Serial.print("Failed to init UARTControl (HW). Reason is: ");
    switch (err) {
      case Control_ActiveAlready:
        {
          Serial.println("UARTControl is active already");
          break;
        }
    }
  }

  err = mp3Ctrl.init(hwUartCtrl, busyPin);

  if (err != Control_OK) {
    Serial.print("Failed to init MP3Control. Reason is: ");
    switch (err) {
      case Control_ActiveAlready:
        {
          printlnMsg("MP3Control is active already");
          break;
        }
      case DFPlayerMP3Control_PlayerFailedToBegin:
        {
          printlnMsg("DFPlayer failed to begin");
          break;
        }
    }
  }

  if (!err) {
    // mp3Ctrl.getPlayer().next();
    // mp3Ctrl.getPlayer().pause();
    mp3Ctrl.enableScheduler(0, 200, nullptr);
    displayMenu_dfPlayer();
  } else {
    currentChoice = 0;
    mp3Ctrl.release();
    hwUartCtrl.release();
    displayMenu();
  }
}

#ifdef USE_VL53L0XControl
void testcase_vl53l0x(String _inputs) {
  String params = _inputs;
  params.replace(" ", "");
  int commaIndex = params.indexOf(',');

  printlnMsg("\nRunning testcase_vl53l0x...");

  uint8_t sclPin = params.substring(0, commaIndex).toInt();
  uint8_t sdaPin = params.substring(commaIndex + 1).toInt();

  err_t err = i2cCtrl.init(0, sclPin, sdaPin);
  if (err) {
    Serial.print("Fail to initialize i2cCtrl. Error code = ");
    Serial.println(err);
  }

  err = vl53l0xCtrl.init(i2cCtrl);
  if (err) {
    Serial.print("Fail to initialize vl53l0xCtrl. Error code = ");
    Serial.println(err);
  }

  if (err != Control_OK) {
    Serial.print("Failed to init vl53l0xCtrl. Reason is: ");
    switch (err) {
      case Control_ActiveAlready:
        {
          printlnMsg("VL53L0XControl is active already");
          break;
        }
      case I2CMasterControl_InvalidSCL:
        {
          printlnMsg("SCL pin is invalid");
          break;
        }
      case I2CMasterControl_InvalidSDA:
        {
          printlnMsg("SDA pin is invalid");
          break;
        }
      case I2CMasterControl_TwoWireBeginErr:
        {
          printlnMsg("TwoWire failed to begin");
          break;
        }
    }
  }

  if (!err) {
    vl53l0xCtrl.enableScheduler(0, 10, vl53l0xHandler);
    displayMenu_vl53l0x();
  } else {
    currentChoice = 0;
    vl53l0xCtrl.release();
    i2cCtrl.release();
    displayMenu();
  }
}
#endif

#ifdef USE_UltraSonicControl
void testcase_ultrasonic(String _inputs) {
  String params = _inputs;
  params.replace(" ", "");
  int commaIndex = params.indexOf(',');

  printlnMsg("\nRunning testcase_ultrasonic...");

  uint8_t trigPin = params.substring(0, commaIndex).toInt();
  uint8_t echoPin = params.substring(commaIndex + 1).toInt();

  err_t err = ultraSonicCtrl.init(trigPin, echoPin);

  if (err != Control_OK) {
    Serial.print("Failed to init ultraSonicCtrl. Reason is: ");
    switch (err) {
      case Control_ActiveAlready:
        {
          printlnMsg("UltraSonicControl is active already");
          break;
        }
    }
  }

  if (!err) {
    ultraSonicCtrl.startMeasure();
    ultraSonicCtrl.enableScheduler(0, 1000, ultraSonicCtrlHandler);
    displayMenu_ultrasonic();
  } else {
    currentChoice = 0;
    ultraSonicCtrl.release();
    displayMenu();
  }
}
#endif

void testcase_selectDisplay(String _input) {
  if (_input == "1") {
    printlnMsg("Selected SH1106");
    displayType = 1;
    saveDisplayType(1);
    currentChoice = 0;
    displayMenu();
  } else if (_input == "2") {
    printlnMsg("Selected SSD1306");
    displayType = 2;
    saveDisplayType(2);
    currentChoice = 0;
    displayMenu();
  } else if (_input == "x") {
    currentChoice = 0;
    displayMenu();
  } else {
    printlnMsg("Invalid input");
    waitForUserInput(testcase_selectDisplay);
  }
}

void waitForUserInput(FuncPtr_testcase targetFunc) {
  funcPtr_testcase = targetFunc;
  waitingUserInput = true;
}

void handleInput_mpr121(String input) {
  if (input == "x") {
    currentChoice = 0;
    mpr121Ctrl.release();
    i2cCtrl.release();
    displayMenu();
  }
}

void handleInput_testMode(String input) {
  if (input == "x") {
    currentChoice = 0;
    mpr121Ctrl.release();
    i2cCtrl.release();
    servoCtrl[0].release();
    servoCtrl[1].release();
    addrLedCtrl.release();
    if (mp3Ctrl.isInit()) {
      mp3Ctrl.getPlayer().stop();
    }
    mp3Ctrl.release();
    hwUartCtrl.release();
    if (displayType == 1) {
      sh1106Ctrl.getDisplay().clearDisplay();
      sh1106Ctrl.getDisplay().display();
      sh1106Ctrl.release();
    } else if (displayType == 2) {
      ssd1306Ctrl.getDisplay().clearDisplay();
      ssd1306Ctrl.getDisplay().display();
      ssd1306Ctrl.release();
    }

#ifdef USE_HTTPClientControl
    shouldDisplayTime = false;
    httpClientCtrl.release();
#endif
    displayMenu();
  }
}

void handleInput_sequence(String input) {
  if (input == "x") {
    currentChoice = 0;
    sequenceInputState = 0;
    sequence_firstInput = 0;
    sequence_waitingSecondInput = false;
    //placeholder for release logic
    releaseCtrlObjs();
    mpr121Ctrl.release();
    if (displayType == 1 && sh1106Ready) {
      sh1106Ctrl.getDisplay().clearDisplay();
      sh1106Ctrl.getDisplay().display();
      sh1106Ready = false;
      sh1106Ctrl.release();
    } else if (displayType == 2 && ssd1306Ready) {
      ssd1306Ctrl.getDisplay().clearDisplay();
      ssd1306Ctrl.getDisplay().display();
      ssd1306Ready = false;
      ssd1306Ctrl.release();
    }
    i2cCtrl.release();
    displayMenu();
  } else if (input == "1") {  //enable using mpr121 to play sequence
    sequence_firstInput = 1;
    err_t err = i2cCtrl.init(0, 10, 6);

    if (err != Control_OK) {
      printMsg("Error: Fail to initialize I2CMasterControl. Reason is: ");
      switch (err) {
        case I2CMasterControl_InvalidI2CIndex:
          printlnMsg("I2C index is invalid. Only 0 is allowed");
          break;
        case I2CMasterControl_InvalidSCL:
          printlnMsg("SCL pin is invalid");
          break;
        case I2CMasterControl_InvalidSDA:
          printlnMsg("SDA pin is invalid");
          break;
        case I2CMasterControl_InvalidClkFreq:
          printlnMsg("Clock Frequency is invalid");
          break;
      }
    } else {
      printlnMsg("I2CMasterControl is initialized successfully");
    }

    if (displayType == 1) {
      String i2cAddrStr = "3c";
      uint16_t width = 128;
      uint16_t height = 64;
      int i2cAddr = (unsigned int)strtol(i2cAddrStr.c_str(), NULL, 16);
      err = sh1106Ctrl.init(i2cCtrl, i2cAddr, width, height, -1);

      if (err != Control_OK) {
        printMsg("Error: Fail to initialize SH1106Control. Reason is: ");
        switch (err) {
          case SSD1306Control_I2CNotActive:
            printlnMsg("I2CMasterControl is not active");
            break;
          case SSD1306Control_I2CAddrError:
            printlnMsg("I2C address is invalid for SSD1306Control");
            break;
        }
        // printlnMsg("Enter 'x' to go back to Menu");
        sh1106Ready = false;
        // return;
      } else {
        printlnMsg("Successfully request sh1106Ctrl");
        sh1106Ctrl.getDisplay().display();
        sh1106Ctrl.getDisplay().clearDisplay();
        sh1106Ctrl.getDisplay().setTextSize(1);
        sh1106Ctrl.getDisplay().setTextColor(WHITE);
        sh1106Ctrl.getDisplay().setTextWrap(true);
        sh1106Ctrl.getDisplay().setCursor(0, 0);
        sh1106Ctrl.getDisplay().println("Successfully request sh1106Ctrl");
        sh1106Ctrl.getDisplay().display();
        sh1106Ctrl.getDisplay().clearDisplay();
        initTestdrawbitmap_sh1106(logo16_glcd_bmp, LOGO16_GLCD_HEIGHT, LOGO16_GLCD_WIDTH);

        // printlnMsg("Enter 'x' to go back to Menu");
        sh1106Ready = true;
        // return;
      }
    } else {
      String i2cAddrStr = "3c";
      uint16_t width = 128;
      uint16_t height = 64;
      int i2cAddr = (unsigned int)strtol(i2cAddrStr.c_str(), NULL, 16);
      err = ssd1306Ctrl.init(i2cCtrl, i2cAddr, width, height, -1);

      if (err != Control_OK) {
        printMsg("Error: Fail to initialize SSD1306Control. Reason is: ");
        switch (err) {
          case SSD1306Control_I2CNotActive:
            printlnMsg("I2CMasterControl is not active");
            break;
          case SSD1306Control_I2CAddrError:
            printlnMsg("I2C address is invalid for SSD1306Control");
            break;
        }
        // printlnMsg("Enter 'x' to go back to Menu");
        ssd1306Ready = false;
        // return;
      } else {
        printlnMsg("Successfully request ssd1306Ctrl");
        ssd1306Ctrl.getDisplay().display();
        ssd1306Ctrl.getDisplay().clearDisplay();
        ssd1306Ctrl.getDisplay().setTextSize(1);
        ssd1306Ctrl.getDisplay().setTextColor(WHITE);
        ssd1306Ctrl.getDisplay().setTextWrap(true);
        ssd1306Ctrl.getDisplay().setCursor(0, 0);
        ssd1306Ctrl.getDisplay().println("Successfully request ssd1306Ctrl");
        ssd1306Ctrl.getDisplay().display();
        ssd1306Ctrl.getDisplay().clearDisplay();
        initTestdrawbitmap_ssd1306(logo16_glcd_bmp, LOGO16_GLCD_HEIGHT, LOGO16_GLCD_WIDTH);

        // printlnMsg("Enter 'x' to go back to Menu");
        ssd1306Ready = true;
        // return;
      }
    }

    err = mpr121Ctrl.init(i2cCtrl, 0x5A, 7, 1000, 10, mpr121CtrlEventHandler_sequence);
    if (err != Control_OK) {
      printMsg("Error: Fail to initialize MPR121Control. Reason is: ");
      switch (err) {
        case MPR121Control_I2CNotActive:
          printlnMsg("I2CMasterControl is not active");
          break;
        case Control_NullEventHandler:
          printlnMsg("MPR121Control Event Handler is null");
          break;
        case MPR121Control_I2CAddrError:
          printlnMsg("I2C address is invalid for MPR121Control");
          break;
        case MPR121Control_IRQInvalid:
          printlnMsg("IRQ pin is invalid for MPR121Control");
          break;
      }

      // currentChoice = 0;
      displayMenu_sequence_noMPR121();
      sequence_firstInput = 1;
      sequence_waitingSecondInput = true;
      return;
    }

    printlnMsg();
    printlnMsg("Touch and release MPR121 to play specific set of sequence OR enter \"x\" to go back main menu.");
  } else if (input == "2") {  //change setting: 1. mpr121 key-binding 2.wait until finish/abort current and play next
    sequence_firstInput = 2;
    sequence_waitingSecondInput = true;
    printlnMsg("Select setting to change:");
    printlnMsg("1: MPR121 key binding");
    printlnMsg("2: Change mode (waiting until finish/abort current sequence and play next sequence immediately)");
  }
}

#ifdef USE_LiquidCrystal
void handleInput_lcd1602(String userInput) {
  if (userInput == "x") {
    lcd->clear();
    currentChoice = 0;
    delete lcd;
    // i2cCtrl.release();
    Wire.end();
    displayMenu();
  } else {
    lcd->clear();  // Clear previous content

    // Handle text longer than 16 characters
    if (userInput.length() <= 16) {
      lcd->setCursor(0, 0);
      lcd->print(userInput);
    } else {
      // Display first 16 characters on row 1
      lcd->setCursor(0, 0);
      lcd->print(userInput.substring(0, 16));
      // Display next 16 characters (or less) on row 2
      if (userInput.length() > 16) {
        lcd->setCursor(0, 1);
        lcd->print(userInput.substring(16, std::min(userInput.length(), (unsigned int)32)));
      }
    }
    displayMenu_lcd1602();
  }
}
#endif

void handleSecondInput_sequence(String userInput) {
  if (sequence_firstInput == 1) {
    if (userInput == "x") {
      sequenceInputState = 0;
      sequence_firstInput = 0;
      sequence_waitingSecondInput = false;
      mpr121Ctrl.release();
      i2cCtrl.release();
      displayMenu_sequence();
      return;
    } else {
      int i = userInput.toInt();
      if (mpr121_seq_mode == 1) {
        Serial.println("current mpr121_seq_mode is 1");
        if (isAllFinish()) {
          if (mpr121_seq_mapping[i] != -1) {
            playSetSequence(mpr121_seq_mapping[i]);
          } else {
            playSetSequence(i);
          }
        }
      } else if (mpr121_seq_mode == 2) {
        Serial.println("current mpr121_seq_mode is 2");
        addrLedCtrl_0.abortAllSequences();
        if (mpr121_seq_mapping[i] != -1) {
          playSetSequence(mpr121_seq_mapping[i]);
        } else {
          playSetSequence(i);
        }
      }
      displayMenu_sequence_noMPR121();
    }
  } else if (sequence_firstInput == 2) {  // change setting
    switch (sequenceInputState) {
      case 0:  // select setting to change
        {
          if (userInput == "1") {  //change mpr121 key-binding
            printlnMsg("Enter \"mpr121 touch pin\" & \"number of corresponding sequence set\"(separated by comma) [example: 0,1] OR enter \"x\" to go back play sequence menu");
            sequenceInputState = 1;
          } else if (userInput == "2") {  //change "wait until finish/abort current and play next"
            printlnMsg("Enter the mode for sequence playback");
            printlnMsg("1: waiting until sequence finishes");
            printlnMsg("2: abort currently playing sequence and play next sequence immediately");
            printlnMsg("x: go back play sequence menu");
            sequenceInputState = 2;
          }
          break;
        }
      case 1:
        {
          if (userInput == "x") {
            sequenceInputState = 0;
            sequence_firstInput = 0;
            sequence_waitingSecondInput = false;
            displayMenu_sequence();
            return;
          }
          int commaIndex = userInput.indexOf(",");
          if (commaIndex != -1) {
            int mprPoint = userInput.substring(0, commaIndex).toInt();
            int seqNum = userInput.substring(commaIndex + 1).toInt();
            // mpr121_seq_map[mprPoint] = seqNum;
            mpr121_seq_mapping[mprPoint] = seqNum;
            saveSequenceSetting();
            printlnMsg("Mapping Done. You may enter another pair of values of enter \"x\" to go back play sequence menu.");
          } else {
            printlnMsg("Invalid Input");
          }
          break;
        }
      case 2:
        {
          if (userInput == "1") {
            mpr121_seq_mode = 1;
          } else if (userInput == "2") {
            mpr121_seq_mode = 2;
          } else {
            printlnMsg("Invalid Input");
            return;
          }
          saveSequenceSetting();
          sequenceInputState = 0;
          sequence_firstInput = 0;
          sequence_waitingSecondInput = false;
          displayMenu_sequence();
          return;
          break;
        }
    }
  }
}

// #ifdef USE_SH1106Control
void handleInput_sh1106(String input) {
  if (input == "x") {
    sh1106Ready = false;
    currentChoice = 0;
    sh1106Ctrl.getDisplay().clearDisplay();
    sh1106Ctrl.getDisplay().display();
    sh1106Ctrl.release();
    i2cCtrl.release();
    displayMenu();
  }
}
// #endif

// #ifdef USE_SSD1306Control
void handleInput_ssd1306(String input) {
  if (input == "x") {
    ssd1306Ready = false;
    currentChoice = 0;
    ssd1306Ctrl.getDisplay().clearDisplay();
    ssd1306Ctrl.getDisplay().display();
    ssd1306Ctrl.release();
    i2cCtrl.release();
    displayMenu();
  }
}
// #endif

void handleInput_addrLed(String input) {
  if (input == "x") {
    currentChoice = 0;
    addrLedCtrl.release();
    displayMenu();
    return;
  } else if (input == "1") {  //setRGB
    printlnMsg("Enter parameters (index,r,g,b OR start_index,end_index,r,g,b): ");
    addr_firstInput = 1;
    addr_waitingSecondInput = true;
  } else if (input == "2") {  //setHSV
    printlnMsg("Enter parameters (index,h,s,v OR start_index,end_index,h,s,v): ");
    addr_firstInput = 2;
    addr_waitingSecondInput = true;
  } else if (input == "3") {
    printlnMsg("Enter parameters (index, duration, start_r, start_g, start_b, end_r, end_g, end_b (e.g. [0,5000,255,0,0,0,0,255]) OR start_index, end_index, duration, start_r, start_g, start_b, end_r, end_g, end_b (e.g. [0,9,5000,255,0,0,0,0,255])): ");
    addr_firstInput = 3;
    addr_waitingSecondInput = true;
  } else if (input == "4") {
    printlnMsg("Enter parameters (index, duration, start_h, start_s, start_v, end_h, end_s, end_v (e.g. [0,5000,0,80,80,270,80,80]) OR start_index, end_index, duration, start_h, start_s, start_v, end_h, end_s, end_v (e.g. [0,9,5000,0,80,80,270,80,80])): ");
    addr_firstInput = 4;
    addr_waitingSecondInput = true;
  } else {
    printlnMsg("Invalid input");
    displayMenu_addrLed();
  }
}

void handleSecondInput_addrLed(String userInput) {
  if (addr_firstInput == 1) {  //setRGB
    int inputs[5];
    int numOfInput = extractValues_int(userInput, ',', inputs, 5);
    std::vector<int> targets;
    if (numOfInput == 4) {
      targets.push_back(inputs[0]);
      addrLedCtrl.setRGB(targets, inputs[1], inputs[2], inputs[3]);
    } else if (numOfInput == 5) {
      for (uint8_t i = inputs[0]; i <= inputs[1]; i++) {
        targets.push_back(i);
      }
      addrLedCtrl.setRGB(targets, inputs[2], inputs[3], inputs[4]);
    } else {
      printlnMsg("Invalid input");
    }
  } else if (addr_firstInput == 2) {  //setHSV
    int inputs[5];
    int numOfInput = extractValues_int(userInput, ',', inputs, 5);
    std::vector<int> targets;
    if (numOfInput == 4) {
      targets.push_back(inputs[0]);
      addrLedCtrl.setHSV(targets, inputs[1], inputs[2], inputs[3]);
    } else if (numOfInput == 5) {
      for (uint8_t i = inputs[0]; i <= inputs[1]; i++) {
        targets.push_back(i);
      }
      addrLedCtrl.setHSV(targets, inputs[2], inputs[3], inputs[4]);
    } else {
      printlnMsg("Invalid input");
    }
  } else if (addr_firstInput == 3) {  //Interpolate RGB, expected input => startIndex, endIndex(optional), duration, start_r, start_g, start_b, end_r, end_g, end_b
    int inputs[9];
    int numOfInput = extractValues_int(userInput, ',', inputs, 9);
    std::vector<int> targets;
    if (numOfInput == 8) {
      targets.push_back(inputs[0]);

      addrLedSeq_advance.clearCommand();
      addrLedSeq_advance.addInterpolateRGB(inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7]);
      addrLedCtrl.playRelTime(targets, addrLedSeq_advance, 0, 1);
    } else if (numOfInput == 9) {
      for (uint8_t i = inputs[0]; i <= inputs[1]; i++) {
        targets.push_back(i);
      }

      addrLedSeq_advance.clearCommand();
      addrLedSeq_advance.addInterpolateRGB(inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7], inputs[8]);
      addrLedCtrl.playRelTime(targets, addrLedSeq_advance, 0, 1);
    } else {
      printlnMsg("Invalid input");
    }
  } else if (addr_firstInput == 4) {  //Interpolate HSV
    int inputs[9];
    int numOfInput = extractValues_int(userInput, ',', inputs, 9);
    std::vector<int> targets;
    if (numOfInput == 8) {
      targets.push_back(inputs[0]);

      addrLedSeq_advance.clearCommand();
      addrLedSeq_advance.addInterpolateHSV(inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7]);
      addrLedCtrl.playRelTime(targets, addrLedSeq_advance, 0, 1);
    } else if (numOfInput == 9) {
      for (uint8_t i = inputs[0]; i <= inputs[1]; i++) {
        targets.push_back(i);
      }

      addrLedSeq_advance.clearCommand();
      addrLedSeq_advance.addInterpolateHSV(inputs[2], inputs[3], inputs[4], inputs[5], inputs[6], inputs[7], inputs[8]);
      addrLedCtrl.playRelTime(targets, addrLedSeq_advance, 0, 1);
    } else {
      printlnMsg("Invalid input");
    }
  }

  displayMenu_addrLed();
}

void handleInput_servo(String input) {
  if (input == "x") {
    currentChoice = 0;
    for (uint8_t i = 0; i < noOfActiveServo; i++) {
      servoCtrl[i].release();
    }
    noOfActiveServo = 0;
    displayMenu();
    return;
  } else {
    double angles[noOfActiveServo];
    int numOfInput = extractValues_double(input, ',', angles, noOfActiveServo);
    for (uint8_t i = 0; i < numOfInput; i++) {
      servoCtrl[i].setAngle(angles[i]);
    }
  }
  displayMenu_servo();
}

void handleInput_tone(String input) {
  if (input == "x") {
    currentChoice = 0;
    toneCtrl.release();
    displayMenu();
    return;
  } else {
    uint32_t inputs[3];
    int numOfInput = extractValues_ulong(input, ',', inputs, 3);
    if (numOfInput < 3) {
      printlnMsg("Invalid Input");
    } else {
      toneCtrl.setTone(inputs[0], inputs[1]);
      delay(inputs[2]);
      toneCtrl.setDuty(0);
    }
  }
  displayMenu_tone();
}

void handleInput_pwm(String input) {
  if (input == "x") {
    currentChoice = 0;
    for (uint8_t i = 0; i < noOfActivePWM; i++) {
      pwmCtrl[i].release();
    }
    noOfActivePWM = 0;
    displayMenu();
    return;
  } else {
    int values[noOfActivePWM];
    int numOfInput = extractValues_int(input, ',', values, noOfActivePWM);
    for (uint8_t i = 0; i < numOfInput; i++) {
      pwmCtrl[i].setDuty(values[i]);
    }
  }
  displayMenu_pwm();
}

void handleInput_adc(String input) {
  if (input == "x") {
    currentChoice = 0;
    adcCtrl.release();
    displayMenu();
  }
}

void handleInput_gpioIn(String input) {
  if (input == "x") {
    currentChoice = 0;
    binInCtrl.release();
    displayMenu();
  }
}

void handleInput_gpioOut(String input) {
  if (input == "x") {
    currentChoice = 0;
    binOutCtrl.release();
    displayMenu();
    return;
  } else {
    if (input.toInt() == 0 || input.toInt() == 1) {
      binOutCtrl.write(input.toInt());
    } else {
      printlnMsg("Input can only be 0 OR 1 OR 'x' for going back main menu");
    }
  }
  displayMenu_gpioOut();
}

#ifdef USE_HTTPClientControl
void handleInput_http(String input) {
  if (input == "x") {
    currentChoice = 0;
    httpClientCtrl.release();
    displayMenu();
    return;
  } else if (input == "1") {  //GET
    printlnMsg("Enter \"path for resource and query\" (example: /weatherAPI/opendata/weather.php?dataType=flw&lang=en): ");
    http_firstInput = 1;
    http_waitingSecondInput = true;
  } else if (input == "2") {  //POST
    printlnMsg("Enter \"path for resource\", \"content type\" & \"content\" (example: /post-data-endpoint,application/json,{\"data1\":1234, \"data2\":5678}): ");
    http_firstInput = 2;
    http_waitingSecondInput = true;
  } else {
    printlnMsg("Invalid input");
    displayMenu_http();
  }
}
#endif

#ifdef USE_HTTPClientControl
void handleSecondInput_http(String _input) {
  httpReceivedBody = "";
  if (http_firstInput == 1) {  //GET
    String params = _input;
    int slashIndex = params.indexOf('/');
    // Serial.print("indexOf slash is: ");
    // Serial.println(slashIndex);
    if (slashIndex != 0) {  //user does not include "/" at the beginning of api
      params = "/" + params;
    }
    err_t err;
    if (httpTargetPort == 0) {
      err = httpClientCtrl.connect(httpTargetLink);
    } else {
      err = httpClientCtrl.connect(httpTargetLink, httpTargetPort);
    }
    if (err) {
      printlnMsg("Failed to connect to HTTP server");
      printMsg("Error code is: ");
      printlnMsg(err);
      currentChoice = 0;
      httpClientCtrl.release();
      displayMenu();
      return;
    }
    httpClientCtrl.get(params);
    httpClientCtrl.setReqHeaderConnClose();
    err = httpClientCtrl.sendRequest();
    if (err) {
      printlnMsg("Failed to send GET request");
      displayMenu_http();
    }
  } else if (http_firstInput == 2) {  //POST
    String params = _input;
    params.replace(" ", "");
    int commaIndex = params.indexOf(',');
    int commaIndex2 = params.indexOf(',', commaIndex + 1);

    String api = params.substring(0, commaIndex);
    String contentType = params.substring(commaIndex + 1, commaIndex2);
    String content = params.substring(commaIndex2 + 1);

    int slashIndex = api.indexOf('/');
    if (slashIndex != 0) {
      api = "/" + api;
    }

    err_t err;
    if (httpTargetPort == 0) {
      err = httpClientCtrl.connect(httpTargetLink);
    } else {
      err = httpClientCtrl.connect(httpTargetLink, httpTargetPort);
    }
    if (err) {
      printlnMsg("Failed to connect to HTTP server");
      printMsg("Error code is: ");
      printlnMsg(err);
      currentChoice = 0;
      httpClientCtrl.release();
      displayMenu();
      return;
    }

    httpClientCtrl.post(api, contentType, content);
    httpClientCtrl.setReqHeaderConnClose();
    err = httpClientCtrl.sendRequest();
    if (err) {
      printlnMsg("Failed to send POST request");
      displayMenu_http();
    }
  }

  // displayMenu();
}
#endif

void handleInput_mqtt(String input) {
  if (input == "x") {
    // if (mqttHasSubscribeTopic) {
    // client.unsubscribe(mqtt_topic.c_str());
    // mqttHasSubscribeTopic = false;
    // displayMenu_mqtt();
    // } else {
    currentChoice = 0;
    client.disconnect();
    shouldMqttConnect = false;
    displayMenu();
    // }
    return;
  } else if (input == "1") {  //Subscribe
    printlnMsg("Enter \"topic\" (example: exampleTopic/1): ");
    mqtt_firstInput = 1;
    mqtt_waitingSecondInput = true;
  } else if (input == "2") {  //Publish
    // printlnMsg("Enter \"topic\", \"message\" & \"shouldRetain\"(optional), parameters should be separated by comma: ");
    printlnMsg("Enter \"topic\" (example: exampleTopic/1): ");
    mqtt_firstInput = 2;
    mqtt_waitingSecondInput = true;
  } else {
    printlnMsg("Invalid input");
    displayMenu_mqtt();
  }
}

void handleSecondInput_mqtt(String _input) {
  switch (mqttInputState) {
    case 0:
      {
        if (mqtt_firstInput == 1) {  //Subscribe
          client.subscribe(_input.c_str());
          mqttHasSubscribeTopic = true;
          // mqtt_topic = _input;
          mqtt_topics.push_back(_input);
          mqttInputState = 1;
          printlnMsg("Subscribed topic \"" + _input + "\". You may enter extra topic to subscribe OR press \"x\" to go back MQTT menu");
        } else if (mqtt_firstInput == 2) {  //Publish
          mqtt_publish_topic = _input;
          mqttInputState = 2;
          printlnMsg("Enter \"content\" (example: {\"data1\":1234, \"data2\":5678}):");
        }
        break;
      }  //end of case: 0
    case 1:
      {
        if (_input == "x") {
          mqttInputState = 0;
          mqtt_waitingSecondInput = false;
          mqtt_firstInput = 0;
          for (uint8_t i = 0; i < mqtt_topics.size(); i++) {
            client.unsubscribe(mqtt_topics[i].c_str());
          }
          mqtt_topics.clear();
          displayMenu_mqtt();
          return;
        }
        client.subscribe(_input.c_str());
        mqtt_topics.push_back(_input);
        mqttHasSubscribeTopic = true;
        printlnMsg("Subscribed topics: " /* + _input + "\". You may enter extra topic to subscribe OR press \"x\" to go back MQTT menu"*/);
        for (int i = 0; i < mqtt_topics.size(); i++) {
          printlnMsg(mqtt_topics[i]);
        }
        printlnMsg("You may enter extra topic to subscribe OR press \"x\" to go back MQTT menu");
        break;
      }
    case 2:
      {
        mqtt_publish_content = _input;
        mqttInputState = 3;
        printlnMsg("Enter \"retained\"(true OR false)");
        break;
      }
    case 3:
      {
        if (_input == "true") {
          mqtt_publish_retained = true;
        } else {
          mqtt_publish_retained = false;
        }

        client.publish(mqtt_publish_topic.c_str(), mqtt_publish_content.c_str(), mqtt_publish_retained);
        mqttInputState = 0;
        mqtt_waitingSecondInput = false;
        mqtt_firstInput = 0;
        displayMenu_mqtt();
      }
  }  //end of switcg(mqttInputState)
}  // end of handleSecondInput_mqtt

/////////////////////////////////////

void handleInput_mqtt_ws(String input) {
  if (input == "x") {
    // if (mqttHasSubscribeTopic) {
    //   wsMqttClient.unsubscribe(mqtt_topic);
    //   mqttHasSubscribeTopic = false;
    //   displayMenu_mqtt();
    // } else {
    currentChoice = 0;
    wsMqttClient.disconnect();
    shouldMqttConnect_WS = false;
    displayMenu();
    // }
    return;
  } else if (input == "1") {  //Subscribe
    printlnMsg("Enter \"topic\" (example: exampleTopic/1): ");
    mqtt_ws_firstInput = 1;
    mqtt_ws_waitingSecondInput = true;
  } else if (input == "2") {  //Publish
    // printlnMsg("Enter \"topic\", \"message\" & \"shouldRetain\"(optional), parameters should be separated by comma: ");
    printlnMsg("Enter \"topic\" (example: exampleTopic/1): ");
    mqtt_ws_firstInput = 2;
    mqtt_ws_waitingSecondInput = true;
  } else {
    printlnMsg("Invalid input");
    displayMenu_mqtt();
  }
}

void handleSecondInput_mqtt_ws(String _input) {
  switch (mqttInputState) {
    case 0:
      {
        if (mqtt_ws_firstInput == 1) {  //Subscribe
                                        // client.subscribe(_input.c_str());
          wsMqttClient.subscribe(_input, [](const String& payload, const size_t size) {
            Serial.println("Subcribed topic has new message!");
          });
          mqttHasSubscribeTopic = true;
          // mqtt_topic = _input;
          mqtt_topics.push_back(_input);
          mqttInputState = 1;
          printlnMsg("Subscribed topic \"" + _input + "\". You may enter extra topic to subscribe OR press \"x\" to go back MQTT menu");
        } else if (mqtt_ws_firstInput == 2) {  //Publish
          mqtt_publish_topic = _input;
          mqttInputState = 2;
          printlnMsg("Enter \"content\" (example: {\"data1\":1234, \"data2\":5678}):");
        }
        break;
      }  //end of case: 0
    case 1:
      {
        if (_input == "x") {
          mqttInputState = 0;
          mqtt_ws_waitingSecondInput = false;
          mqtt_ws_firstInput = 0;
          for (uint8_t i = 0; i < mqtt_topics.size(); i++) {
            wsMqttClient.unsubscribe(mqtt_topics[i].c_str());
          }
          mqtt_topics.clear();
          displayMenu_mqtt();
          return;
        }
        wsMqttClient.subscribe(_input, [](const String& payload, const size_t size) {
          Serial.println("Subcribed topic has new message!");
        });
        mqtt_topics.push_back(_input);
        mqttHasSubscribeTopic = true;
        printlnMsg("Subscribed topic \"" + _input + "\". You may enter extra topic to subscribe OR press \"x\" to go back MQTT menu");
        break;
      }
    case 2:
      {
        mqtt_publish_content = _input;
        mqttInputState = 3;
        printlnMsg("Enter \"retained\"(true OR false)");
        break;
      }
    case 3:
      {
        if (_input == "true") {
          mqtt_publish_retained = true;
        } else {
          mqtt_publish_retained = false;
        }

        // client.publish(mqtt_publish_topic.c_str(), mqtt_publish_content.c_str(), mqtt_publish_retained);
        wsMqttClient.publish(mqtt_publish_topic, mqtt_publish_content, mqtt_publish_retained);
        mqttInputState = 0;
        mqtt_ws_waitingSecondInput = false;
        mqtt_ws_firstInput = 0;
        displayMenu_mqtt();
      }
  }  //end of switcg(mqttInputState)
}

void handleInput_dfPlayer(String input) {
  if (input == "x") {
    currentChoice = 0;
    mp3Ctrl.getPlayer().stop();
    // mp3Ctrl.release();
    displayMenu();
    return;
  } else {
    int8_t input_int = input.toInt();
    if (input_int == 1) {
      mp3_firstInput = 1;
      mp3_waitingSecondInput = true;
      displaySecondMenu_dfPlayer();
    } else if (input_int == 2) {
      mp3_firstInput = 2;
      mp3_waitingSecondInput = true;
      displaySecondMenu_dfPlayer();
    } else if (input_int == 3) {
      mp3_firstInput = 3;
      mp3_waitingSecondInput = true;
      displaySecondMenu_dfPlayer();
    } else {
      printlnMsg("Invalid input");
      displayMenu_dfPlayer();
    }
  }
  // displayMenu_dfPlayer();
}

void handleSecondInput_dfPlayer(String input) {
  if (input == "x") {
    mp3_waitingSecondInput = false;
    mp3_firstInput = 0;
    // mp3Ctrl.getPlayer().stop();
    displayMenu_dfPlayer();
    return;
  }

  if (mp3_firstInput == 1) {  //play MP3
    mp3Ctrl.getPlayer().play(input.toInt());
    displaySecondMenu_dfPlayer();
  } else if (mp3_firstInput == 2) {  //set volume
    mp3Ctrl.getPlayer().volume(input.toInt());
    displaySecondMenu_dfPlayer();
  } else if (mp3_firstInput == 3) {  // index, volume, duration, loopAfterEnd, fadeInTime, fadeOutTime
    String params = input;
    params.replace(" ", "");
    int commaIndex = params.indexOf(",");                    //must exist
    int commaIndex2 = params.indexOf(",", commaIndex + 1);   //must exist
    int commaIndex3 = params.indexOf(",", commaIndex2 + 1);  //must exist
    int commaIndex4 = params.indexOf(",", commaIndex3 + 1);  //optional
    int commaIndex5 = params.indexOf(",", commaIndex4 + 1);  //optional

    if (commaIndex == -1 || commaIndex2 == -1 || commaIndex3 == -1) {
      printlnMsg("Invalid input");
      displaySecondMenu_dfPlayer();
      return;
    }

    uint16_t index = params.substring(0, commaIndex).toInt();
    uint8_t volume = params.substring(commaIndex + 1, commaIndex2).toInt();
    uint32_t duration = params.substring(commaIndex2 + 1, commaIndex3).toInt();
    uint32_t fadeInTime = 0;
    uint32_t fadeOutTime = 0;
    bool loopAfterEnd = false;
    ;
    if (commaIndex4 == -1) {
      String _loopAfterEnd = params.substring(commaIndex3 + 1);
      if (_loopAfterEnd == "true") {
        loopAfterEnd = true;
      }
    } else {
      String _loopAfterEnd = params.substring(commaIndex3 + 1, commaIndex4);
      if (_loopAfterEnd == "true") {
        loopAfterEnd = true;
      }
      if (commaIndex5 == -1) {
        fadeInTime = params.substring(commaIndex4 + 1).toInt();
      } else {
        fadeInTime = params.substring(commaIndex4 + 1, commaIndex5).toInt();
        fadeOutTime = params.substring(commaIndex5 + 1).toInt();
      }
    }

    mp3Seq_advance.clearCommand();
    mp3Seq_advance.addCommand(index, volume, duration, loopAfterEnd, fadeInTime, fadeOutTime);
    mp3Ctrl.playRelTime(mp3Seq_advance, 0, 1);
    displaySecondMenu_dfPlayer();
  }
}

#ifdef USE_VL53L0XControl
void handleInput_vl53l0x(String input) {
  if (input == "x") {
    currentChoice = 0;
    vl53l0xCtrl.release();
    i2cCtrl.release();
    displayMenu();
  }
}
#endif

#ifdef USE_UltraSonicControl
void handleInput_ultrasonic(String input) {
  if (input == "x") {
    currentChoice = 0;
    ultraSonicCtrl.stopMeasure();
    ultraSonicCtrl.release();
    displayMenu();
  }
}
#endif

// #ifdef USE_SH1106Control
void initTestdrawbitmap_sh1106(const uint8_t* bitmap, uint8_t w, uint8_t h) {
  for (uint8_t f = 0; f < NUMFLAKES; f++) {
    icons[f][XPOS] = random(sh1106Ctrl.getDisplay().width());
    icons[f][YPOS] = 0;
    icons[f][DELTAY] = random(5) + 1;
  }
}
// #endif

// #ifdef USE_SSD1306Control
void initTestdrawbitmap_ssd1306(const uint8_t* bitmap, uint8_t w, uint8_t h) {
  for (uint8_t f = 0; f < NUMFLAKES; f++) {
    icons[f][XPOS] = random(ssd1306Ctrl.getDisplay().width());
    icons[f][YPOS] = 0;
    icons[f][DELTAY] = random(5) + 1;
  }
}
// #endif

// #ifdef USE_SH1106Control
void drawBitMap_sh1106() {
  // draw each icon
  for (uint8_t f = 0; f < NUMFLAKES; f++) {
    sh1106Ctrl.getDisplay().drawBitmap(icons[f][XPOS], icons[f][YPOS], logo16_glcd_bmp, LOGO16_GLCD_WIDTH, LOGO16_GLCD_HEIGHT, WHITE);
  }
  sh1106Ctrl.getDisplay().display();
  delay(200);

  // then erase it + move it
  for (uint8_t f = 0; f < NUMFLAKES; f++) {
    sh1106Ctrl.getDisplay().drawBitmap(icons[f][XPOS], icons[f][YPOS], logo16_glcd_bmp, LOGO16_GLCD_WIDTH, LOGO16_GLCD_HEIGHT, BLACK);
    // move it
    icons[f][YPOS] += icons[f][DELTAY];
    // if its gone, reinit
    if (icons[f][YPOS] > sh1106Ctrl.getDisplay().height()) {
      icons[f][XPOS] = random(sh1106Ctrl.getDisplay().width());
      icons[f][YPOS] = 0;
      icons[f][DELTAY] = random(5) + 1;
    }
  }
}
// #endif

// #ifdef USE_SSD1306Control
void drawBitMap_ssd1306() {
  // draw each icon
  for (uint8_t f = 0; f < NUMFLAKES; f++) {
    ssd1306Ctrl.getDisplay().drawBitmap(icons[f][XPOS], icons[f][YPOS], logo16_glcd_bmp, LOGO16_GLCD_WIDTH, LOGO16_GLCD_HEIGHT, WHITE);
  }
  ssd1306Ctrl.getDisplay().display();
  delay(200);

  // then erase it + move it
  for (uint8_t f = 0; f < NUMFLAKES; f++) {
    ssd1306Ctrl.getDisplay().drawBitmap(icons[f][XPOS], icons[f][YPOS], logo16_glcd_bmp, LOGO16_GLCD_WIDTH, LOGO16_GLCD_HEIGHT, BLACK);
    // move it
    icons[f][YPOS] += icons[f][DELTAY];
    // if its gone, reinit
    if (icons[f][YPOS] > ssd1306Ctrl.getDisplay().height()) {
      icons[f][XPOS] = random(ssd1306Ctrl.getDisplay().width());
      icons[f][YPOS] = 0;
      icons[f][DELTAY] = random(5) + 1;
    }
  }
}
// #endif

int extractValues_int(String input, char delimiter, int* values, uint8_t expectedNumberOfInput) {
  int startPos = 0;
  int endPos = 0;
  int index = 0;

  while ((endPos = input.indexOf(delimiter, startPos)) != -1) {
    // Extract the value between startPos and endPos
    String value = input.substring(startPos, endPos);

    // Remove any unnecessary spaces from the extracted value
    value.trim();

    // Store the extracted value into the array
    values[index++] = value.toInt();

    // Update startPos to the position after the delimiter
    startPos = endPos + 1;

    // Break if the maximum number of values is reached
    if (index >= expectedNumberOfInput) {
      return -1;
    }
  }

  // Extract the last value after the last delimiter
  String value = input.substring(startPos);
  value.trim();

  // Store the last extracted value into the array if there's space
  if (index < expectedNumberOfInput) {
    values[index++] = value.toInt();
  }

  // Return the number of values extracted
  return index;
}

int extractValues_double(String input, char delimiter, double* values, uint8_t expectedNumberOfInput) {
  int startPos = 0;
  int endPos = 0;
  int index = 0;

  while ((endPos = input.indexOf(delimiter, startPos)) != -1) {
    // Extract the value between startPos and endPos
    String value = input.substring(startPos, endPos);

    // Remove any unnecessary spaces from the extracted value
    value.trim();

    // Store the extracted value into the array
    values[index++] = value.toDouble();

    // Update startPos to the position after the delimiter
    startPos = endPos + 1;

    // Break if the maximum number of values is reached
    if (index >= expectedNumberOfInput) {
      return -1;
    }
  }

  // Extract the last value after the last delimiter
  String value = input.substring(startPos);
  value.trim();

  // Store the last extracted value into the array if there's space
  if (index < expectedNumberOfInput) {
    values[index++] = value.toDouble();
  }

  // Return the number of values extracted
  return index;
}

int extractValues_ulong(String input, char delimiter, uint32_t* values, uint8_t expectedNumberOfInput) {
  int startPos = 0;
  int endPos = 0;
  int index = 0;

  while ((endPos = input.indexOf(delimiter, startPos)) != -1) {
    // Extract the value between startPos and endPos
    String value = input.substring(startPos, endPos);

    // Remove any unnecessary spaces from the extracted value
    value.trim();

    // Store the extracted value into the array
    values[index++] = value.toDouble();

    // Update startPos to the position after the delimiter
    startPos = endPos + 1;

    // Break if the maximum number of values is reached
    if (index >= expectedNumberOfInput) {
      return 0;
    }
  }

  // Extract the last value after the last delimiter
  String value = input.substring(startPos);
  value.trim();

  // Store the last extracted value into the array if there's space
  if (index < expectedNumberOfInput) {
    values[index++] = value.toDouble();
  }

  // Return the number of values extracted
  return index;
}

void handleMsg(String input) {
  input.replace(" ", "");
  if (currentChoice == 0) {
    if (input != "\n") {
      bool isChoiceValid = true;

      int choice = input.toInt();

      switch (choice) {
        case 1:
          {
            testcase_downloadInitFile();
            isChoiceValid = false;
            break;
          }
        case 2:
          {
            testcase_mpr121();
            break;
          }
        case 3:
          {
            if (displayType == 1) {
              printlnMsg("Enter the \"width\", \"height\" and \"I2C address\" of SH1106 (separate by comma) [example: 128,64,3c]: ");
              waitForUserInput(testcase_sh1106);
              break;
            } else {
              printlnMsg("Invalid choice. Please try again.");
              isChoiceValid = false;
              break;
            }
          }
        case 4:
          {
            if (displayType == 2) {
              printlnMsg("Enter the \"width\", \"height\" and \"I2C address\" of SSD1306 (separate by comma) [example: 128,64,3c]: ");
              waitForUserInput(testcase_ssd1306);
              break;
            } else {
              printlnMsg("Invalid choice. Please try again.");
              isChoiceValid = false;
              break;
            }
          }
        case 5:
          {
            printlnMsg("Enter the \"pin number\" and \"number of LEDs\" (separate by comma): ");
            waitForUserInput(testcase_neopixel);
            break;
          }
        case 6:
          {
            printlnMsg("Enter the pin number(s) of Servo (up to 6 pins, with comma separation):");
            waitForUserInput(testcase_servo);
            break;
          }
        case 7:
          {
            printlnMsg("Enter the pin number of Tone:");
            waitForUserInput(testcase_tone);
            break;
          }
        case 8:
          {
            printlnMsg("Enter the pin number(s) of PWM (up to 6 pins, with comma separation):");
            waitForUserInput(testcase_pwm);
            break;
          }
        case 9:
          {
            printlnMsg("Enter the pin number of ADC:");
            waitForUserInput(testcase_adc);
            break;
          }
        case 10:
          {
            printlnMsg("Enter the pin number and mode(optional, separated by comma) for GPIO In (mode: 0 for INPUT, 1 for INPUT_PULLUP, default is INPUT, e.g. '9,1'):");
            waitForUserInput(testcase_gpioIn);
            break;
          }
        case 11:
          {
            printlnMsg("Enter the pin Number and initial state(optional, separated by comma) for GPIO Out (initial state: 0 for LOW, 1 for HIGH, default is LOW, e.g. '12,1'):");
            waitForUserInput(testcase_gpioOut);
            break;
          }
        case 12:
          {
            printlnMsg("Enter the SSID and password of WiFi AP to connect (separated by comma):");
            waitForUserInput(testcase_wifi);
            break;
          }
        case 13:
          {
#ifdef USE_HTTPClientControl
            if (!wifiCtrl.isInit()) {
              printlnMsg("WiFiControl is not initialized. Please use function 12 to connect WiFi first.");
              currentChoice = 0;
              displayMenu();
              return;
            }

            httpClientCtrl.release();
            printlnMsg("Enter the \"address\" & \"port\"(optional) & \"is secure\"(true OR false) for HTTP Request (separated by comma) (example: [data.weather.gov.hk,true] / [192.168.0.1,3000,false]):");
            waitForUserInput(testcase_http);
            break;
#else
            printlnMsg("Invalid choice. Please try again.");
            isChoiceValid = false;
            break;
#endif
          }
        case 14:
          {
            if (!wifiCtrl.isInit()) {
              printlnMsg("WiFiControl is not initialized. Please use function 12 to connect WiFi first.");
              currentChoice = 0;
              displayMenu();
              return;
            }

            printlnMsg("Enter the \"address\" and \"port\" of MQTT broker (separated by comma) (example: broker.hivemq.com,1883):");
            waitForUserInput(testcase_mqtt);
            break;
          }
        case 15:
          {
            if (!wifiCtrl.isInit()) {
              printlnMsg("WiFiControl is not initialized. Please use function 12 to connect WiFi first.");
              currentChoice = 0;
              displayMenu();
              return;
            }

            printlnMsg("Enter the \"address\" and \"port\" of MQTT broker (separated by comma) (example: mqtt.designandmake.org,80):");
            waitForUserInput(testcase_mqtt_ws);
            break;
          }
        case 16:
          {
            mp3Ctrl.release();
            hwUartCtrl.release();
            printlnMsg("Enter the \"pin number of RX\", \"pin number of TX\" and \"pin number of Busy\"(separated in comma) which are connected to DFPlayer mini:");
            waitForUserInput(testcase_dfPlayer);
            break;
          }
        case 17:
          {
#ifdef USE_VL53L0XControl
            printlnMsg("Enter the \"pin number of SCL\" and \"pin number of SDA\" (separated in comma):");
            waitForUserInput(testcase_vl53l0x);
            break;
#else
            printlnMsg("Invalid choice. Please try again.");
            isChoiceValid = false;
            break;
#endif
          }
        case 18:
          {
            testcase_listFile();
            isChoiceValid = false;
            break;
          }
        case 19:
          {
            mp3Ctrl.release();
            hwUartCtrl.release();
            testcase_testMode();
            isChoiceValid = false;
            break;
          }
        case 20:
          {
            mp3Ctrl.release();
            hwUartCtrl.release();
            testcase_sequence();
            isChoiceValid = false;
            break;
          }
        case 21:
          {
#ifdef USE_LiquidCrystal
            printlnMsg("Enter the \"pin number of SCL\" and \"pin number of SDA\" (separated in comma):");
            waitForUserInput(testcase_lcd1602);
            isChoiceValid = false;
            break;
#else
            printlnMsg("Invalid choice. Please try again.");
            isChoiceValid = false;
            break;
#endif
          }
        case 22:
          {
#ifdef USE_UltraSonicControl
            printlnMsg("Enter the \"pin number of trig\" and \"pin number of echo\" (separated in comma):");
            waitForUserInput(testcase_ultrasonic);
            break;
#else
            printlnMsg("Invalid choice. Please try again.");
            isChoiceValid = false;
            break;
#endif
          }

        case 23:
          {
            printlnMsg("Select a display type:");
            printlnMsg("1: SH1106");
            printlnMsg("2: SSD1306");
            printlnMsg("x: return");
            waitForUserInput(testcase_selectDisplay);
            break;
          }
        default:
          {
            printlnMsg("Invalid choice. Please try again.");
            isChoiceValid = false;
          }
      }

      if (isChoiceValid) {
        currentChoice = choice;
      }
    }
  } else if (currentChoice == 2) {  //mpr121
    handleInput_mpr121(input);
  } else if (currentChoice == 3) {  //sh1106
    if (displayType == 1) {
      handleInput_sh1106(input);
    }
  } else if (currentChoice == 4) {  //ssd1306
    if (displayType == 2) {
      handleInput_ssd1306(input);
    }
  } else if (currentChoice == 5) {  //addrLed
    handleInput_addrLed(input);
  } else if (currentChoice == 6) {
    handleInput_servo(input);
  } else if (currentChoice == 7) {
    handleInput_tone(input);
  } else if (currentChoice == 8) {
    handleInput_pwm(input);
  } else if (currentChoice == 9) {
    handleInput_adc(input);
  } else if (currentChoice == 10) {
    handleInput_gpioIn(input);
  } else if (currentChoice == 11) {
    handleInput_gpioOut(input);
  } else if (currentChoice == 13) {
#ifdef USE_HTTPClientControl
    handleInput_http(input);
#endif
  } else if (currentChoice == 14) {
    handleInput_mqtt(input);
  } else if (currentChoice == 15) {
    handleInput_mqtt_ws(input);
  } else if (currentChoice == 16) {
    handleInput_dfPlayer(input);
  } else if (currentChoice == 17) {
#ifdef USE_VL53L0XControl
    handleInput_vl53l0x(input);
#endif
  } else if (currentChoice == 19) {
    handleInput_testMode(input);
  } else if (currentChoice == 20) {
    handleInput_sequence(input);
  } else if (currentChoice == 21) {
#ifdef USE_LiquidCrystal
    handleInput_lcd1602(input);
#endif
  } else if (currentChoice == 22) {
#ifdef USE_UltraSonicControl
    handleInput_ultrasonic(input);
#endif
  }
  //==================
}

void printlnMsg() {
  Serial.println();
  if (isWsConnected) {
    webSocketServer->broadcastTXT("\n");
  }
}

void printMsg(String msg) {
  Serial.print(msg);
  if (isWsConnected) {
    webSocketServer->broadcastTXT(msg);
  }
}

void printlnMsg(String msg) {
  Serial.println(msg);
  if (isWsConnected) {
    webSocketServer->broadcastTXT(msg + "\n");
  }
}

void printMsg(int msg) {
  Serial.print(msg);
  if (isWsConnected) {
    String wsMsg = String(msg);
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void printlnMsg(int msg) {
  Serial.println(msg);
  if (isWsConnected) {
    String wsMsg = String(msg) + "\n";
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void printMsg(double msg) {
  Serial.print(msg);
  if (isWsConnected) {
    String wsMsg = String(msg);
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void printlnMsg(double msg) {
  Serial.println(msg);
  if (isWsConnected) {
    String wsMsg = String(msg) + "\n";
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void printMsg(uint32_t msg) {
  Serial.print(msg);
  if (isWsConnected) {
    String wsMsg = String(msg);
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void printlnMsg(uint32_t msg) {
  Serial.println(msg);
  if (isWsConnected) {
    String wsMsg = String(msg) + "\n";
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void printMsg(int32_t msg) {
  Serial.print(msg);
  if (isWsConnected) {
    String wsMsg = String(msg);
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void printlnMsg(int32_t msg) {
  Serial.println(msg);
  if (isWsConnected) {
    String wsMsg = String(msg) + "\n";
    webSocketServer->broadcastTXT(wsMsg);
  }
}

void saveSequenceSetting() {
  // Create a JSON document
  DynamicJsonDocument doc(256);
  JsonArray array = doc.createNestedArray("mpr121_seq_mapping");
  for (int i = 0; i < 12; i++) {
    array.add(mpr121_seq_mapping[i]);
  }
  doc["mpr121_seq_mode"] = mpr121_seq_mode;

  // Open the file for writing
  File file = LittleFS.open("/sequenceSetting.json", "w");
  if (!file) {
    Serial.println("Failed to open file for writing");
    return;
  }

  // Serialize JSON to file
  if (serializeJson(doc, file) == 0) {
    Serial.println("Failed to write to file");
  }

  // Close the file
  file.close();
}

// Function to load data from JSON file
void loadSequenceSetting() {
  // Check if the file exists
  if (!LittleFS.exists("/sequenceSetting.json")) {
    // Serial.println("JSON file does not exist");
    return;
  }

  // Open the file for reading
  File file = LittleFS.open("/sequenceSetting.json", "r");
  if (!file) {
    Serial.println("Failed to open file for reading");
    return;
  }

  // Allocate a JSON document
  DynamicJsonDocument doc(256);

  // Deserialize the JSON document
  DeserializationError error = deserializeJson(doc, file);
  if (error) {
    Serial.print("Failed to read file, using default configuration: ");
    Serial.println(error.c_str());
    return;
  }

  // Read values from JSON
  JsonArray array = doc["mpr121_seq_mapping"];
  for (int i = 0; i < array.size(); i++) {
    mpr121_seq_mapping[i] = array[i];
  }
  mpr121_seq_mode = doc["mpr121_seq_mode"];

  // Close the file
  file.close();
}

bool isAllFinish_testMode() {
  if (addrLedCtrl.seqObjs.size() == 0) {
    return false;
  }
  bool isAddrLedFinished = true;
  for (int i = 0; i < addrLedCtrl_0.seqObjs.size(); i++) {
    if (addrLedCtrl_0.seqObjs[i] != nullptr) {
      isAddrLedFinished = false;
      return false;
    }
  }

  if (servoCtrl[0].isPlaying()) {
    return false;
  }

  if (servoCtrl[1].isPlaying()) {
    return false;
  }

  if (mp3Ctrl.isPlaying()) {
    return false;
  }

  return true;
}

void saveDisplayType(uint8_t _type) {
  JsonDocument doc;
  doc["type"] = _type;
  File file = LittleFS.open("/display.json", "w");
  serializeJson(doc, file);
  file.close();
}
