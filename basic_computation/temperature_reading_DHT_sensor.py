import streamlit as st
import requests

ESP32_IP = "http://192.168.0.104"

st.set_page_config(page_title="ESP32-S3 Environment Monitor", page_icon="🌡️")

st.title("🌡️ ESP32-S3 Real Sensor Dashboard")
st.caption(f"Targeting ESP32 at: `{ESP32_IP}`")

st.divider()

if st.button("🔄 Read DHT Sensor Data", use_container_width=True):
    try:
        response = requests.get(f"{ESP32_IP}/sensor", timeout=3)
        data = response.json()
        
        if response.status_code == 200:
            col1, col2 = st.columns(2)
            col1.metric(label="Temperature", value=f"{data['temperature']} °C")
            col2.metric(label="Humidity", value=f"{data['humidity']} %")
        else:
            # Displays the specific error returned from ESP32
            st.warning(data.get("error", "ESP32 server returned an error."))
            
    except requests.exceptions.RequestException as e:
        st.error(f"Cannot connect to ESP32: {e}")
