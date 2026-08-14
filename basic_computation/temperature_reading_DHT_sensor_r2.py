#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>

// Pin Definitions for ESP32-S3
#define DHTPIN 4       // GPIO pin connected to DHT22 data pin
#define DHTTYPE DHT22  

// WiFi Credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WebServer server(80);
DHT dht(DHTPIN, DHTTYPE);

void handleSensor() {
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  String json = "{";
  
  if (isnan(t) || isnan(h)) {
    json += "\"error\": \"Failed to read from DHT sensor!\"";
    server.send(500, "application/json", json + "}");
    return;
  }

  json += "\"temperature\": " + String(t, 2) + ", ";
  json += "\"humidity\": " + String(h, 2);
  json += "}";

  // Add CORS header so Streamlit can fetch it without issues
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP: " + WiFi.localIP().toString());

  server.on("/sensor", handleSensor);
  server.begin();
}

void loop() {
  server.handleClient();
}
