#include <WiFi.h>
#include <WebServer.h>

// Wi-Fi Credentials
const char* ssid     = "WIFI_SSID"; //
const char* password = "WIFI_PASSWORD"; // Put your Wi-Fi password here

// Create Web Server on port 80
WebServer server(80);

// Built-in LED on GPIO 2 (or change to your board's LED pin)
const int LED_PIN = 2; 

void handleRoot() {
  server.send(200, "text/plain", "ESP32-S3 Web Server Ready!");
}

// Endpoint to send sensor data to Streamlit
void handleSensorData() {
  // Simulate reading a sensor (e.g., temperature)
  float temperature = 20.0 + random(0, 100) / 10.0; 
  
  String json = "{\"temperature\": " + String(temperature, 1) + "}";
  server.send(200, "application/json", json);
}

// Endpoints to receive commands from Streamlit
void handleLedOn() {
  digitalWrite(LED_PIN, HIGH);
  server.send(200, "text/plain", "LED IS ON");
  Serial.println("Command Received: LED turned ON");
}

void handleLedOff() {
  digitalWrite(LED_PIN, LOW);
  server.send(200, "text/plain", "LED IS OFF");
  Serial.println("Command Received: LED turned OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Define HTTP Routes
  server.on("/", handleRoot);
  server.on("/sensor", handleSensorData);
  server.on("/led/on", handleLedOn);
  server.on("/led/off", handleLedOff);

  server.begin();
  Serial.println("HTTP Server Started!");
}

void loop() {
  server.handleClient(); // Keep listening for incoming HTTP requests
}
