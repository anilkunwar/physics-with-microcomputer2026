#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>

// Wi-Fi Credentials
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// DHT Configuration
#define DHTPIN 4           // GPIO pin connected to DATA
#define DHTTYPE DHT22      // Change to DHT11 if using a DHT11 sensor

DHT dht(DHTPIN, DHTTYPE);
WebServer server(80);

void handleSensorData() {
  float temperature = dht.readTemperature(); // Celsius
  float humidity = dht.readHumidity();        // Percentage %

  // Check if reading failed
  if (isnan(temperature) || isnan(humidity)) {
    server.send(500, "application/json", "{\"error\": \"Failed to read from DHT sensor\"}");
    return;
  }

  // Build JSON response
  String json = "{";
  json += "\"temperature\": " + String(temperature, 1) + ",";
  json += "\"humidity\": " + String(humidity, 1);
  json += "}";

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

  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/sensor", handleSensorData);
  server.begin();
}

void loop() {
  server.handleClient();
}
