import streamlit as st
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Security Scanner",
    page_icon="🛡️",
    layout="wide"
)

# Simple title
st.title("🛡️ Security Scanner")
st.write("Simple working version")

# Simple metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Scans", "1,247", "+12%")

with col2:
    st.metric("Threats Found", "342", "-5%")

with col3:
    st.metric("Security Score", "89%", "+3%")

with col4:
    st.metric("Active Scans", "3", "+1")

# Simple chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Critical', 'High', 'Medium']
)
st.line_chart(chart_data)

# Simple scanner
st.subheader("Scanner")
target = st.text_input("Target", "example.com")

if st.button("Start Scan"):
    with st.spinner("Scanning..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.05)
            progress_bar.progress(i + 1)
        st.success("Scan complete!")
        st.balloons()

# Simple table
st.subheader("Recent Threats")
threat_data = pd.DataFrame({
    'Time': [datetime.now().strftime('%H:%M:%S') for _ in range(5)],
    'Type': ['SQL Injection', 'XSS', 'Port Scan', 'Brute Force', 'Malware'],
    'Severity': ['Critical', 'High', 'Medium', 'High', 'Critical'],
    'Source': ['192.168.1.105', '10.0.0.23', '172.16.0.50', '45.33.22.11', '87.65.43.21']
})
st.dataframe(threat_data, use_container_width=True)
