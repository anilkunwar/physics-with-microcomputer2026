import streamlit as st
import requests

# Set your ESP32's assigned IP Address
ESP32_IP = "http://192.168.0.104"

st.set_page_config(page_title="ESP32-S3 Local Dashboard", page_icon="📡", layout="centered")

st.title("📡 ESP32-S3 Local Wi-Fi Control")
st.caption(f"Connected to ESP32 at: `{ESP32_IP}`")

st.divider()

# --- Section 1: Read Sensor Data ---
st.header("📊 Sensor Monitoring")

if st.button("🔄 Read Sensor Data", use_container_width=True):
    try:
        response = requests.get(f"{ESP32_IP}/sensor", timeout=3)
        if response.status_code == 200:
            data = response.json()
            st.metric(label="Current Temperature", value=f"{data['temperature']} °C")
        else:
            st.error("Failed to retrieve data from ESP32.")
    except requests.exceptions.RequestException as e:
        st.error(f"Cannot connect to ESP32. Check Wi-Fi connection.\n\nError: {e}")

st.divider()

# --- Section 2: Send Commands to ESP32 ---
st.header("🎛️ Hardware Control")

col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 Turn LED ON", use_container_width=True):
        try:
            res = requests.get(f"{ESP32_IP}/led/on", timeout=3)
            st.success(res.text)
        except Exception as e:
            st.error(f"Connection error: {e}")

with col2:
    if st.button("🔴 Turn LED OFF", use_container_width=True):
        try:
            res = requests.get(f"{ESP32_IP}/led/off", timeout=3)
            st.info(res.text)
        except Exception as e:
            st.error(f"Connection error: {e}")
