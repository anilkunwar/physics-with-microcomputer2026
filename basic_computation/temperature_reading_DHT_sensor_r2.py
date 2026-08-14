import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ------------------- Page Configuration -------------------
st.set_page_config(page_title="ESP32-S3 Digital Twin", page_icon="🌡️", layout="wide")

# ------------------- Helper Functions -------------------
def init_state():
    """Initialize session state variables."""
    if "temp_data" not in st.session_state:
        st.session_state.temp_data = []
    if "hum_data" not in st.session_state:
        st.session_state.hum_data = []
    if "time_data" not in st.session_state:
        st.session_state.time_data = []
    if "monitoring" not in st.session_state:
        st.session_state.monitoring = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "last_temp" not in st.session_state:
        st.session_state.last_temp = None
    if "last_hum" not in st.session_state:
        st.session_state.last_hum = None

init_state()

# ------------------- Sidebar Control Panel -------------------
st.sidebar.title("⚙️ Digital Twin Control")
ESP32_IP = st.sidebar.text_input("ESP32 IP Address", "http://192.168.0.104")
poll_interval = st.sidebar.slider("Polling Interval (seconds)", 1, 10, 2)
max_points = st.sidebar.slider("Max Data Points in Memory", 20, 500, 100)

# Start/Stop Monitoring
if st.sidebar.button("🟢 Start Monitoring" if not st.session_state.monitoring else "🔴 Stop Monitoring", use_container_width=True):
    st.session_state.monitoring = not st.session_state.monitoring
    if st.session_state.monitoring and st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    st.rerun()

# Manual Clear Data
if st.sidebar.button("🗑️ Clear Data", use_container_width=True):
    st.session_state.temp_data.clear()
    st.session_state.hum_data.clear()
    st.session_state.time_data.clear()
    st.session_state.start_time = None
    st.session_state.last_temp = None
    st.session_state.last_hum = None
    st.rerun()

# ------------------- Auto-Refresh Logic -------------------
# If monitoring is active, trigger a rerun every X seconds
if st.session_state.monitoring:
    st_autorefresh(interval=poll_interval * 1000, key="esp32poll")

# ------------------- Data Fetching -------------------
if st.session_state.monitoring:
    try:
        # Append timestamp count (seconds since monitoring started)
        elapsed_time = time.time() - st.session_state.start_time
        
        response = requests.get(f"{ESP32_IP}/sensor", timeout=3)
        data = response.json()
        
        if response.status_code == 200:
            temp = data.get('temperature')
            hum = data.get('humidity')
            
            # Save previous value to calculate deltas
            st.session_state.last_temp = st.session_state.temp_data[-1] if st.session_state.temp_data else temp
            st.session_state.last_hum = st.session_state.hum_data[-1] if st.session_state.hum_data else hum
            
            st.session_state.temp_data.append(temp)
            st.session_state.hum_data.append(hum)
            st.session_state.time_data.append(elapsed_time)
            
            # Trim data to prevent memory overflow
            if len(st.session_state.temp_data) > max_points:
                st.session_state.temp_data.pop(0)
                st.session_state.hum_data.pop(0)
                st.session_state.time_data.pop(0)
        else:
            st.sidebar.error(f"ESP32 Error: {data.get('error', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Connection lost: {e}")
        st.session_state.monitoring = False
        st.rerun()

# ------------------- Dashboard UI -------------------
st.title("🌡️ ESP32-S3 Digital Twin Dashboard")
st.caption(f"Real-time telemetry streaming from: `{ESP32_IP}/sensor`")

# Status Indicator
status_col1, status_col2 = st.columns([1, 3])
with status_col1:
    if st.session_state.monitoring:
        st.markdown("🟢 **LIVE STREAMING**")
    else:
        st.markdown("🔴 **IDLE / STOPPED**")

# Top Metrics
df = pd.DataFrame({
    "Time (s)": st.session_state.time_data,
    "Temperature (°C)": st.session_state.temp_data,
    "Humidity (%)": st.session_state.hum_data
})

col1, col2, col3, col4 = st.columns(4)
current_temp = df["Temperature (°C)"].iloc[-1] if not df.empty else 0
current_hum = df["Humidity (%)"].iloc[-1] if not df.empty else 0
delta_temp = current_temp - st.session_state.last_temp if st.session_state.last_temp is not None else 0
delta_hum = current_hum - st.session_state.last_hum if st.session_state.last_hum is not None else 0

col1.metric("Current Temperature", f"{current_temp} °C", delta=f"{delta_temp:.2f} °C")
col2.metric("Current Humidity", f"{current_hum} %", delta=f"{delta_hum:.2f} %")
col3.metric("Data Points Logged", len(st.session_state.temp_data))
col4.metric("Session Time", f"{int(st.session_state.time_data[-1])}s" if not df.empty else "0s")

st.divider()

# ------------------- Visualizations -------------------
if df.empty:
    st.info("Awaiting telemetry data... Press 'Start Monitoring' in the sidebar.")
else:
    # Row 1: Time Series Curves
    st.subheader("📈 Real-Time Time Series Curves")
    curve_col1, curve_col2 = st.columns(2)
    
    with curve_col1:
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=df["Time (s)"], y=df["Temperature (°C)"], 
                                      mode='lines+markers', name='Temperature',
                                      line=dict(color='firebrick', width=2)))
        fig_temp.update_layout(title="Temperature over Time", xaxis_title="Time (seconds)", yaxis_title="°C", template="plotly_dark")
        st.plotly_chart(fig_temp, use_container_width=True)
        
    with curve_col2:
        fig_hum = go.Figure()
        fig_hum.add_trace(go.Scatter(x=df["Time (s)"], y=df["Humidity (%)"], 
                                     mode='lines+markers', name='Humidity',
                                     line=dict(color='royalblue', width=2)))
        fig_hum.update_layout(title="Humidity over Time", xaxis_title="Time (seconds)", yaxis_title="%", template="plotly_dark")
        st.plotly_chart(fig_hum, use_container_width=True)

    # Row 2: Histograms and Distributions
    st.subheader("📊 Statistical Distributions")
    hist_col1, hist_col2, hist_col3 = st.columns(3)
    
    with hist_col1:
        fig_hist_temp = px.histogram(df, x="Temperature (°C)", nbins=15, title="Temperature Distribution", template="plotly_dark", color_discrete_sequence=['indianred'])
        fig_hist_temp.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist_temp, use_container_width=True)
        
    with hist_col2:
        fig_hist_hum = px.histogram(df, x="Humidity (%)", nbins=15, title="Humidity Distribution", template="plotly_dark", color_discrete_sequence=['cornflowerblue'])
        fig_hist_hum.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist_hum, use_container_width=True)
        
    with hist_col3:
        # Scatter plot to show correlation
        fig_scatter = px.scatter(df, x="Temperature (°C)", y="Humidity (%)", 
                                 title="Temp vs Humidity Correlation", 
                                 template="plotly_dark", 
                                 color=df.index, 
                                 color_continuous_scale=px.colors.sequential.Viridis)
        fig_scatter.update_traces(marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')))
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Row 3: Raw Data Table
    with st.expander("Inspect Raw Telemetry Data"):
        st.dataframe(df.style.format({"Temperature (°C)": "{:.2f}", "Humidity (%)": "{:.2f}", "Time (s)": "{:.1f}"}), use_container_width=True)
