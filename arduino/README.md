# How to Download and Install Arduino IDE 2 (Along with Addition of ESP32 Support)
### **Step-by-Step: Upgrading to Arduino IDE 2.x on Ubuntu**

Since AppImages run as self-contained executables without modifying system libraries, installing the modern IDE is quick and won't conflict with older packages.

---

### **Step 1: Install Required Dependencies**

Modern AppImages in Ubuntu require `libfuse2` to run. Open your Ubuntu Terminal (`Ctrl + Alt + T`) and run:

```bash
sudo apt update && sudo apt install libfuse2 -y

```

*(If you are on Ubuntu 24.04 or newer, run `sudo apt install libfuse2t64 -y` instead.)*

---

### **Step 2: Download the New IDE**

1. Open your browser and go to the official website: **[arduino.cc/en/software](https://www.arduino.cc/en/software)**.
2. Under **Arduino IDE 2.x**, click on **Linux AppImage 64 bits (x86-64)**.
3. Save the `.AppImage` file to your **Downloads** folder.

---

### **Step 3: Make it Executable & Launch**

#### **Method A: Via Terminal (Fastest)**

1. Move into your `Downloads` directory:
```bash
cd ~/Downloads

```


2. Grant execution permissions:
```bash
chmod +x arduino-ide_*_Linux_64bit.AppImage

```


3. Launch the IDE:
```bash
./arduino-ide_*_Linux_64bit.AppImage

```


#### **Method B: Via Graphical Interface (GUI)**

1. Open your **Files** manager and open the **Downloads** folder.
2. Right-click the `arduino-ide_...AppImage` file and choose **Properties**.
3. Go to the **Permissions** tab and check the box that says **"Allow executing file as program"**.
4. Close the window, then **double-click** the AppImage file to run it.

---

### **Step 4: Add ESP32 Support in Arduino IDE 2.x**

Now that you have the updated IDE running:

1. Press **`Ctrl + ,`** (or go to **File > Preferences**).
2. Look near the bottom for **"Additional Boards Manager URLs"**.
3. Paste the official Espressif board package link:
```text
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

```


4. Click **OK**.
5. Click the **Boards Manager** icon on the left sidebar (or press `Ctrl + Shift + B`), search for **`esp32`**, and click **Install**.


# Running Arduino IDE with Alias


### **1. Set Up the Bash Alias**

Run this command in your terminal to create the `arduino` shortcut pointing directly to your exact folder location:

```bash
echo "alias arduino='~/workstation/softwares/arduino/arduino-ide_2.3.10_Linux_64bit.AppImage &'" >> ~/.bashrc

```

Then, reload your configuration:

```bash
source ~/.bashrc

```

---

### **2. Launch Arduino IDE**

Now you can open the IDE from any directory in your terminal by typing:

```bash
arduino

```

*(The `&` keeps the IDE running in the background so your terminal prompt stays free!)*


Prerequisites & N16R8 Settings
Before uploading code, ensure these board parameters are configured in Tools:

Board: ESP32S3 Dev Module (already selected in your top bar)

Port: Select your device path (e.g., /dev/ttyACM0 or /dev/ttyUSB0)

Flash Size: 16MB (128Mb)

PSRAM: OPI PSRAM

USB CDC On Boot: Enabled

# Connecting ESP32 to WiFi

That default template is generated every time you open a new sketch in Arduino.

To replace `sketch_monthDDa.ino` with the Wi-Fi connection code, simply **copy the code below**, select everything inside your Arduino IDE editor window (`Ctrl + A`), and paste it in (`Ctrl + V`):

```cpp
#include <WiFi.h>

// Replace with your 2.4 GHz Wi-Fi credentials
const char* ssid     = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

void setup() {
  // Start serial communication at 115200 baud
  Serial.begin(115200);
  delay(1000); 

  Serial.println("\n--- ESP32-S3 Wi-Fi Setup ---");
  
  // Set ESP32 to Station (client) mode
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.print("Connecting to: ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Print dots while waiting to connect
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected successfully!");
  Serial.print("IP address assigned: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Main code runs repeatedly after setup completes
}

```

---

### **Next Steps to Test It:**

1. Update `"YOUR_WIFI_SSID"` and `"YOUR_WIFI_PASSWORD"` with your actual Wi-Fi details.
2. Click the **Upload Arrow (`->`)** at the top-left of the IDE.
3. Once finished, click the **Serial Monitor** icon (top-right corner, looks like a magnifying glass) and make sure the baud rate dropdown at the bottom right of the monitor tab is set to **`115200 baud`**.
