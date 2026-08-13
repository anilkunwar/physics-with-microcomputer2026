# How to Download and Install Arduino IDE 2

The reason you cannot find the **"Additional Boards Manager URLs"** field in your Preferences window is because you are currently running an **outdated version of Arduino IDE** (likely version 1.0.x installed from the standard Ubuntu package repository).

You can confirm this by looking at your Preferences menu: options like *“Update sketch files to new extension on save (.pde -> .ino)”* only existed in the legacy 1.0.x versions before the **Boards Manager** feature was introduced in modern releases. The ESP32-S3 cannot be programmed on this version.

---

### 🚀 **Solution: Install Arduino IDE 2.x**

To program your ESP32-S3, you'll need to upgrade to a modern version of the IDE:

#### **Step 1: Download the Modern IDE**

1. Open your browser and go to the official website: [arduino.cc/en/software](https://www.arduino.cc/en/software).
2. Under **Arduino IDE 2.x**, download the **Linux AppImage** (64-bit) file.

#### **Step 2: Make it Executable and Run**

1. Open your **Terminal** and navigate to your `Downloads` folder:
```bash
cd ~/Downloads

```


2. Grant execution permissions to the downloaded file:
```bash
chmod +x arduino-ide_*_Linux_64bit.AppImage

```


3. Launch the IDE:
```bash
./arduino-ide_*_Linux_64bit.AppImage

```



---

### **Step 3: Add ESP32 Support in Arduino IDE 2.x**

Once the new version opens:

1. Press `Ctrl + ,` (or go to **File > Preferences**).
2. You will now see the **"Additional Boards Manager URLs"** field near the bottom.
3. Paste the URL:
```text
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

```


4. Click **OK**, then open **Boards Manager** (`Ctrl + Shift + B`), search for **esp32**, and click **Install**.
