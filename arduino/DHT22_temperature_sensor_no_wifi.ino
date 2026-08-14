#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22   // DHT22 (or DHT11)

DHT dht(DHTPIN, DHTTYPE);   // Constructor with pin and type

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("\n=== DHT22 Test (No WiFi) ===");
  dht.begin();   // Adafruit uses begin()
}

void loop() {
  float temp = dht.readTemperature();   // readTemperature() not getTemperature()
  float hum = dht.readHumidity();

  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print(" °C, Hum: ");
  Serial.print(hum);
  Serial.println(" %");

  if (isnan(temp) || isnan(hum)) {
    Serial.println("⚠️ Read failed – check wiring!");
  }

  delay(2000);
}
