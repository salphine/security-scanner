import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Security Scanner",
    page_icon="???",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #f5f7f9; }
    .risk-high { color: #ff4b4b; font-weight: bold; }
    .risk-medium { color: #ffa500; font-weight: bold; }
    .risk-low { color: #00cc66; font-weight: bold; }
    .metric-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"
if 'current_scan' not in st.session_state:
    st.session_state.current_scan = None

# Sidebar
with st.sidebar:
    st.title("??? Security Scanner")
    st.markdown("---")
    
    # API Connection
    try:
        response = requests.get(f"{st.session_state.api_url}/")
        if response.status_code == 200:
            st.success("? Backend Connected")
        else:
            st.error("? Backend Error")
    except:
        st.error("? Backend Offline")
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["?? New Scan", "?? History", "?? Analytics", "?? Reports"]
    )
    
    st.markdown("---")
    st.info("? BBIT Security Tool v1.0")

# Main content
if page == "?? New Scan":
    st.title("?? New Security Scan")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("scan_form"):
            target = st.text_input("Target (IP or Domain)", placeholder="example.com or 192.168.1.1")
            scan_type = st.selectbox(
                "Scan Type",
                ["Quick Port Scan", "Web Audit", "Full Scan"]
            )
            
            submitted = st.form_submit_button("?? Start Scan", type="primary", use_container_width=True)
            
            if submitted and target:
                try:
                    response = requests.post(
                        f"{st.session_state.api_url}/api/scans/start",
                        params={"target": target, "scan_type": scan_type.lower().replace(" ", "_")}
                    )
                    if response.status_code == 200:
                        st.session_state.current_scan = response.json()['scan_id']
                        st.success(f"Scan started! ID: {st.session_state.current_scan}")
                        st.balloons()
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.info("""
        ### Quick Tips
        - Use IP addresses or domains
        - Port scans are fastest
        - Web audit checks headers
        - Full scan is comprehensive
        """)
    
    # Show progress
    if st.session_state.current_scan:
        st.markdown("---")
        st.subheader("?? Scan Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(101):
            time.sleep(0.03)
            progress_bar.progress(i)
            status_text.text(f"Scanning... {i}%")
        
        st.success("? Scan completed!")

elif page == "?? History":
    st.title("?? Scan History")
    
    try:
        response = requests.get(f"{st.session_state.api_url}/api/scans/")
        scans = response.json()
        
        if scans:
            df = pd.DataFrame(scans)
            st.dataframe(df[['id', 'target', 'scan_type', 'status', 'started_at']], 
                        use_container_width=True, hide_index=True)
        else:
            st.info("No scans found. Start your first scan!")
    except:
        st.error("Could not fetch scan history")

elif page == "?? Analytics":
    st.title("?? Security Analytics")
    
    # Sample data
    risk_data = pd.DataFrame({
        'Risk Level': ['Critical', 'High', 'Medium', 'Low'],
        'Count': [2, 5, 12, 8]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(risk_data, values='Count', names='Risk Level', 
                     title='Risk Distribution',
                     color='Risk Level',
                     color_discrete_map={
                         'Critical': '#ff0000',
                         'High': '#ffa500',
                         'Medium': '#ffff00',
                         'Low': '#00ff00'
                     })
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig2 = px.bar(risk_data, x='Risk Level', y='Count',
                      title='Vulnerabilities by Risk',
                      color='Risk Level')
        st.plotly_chart(fig2, use_container_width=True)

elif page == "?? Reports":
    st.title("?? Generate Report")
    st.info("Run a scan first to generate reports")
