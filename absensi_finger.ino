#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <Adafruit_Fingerprint.h>
#include <PubSubClient.h>

// ================= OLED =================
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define BUTTON_DAFTAR 18
#define BUTTON_ABSEN 19

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// ================= WIFI =================
const char* ssid = "KOJUWA";
const char* password = "butterscotch";

// ================= MQTT =================
const char* mqtt_server = ""; // ganti IP laptop kamu
const char* topic = "esp/sensor";

WiFiClient espClient;
PubSubClient client(espClient);

// ================= FINGERPRINT =================
HardwareSerial mySerial(2);
#define FINGER_RX 16
#define FINGER_TX 17

Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

// ================= FLAGS =================
bool sensorReady = false;

// ================= SETUP =================
void setup() {
  Serial.begin(115200);

  // OLED INIT
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED gagal");
    while (1);
  }

  tampilkanAwal();

  // WIFI CONNECT
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    tampilkanConnecting();
  }

  Serial.println("\nWiFi Connected");

  // MQTT SETUP
  client.setServer(mqtt_server, 1883);

  // FINGERPRINT INIT
  mySerial.begin(57600, SERIAL_8N1, FINGER_RX, FINGER_TX);
  finger.begin(57600);

  if (finger.verifyPassword()) {
    Serial.println("Sensor OK");
    sensorReady = true;
    tampilkanSensorOK();

    // kirim status ke MQTT
    client.connect("ESP32_SENSOR");
    client.publish(topic, "sensor_ok");
  } else {
    Serial.println("Sensor ERROR");
    tampilkanSensorError();

    client.connect("ESP32_SENSOR");
    client.publish(topic, "sensor_error");

    while (1);
  }
}

// ================= LOOP =================
void loop() {

  if (!client.connected()) {
    reconnectMQTT();
  }

  client.loop();
}

// ================= MQTT RECONNECT =================
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("MQTT reconnect...");

    if (client.connect("ESP32_SENSOR")) {
      Serial.println("connected");
    } else {
      Serial.println("failed");
      delay(2000);
    }
  }
}

// ================= OLED =================
void tampilkanAwal() {
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(10, 10);
  display.println("BOOT");
  display.display();
}

void tampilkanConnecting() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(10, 20);
  display.println("Connecting WiFi");
  display.display();
}

void tampilkanSensorOK() {
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(10, 20);
  display.println("SENSOR OK");
  display.display();
}

void tampilkanSensorError() {
  display.clearDisplay();
  display.setTextSize(2);
  display.setCursor(10, 20);
  display.println("ERROR");
  display.display();
}