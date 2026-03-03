import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import random
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Page config
st.set_page_config(
    page_title="Security Command Center",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #00ff8840;
    }
    .threat-card {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        color: white;
    }
    .critical { background: #ff4444; }
    .high { background: #ff8800; }
    .medium { background: #ffaa00; }
    .low { background: #00c851; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='color: white; font-size: 3em;'>🛡️ SECURITY COMMAND CENTER</h1>
    <p style='color: #888;'>Real-time Threat Monitoring</p>
</div>
""", unsafe_allow_html=True)

# Auto refresh
st_autorefresh(interval=3000, key="main_refresh")

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='metric-card'>
        <h3 style='color: #00ff88;'>1,247</h3>
        <p style='color: #888;'>Total Scans</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='metric-card'>
        <h3 style='color: #ff4444;'>342</h3>
        <p style='color: #888;'>Threats</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='metric-card'>
        <h3 style='color: #00c851;'>89%</h3>
        <p style='color: #888;'>Security</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='metric-card'>
        <h3 style='color: #ffaa00;'>45s</h3>
        <p style='color: #888;'>Response</p>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🚨 Threats", "🔍 Scanner", "📊 Analytics"])

with tab1:
    st.subheader("Live Threats")
    
    # Generate random threats
    threats = [
        {"type": "SQL Injection", "severity": "critical", "source": "192.168.1.105", "time": "Now"},
        {"type": "XSS Attack", "severity": "high", "source": "10.0.0.23", "time": "2s ago"},
        {"type": "Port Scan", "severity": "medium", "source": "172.16.0.50", "time": "5s ago"},
        {"type": "Brute Force", "severity": "high", "source": "45.33.22.11", "time": "10s ago"},
    ]
    
    for threat in threats:
        st.markdown(f"""
        <div class='threat-card {threat["severity"]}'>
            <strong>🚨 {threat["type"]}</strong><br>
            Source: {threat["source"]} | {threat["time"]}
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("Scanner")
    
    target = st.text_input("Target", "example.com")
    scan_type = st.selectbox("Scan Type", ["Quick Scan", "Deep Scan", "Full Audit"])
    
    if st.button("Start Scan"):
        progress = st.progress(0)
        status = st.empty()
        
        for i in range(101):
            progress.progress(i)
            status.text(f"Scanning... {i}%")
            time.sleep(0.05)
        
        st.success("Scan complete!")
        st.balloons()
        
        # Show results
        st.metric("Open Ports", random.randint(5, 25))
        st.metric("Vulnerabilities", random.randint(0, 15))
        st.metric("Risk Score", f"{random.randint(20, 85)}%")

with tab3:
    st.subheader("Analytics")
    
    # Simple chart
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Critical', 'High', 'Medium']
    )
    st.line_chart(chart_data)
    
    # Pie chart
    fig = go.Figure(data=[go.Pie(
        labels=['Critical', 'High', 'Medium', 'Low'],
        values=[23, 45, 89, 156],
        marker_colors=['#ff4444', '#ff8800', '#ffaa00', '#00c851']
    )])
    fig.update_layout(title='Risk Distribution')
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    BBIT Security Scanner v1.0 | Real-time Monitoring
</div>
""", unsafe_allow_html=True)
