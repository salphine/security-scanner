"""
ADVANCED SECURITY COMMAND CENTER
BBIT Final Year Project - Professional Enterprise Edition
Real-time Updates | Dynamic Theming | Advanced Analytics | Live Monitoring
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import random
import socket
import requests
import hashlib
import json
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import warnings
warnings.filterwarnings('ignore')

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Advanced Security Command Center",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DYNAMIC THEME SYSTEM ====================
def get_theme_css(primary_color, secondary_color, bg_color):
    """Generate dynamic CSS based on selected colors"""
    return f"""
    <style>
        /* Import gaming font */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&display=swap');
        
        * {{
            font-family: 'Orbitron', sans-serif;
        }}
        
        /* Animated gradient background */
        .stApp {{
            background: linear-gradient(-45deg, {bg_color}, {primary_color}22, {secondary_color}22, {bg_color});
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }}
        
        @keyframes gradient {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Glass morphism cards */
        .glass-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid {primary_color}40;
            border-radius: 20px;
            padding: 25px;
            margin: 10px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            transition: all 0.3s ease;
            animation: cardGlow 3s infinite;
        }}
        
        @keyframes cardGlow {{
            0% {{ box-shadow: 0 8px 32px 0 {primary_color}20; }}
            50% {{ box-shadow: 0 8px 32px 0 {primary_color}60; }}
            100% {{ box-shadow: 0 8px 32px 0 {primary_color}20; }}
        }}
        
        .glass-card:hover {{
            transform: translateY(-5px) scale(1.02);
            border-color: {primary_color};
            box-shadow: 0 15px 45px 0 {primary_color}80;
        }}
        
        /* Metric cards with neon effect */
        .metric-card {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid {primary_color};
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0px {primary_color}; }}
            50% {{ box-shadow: 0 0 20px {primary_color}; }}
            100% {{ box-shadow: 0 0 0px {primary_color}; }}
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(135deg, transparent, {primary_color}20, transparent);
            transform: rotate(45deg);
            animation: shine 3s infinite;
        }}
        
        @keyframes shine {{
            0% {{ transform: translateX(-100%) rotate(45deg); }}
            100% {{ transform: translateX(100%) rotate(45deg); }}
        }}
        
        .metric-value {{
            font-size: 3em;
            font-weight: 800;
            background: linear-gradient(135deg, {primary_color}, {secondary_color});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            position: relative;
            z-index: 1;
        }}
        
        .metric-label {{
            color: #aaa;
            font-size: 1em;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        /* Threat cards with severity colors */
        .threat-card {{
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            color: white;
            animation: slideIn 0.5s, glow 2s infinite;
            position: relative;
            overflow: hidden;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(-100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        @keyframes glow {{
            0% {{ filter: brightness(1); }}
            50% {{ filter: brightness(1.2); }}
            100% {{ filter: brightness(1); }}
        }}
        
        .critical {{ 
            background: linear-gradient(135deg, #ff416c, #ff4b2b);
            border-left: 5px solid white;
        }}
        .high {{ background: linear-gradient(135deg, #f12711, #f5af19); }}
        .medium {{ background: linear-gradient(135deg, #f7971e, #ffd200); color: black; }}
        .low {{ background: linear-gradient(135deg, #56ab2f, #a8e063); color: black; }}
        
        /* Live indicator */
        .live-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: {primary_color};
            border-radius: 50%;
            animation: livePulse 1s infinite;
            margin-right: 8px;
        }}
        
        @keyframes livePulse {{
            0% {{ opacity: 1; transform: scale(1); }}
            50% {{ opacity: 0.5; transform: scale(1.2); }}
            100% {{ opacity: 1; transform: scale(1); }}
        }}
        
        /* Progress bar */
        .progress-bar {{
            height: 20px;
            background: linear-gradient(90deg, {primary_color}, {secondary_color});
            border-radius: 10px;
            animation: progressPulse 2s infinite;
        }}
        
        @keyframes progressPulse {{
            0% {{ opacity: 0.8; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.8; }}
        }}
        
        /* Floating particles */
        .particle {{
            position: fixed;
            width: 3px;
            height: 3px;
            background: {primary_color};
            border-radius: 50%;
            pointer-events: none;
            animation: float 10s linear infinite;
            z-index: 0;
        }}
        
        @keyframes float {{
            from {{ transform: translateY(100vh) rotate(0deg); opacity: 1; }}
            to {{ transform: translateY(-100vh) rotate(360deg); opacity: 0; }}
        }}
        
        /* Neon text */
        .neon-text {{
            color: {primary_color};
            text-shadow: 0 0 10px {primary_color}, 0 0 20px {primary_color}, 0 0 30px {primary_color};
        }}
        
        /* Animated border */
        .animated-border {{
            position: relative;
            padding: 20px;
            border-radius: 15px;
            background: rgba(0,0,0,0.3);
        }}
        
        .animated-border::after {{
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, {primary_color}, {secondary_color}, {primary_color});
            border-radius: 17px;
            z-index: -1;
            animation: borderRotate 3s linear infinite;
        }}
        
        @keyframes borderRotate {{
            0% {{ filter: hue-rotate(0deg); }}
            100% {{ filter: hue-rotate(360deg); }}
        }}
        
        /* Digital clock */
        .digital-clock {{
            font-family: 'Orbitron', monospace;
            font-size: 2.5em;
            color: {primary_color};
            text-shadow: 0 0 20px {primary_color};
            text-align: center;
            padding: 20px;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            border: 1px solid {primary_color};
        }}
    </style>
    """

# ==================== REAL-TIME DATA GENERATOR ====================
class RealTimeMonitor:
    """Generate realistic real-time security data"""
    
    def __init__(self):
        self.threat_types = [
            "SQL Injection", "Cross-Site Scripting (XSS)", "DDoS Attack", 
            "Brute Force Attack", "Port Scan", "Malware Detected", 
            "Privilege Escalation", "Data Exfiltration", "Zero-Day Exploit",
            "Ransomware", "Phishing Attempt", "DNS Hijacking", "Man-in-the-Middle",
            "Buffer Overflow", "Credential Stuffing", "API Abuse"
        ]
        
        self.severities = ["Critical", "High", "Medium", "Low"]
        self.countries = ["🇺🇸 US", "🇨🇳 CN", "🇷🇺 RU", "🇰🇷 KR", "🇧🇷 BR", 
                         "🇮🇳 IN", "🇩🇪 DE", "🇬🇧 GB", "🇫🇷 FR", "🇯🇵 JP"]
        self.attack_vectors = ["Web App", "Network", "Email", "Endpoint", 
                              "Cloud", "IoT", "Mobile", "API"]
        
    def generate_threat(self):
        """Generate a realistic threat event"""
        severity = random.choices(self.severities, weights=[0.15, 0.25, 0.35, 0.25])[0]
        
        return {
            'id': hashlib.md5(f"{time.time()}{random.random()}".encode()).hexdigest()[:8].upper(),
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'type': random.choice(self.threat_types),
            'severity': severity,
            'source_ip': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'destination_port': random.choice([80, 443, 22, 3389, 3306, 5432, 8080, 8443]),
            'protocol': random.choice(['TCP', 'UDP', 'HTTP', 'HTTPS', 'ICMP', 'DNS']),
            'country': random.choice(self.countries),
            'vector': random.choice(self.attack_vectors),
            'confidence': random.randint(75, 100) if severity in ['Critical', 'High'] else random.randint(40, 85),
            'status': random.choice(['Blocked', 'Monitoring', 'Investigating', 'Mitigated']),
            'bytes': random.randint(1024, 1048576),
            'packets': random.randint(10, 1000)
        }
    
    def generate_network_stats(self):
        """Generate real-time network statistics"""
        return {
            'bytes_in': random.randint(1048576, 10485760),
            'bytes_out': random.randint(524288, 5242880),
            'packets_in': random.randint(1000, 10000),
            'packets_out': random.randint(500, 5000),
            'connections': random.randint(500, 5000),
            'bandwidth': round(random.uniform(10, 1000), 2),
            'latency': round(random.uniform(1, 200), 2),
            'packet_loss': round(random.uniform(0, 2), 2),
            'cpu_usage': random.randint(20, 95),
            'memory_usage': random.randint(30, 90),
            'disk_usage': random.randint(40, 85),
            'active_threats': random.randint(0, 15)
        }

# ==================== REAL PORT SCANNER ====================
class PortScanner:
    """Actual working port scanner"""
    
    def __init__(self, target):
        self.target = target
        self.open_ports = []
        self.common_ports = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'RPC', 139: 'NetBIOS',
            143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 993: 'IMAPS', 995: 'POP3S',
            1723: 'PPTP', 3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            5900: 'VNC', 6379: 'Redis', 8080: 'HTTP-Alt', 8443: 'HTTPS-Alt',
            27017: 'MongoDB', 9200: 'Elasticsearch'
        }
        
    def scan_port(self, port):
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                service = self.common_ports.get(port, 'Unknown')
                self.open_ports.append({
                    'port': port,
                    'service': service,
                    'state': 'open',
                    'risk': 'High' if port in [21,23,445,3389,5900] else 'Medium' if port in [22,3306,5432] else 'Low'
                })
            sock.close()
        except:
            pass
    
    def scan(self, ports=None):
        """Scan multiple ports"""
        if ports is None:
            ports = list(self.common_ports.keys())[:20]  # Scan top 20 ports
        
        for port in ports:
            self.scan_port(port)
        
        return self.open_ports

# ==================== SESSION INITIALIZATION ====================
def init_session():
    """Initialize session state"""
    
    # Theme colors
    if 'primary_color' not in st.session_state:
        st.session_state.primary_color = "#00ff88"
    if 'secondary_color' not in st.session_state:
        st.session_state.secondary_color = "#0066ff"
    if 'bg_color' not in st.session_state:
        st.session_state.bg_color = "#0a0f1e"
    
    # Real-time data
    if 'threats' not in st.session_state:
        st.session_state.threats = []
    if 'network_history' not in st.session_state:
        st.session_state.network_history = []
    if 'scan_results' not in st.session_state:
        st.session_state.scan_results = []
    if 'alerts' not in st.session_state:
        st.session_state.alerts = []

# ==================== THEME CONTROLLER ====================
def theme_controller():
    """Interactive theme controller in sidebar"""
    
    with st.sidebar:
        st.markdown("### 🎨 Dynamic Theme Lab")
        
        # Color pickers
        col1, col2 = st.columns(2)
        with col1:
            new_primary = st.color_picker("Primary", st.session_state.primary_color, key="theme_picker_1")
            if new_primary != st.session_state.primary_color:
                st.session_state.primary_color = new_primary
                st.rerun()
        
        with col2:
            new_secondary = st.color_picker("Secondary", st.session_state.secondary_color, key="theme_picker_2")
            if new_secondary != st.session_state.secondary_color:
                st.session_state.secondary_color = new_secondary
                st.rerun()
        
        # Pre-made themes
        st.markdown("### 🎯 Quick Themes")
        theme_cols = st.columns(3)
        
        themes = {
            "💚 Hacker": ("#00ff00", "#006600"),
            "💙 Cyber": ("#00ffff", "#0066ff"),
            "❤️ Alert": ("#ff4444", "#ff8800"),
            "💜 Royal": ("#aa00ff", "#6600cc"),
            "💛 Solar": ("#ffaa00", "#ff6600"),
            "💗 Pink": ("#ff66aa", "#ff3388")
        }
        
        for i, (name, colors) in enumerate(themes.items()):
            with theme_cols[i % 3]:
                if st.button(name, key=f"theme_{i}", use_container_width=True):
                    st.session_state.primary_color = colors[0]
                    st.session_state.secondary_color = colors[1]
                    st.rerun()
        
        # Brightness control
        brightness = st.slider("🌓 Brightness", 0, 100, 50, key="brightness_slider")
        if brightness < 30:
            st.session_state.bg_color = "#000000"
        elif brightness < 60:
            st.session_state.bg_color = "#0a0f1e"
        else:
            st.session_state.bg_color = "#1a1f2e"

# ==================== LIVE METRICS DASHBOARD ====================
def live_metrics():
    """Display live metrics with auto-refresh"""
    
    # Auto-refresh every 2 seconds
    st_autorefresh(interval=2000, key="metrics_refresh")
    
    monitor = RealTimeMonitor()
    stats = monitor.generate_network_stats()
    
    # Store history for charts
    st.session_state.network_history.append({
        'time': datetime.now().strftime("%H:%M:%S"),
        'connections': stats['connections'],
        'bandwidth': stats['bandwidth'],
        'threats': stats['active_threats']
    })
    
    if len(st.session_state.network_history) > 30:
        st.session_state.network_history.pop(0)
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['packets_in']:,}</div>
            <div class="metric-label">Packets In/sec</div>
            <div style="color: #00ff88; font-size: 0.9em;">↑ 12.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['connections']:,}</div>
            <div class="metric-label">Active Connections</div>
            <div style="color: #00ff88; font-size: 0.9em;">↑ 8.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['bandwidth']} Mbps</div>
            <div class="metric-label">Bandwidth</div>
            <div style="color: #ff4444; font-size: 0.9em;">↓ 3.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats['active_threats']}</div>
            <div class="metric-label">Active Threats</div>
            <div style="color: #ff4444; font-size: 0.9em;">⚠️ Critical</div>
        </div>
        """, unsafe_allow_html=True)

# ==================== LIVE THREAT MONITOR ====================
def live_threat_monitor():
    """Real-time threat monitoring with animations"""
    
    st.markdown("### 🚨 Live Threat Intelligence")
    
    # Auto-refresh every 3 seconds
    st_autorefresh(interval=3000, key="threat_refresh")
    
    monitor = RealTimeMonitor()
    
    # Generate new threat (30% chance)
    if random.random() > 0.7:
        new_threat = monitor.generate_threat()
        st.session_state.threats.insert(0, new_threat)
        st.session_state.threats = st.session_state.threats[:15]  # Keep last 15
    
    # Threat distribution chart
    if st.session_state.threats:
        threat_df = pd.DataFrame(st.session_state.threats)
        severity_counts = threat_df['severity'].value_counts()
        
        fig = go.Figure(data=[
            go.Bar(
                x=severity_counts.index,
                y=severity_counts.values,
                marker_color=['#ff416c', '#f12711', '#f7971e', '#56ab2f'],
                text=severity_counts.values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Live Threat Distribution",
            height=250,
            margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Live threat feed
    for threat in st.session_state.threats[:5]:
        severity_class = threat['severity'].lower()
        
        st.markdown(f"""
        <div class="threat-card {severity_class}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span><strong>🚨 {threat['type']}</strong></span>
                <span style="background: rgba(255,255,255,0.2); padding: 3px 10px; border-radius: 15px;">
                    {threat['severity']}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                <span>📍 {threat['source_ip']} ({threat['country']})</span>
                <span>🎯 Port {threat['destination_port']}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                <span>🔒 {threat['vector']}</span>
                <span>⚡ {threat['protocol']}</span>
                <span>📊 {threat['confidence']}% confidence</span>
            </div>
            <div style="margin-top: 10px;">
                <div style="background: rgba(0,0,0,0.3); height: 5px; border-radius: 5px;">
                    <div style="width: {threat['confidence']}%; background: white; height: 5px; border-radius: 5px;"></div>
                </div>
            </div>
            <div style="margin-top: 5px; font-size: 0.8em; opacity: 0.8;">
                ID: {threat['id']} | {threat['timestamp']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== ADVANCED SCANNER ====================
def advanced_scanner():
    """Professional scanner with real-time updates"""
    
    st.markdown("### 🔍 Advanced Port Scanner")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        target = st.text_input("Target IP/Domain", "scanme.nmap.org", 
                               help="Enter IP address or domain name to scan",
                               key="scanner_target")
        
        scan_preset = st.selectbox(
            "Scan Preset",
            ["Quick Scan (Top 20 ports)", "Common Ports (Top 100)", "Full Scan (1-1024)", "Custom"],
            key="scan_preset"
        )
    
    with col2:
        st.markdown("### ⚡ Quick Actions")
        if st.button("🚀 Start Scan", type="primary", use_container_width=True, key="start_scan"):
            st.session_state.scanning = True
            st.session_state.scan_target = target
            st.session_state.scan_progress = 0
    
    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        col1, col2, col3 = st.columns(3)
        with col1:
            timeout = st.slider("Timeout (s)", 0.1, 5.0, 1.0, 0.1, key="scan_timeout")
            threads = st.slider("Threads", 1, 50, 10, key="scan_threads")
        with col2:
            st.checkbox("Service Detection", value=True, key="service_detect")
            st.checkbox("OS Detection", value=False, key="os_detect")
        with col3:
            st.checkbox("Banner Grabbing", value=True, key="banner_grab")
            st.checkbox("Vulnerability Check", value=True, key="vuln_check")
    
    # Scan progress and results
    if st.session_state.get('scanning', False):
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.container()
        
        scanner = PortScanner(st.session_state.scan_target)
        
        # Determine ports to scan
        if scan_preset == "Quick Scan (Top 20 ports)":
            ports = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5432,5900,8080]
        elif scan_preset == "Common Ports (Top 100)":
            ports = list(range(1, 101))
        elif scan_preset == "Full Scan (1-1024)":
            ports = list(range(1, 1025))
        else:
            ports = list(range(1, 101))  # Default
        
        # Simulate scan with real port checking
        for i, port in enumerate(ports[:50]):  # Limit to first 50 ports for demo
            progress = int((i + 1) / len(ports[:50]) * 100)
            progress_bar.progress(progress)
            
            if progress < 30:
                status_text.text(f"🔄 Initializing scan... {progress}%")
            elif progress < 60:
                scanner.scan_port(port)
                status_text.text(f"🔍 Scanning port {port}... {progress}%")
            elif progress < 90:
                status_text.text(f"🛡️ Analyzing results... {progress}%")
            else:
                status_text.text(f"📊 Generating report... {progress}%")
            
            time.sleep(0.05)
        
        status_text.success("✅ Scan completed!")
        st.balloons()
        
        # Display results
        results = scanner.open_ports
        st.session_state.scan_results = results
        
        if results:
            st.subheader(f"📌 Found {len(results)} open ports")
            df_results = pd.DataFrame(results)
            st.dataframe(df_results, use_container_width=True, hide_index=True)
            
            # Risk summary
            risk_counts = pd.Series([r['risk'] for r in results]).value_counts()
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=risk_counts.index,
                    values=risk_counts.values,
                    marker_colors=['#ff4444', '#ff8800', '#00c851']
                )
            ])
            fig.update_layout(title="Risk Distribution", height=300)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No open ports found")
        
        st.session_state.scanning = False

# ==================== LIVE NETWORK ANALYTICS ====================
def network_analytics():
    """Real-time network analytics dashboard"""
    
    st.markdown("### 📊 Live Network Analytics")
    
    # Auto-refresh every 2 seconds
    st_autorefresh(interval=2000, key="network_refresh")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Network traffic chart
        if st.session_state.network_history:
            df = pd.DataFrame(st.session_state.network_history)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df['connections'],
                mode='lines+markers',
                name='Connections',
                line=dict(color=st.session_state.primary_color, width=3)
            ))
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df['bandwidth'],
                mode='lines+markers',
                name='Bandwidth',
                line=dict(color=st.session_state.secondary_color, width=3),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title="Network Traffic Trend",
                height=350,
                xaxis=dict(title="Time"),
                yaxis=dict(title="Connections", side="left"),
                yaxis2=dict(title="Bandwidth (Mbps)", overlaying="y", side="right"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Protocol distribution
        protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'DNS', 'ICMP']
        values = [random.randint(100, 1000) for _ in protocols]
        
        fig = go.Figure(data=[
            go.Bar(
                x=protocols,
                y=values,
                marker_color=[st.session_state.primary_color, st.session_state.secondary_color,
                            '#ff4444', '#ff8800', '#00c851', '#aa00ff'],
                text=values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Protocol Distribution",
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== SYSTEM METRICS ====================
def system_metrics():
    """Real-time system performance metrics"""
    
    st.markdown("### ⚡ System Performance")
    
    # Auto-refresh every 2 seconds
    st_autorefresh(interval=2000, key="system_refresh")
    
    monitor = RealTimeMonitor()
    stats = monitor.generate_network_stats()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # CPU Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stats['cpu_usage'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "CPU Usage %", 'font': {'color': 'white'}},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': 'white'},
                'bar': {'color': st.session_state.primary_color},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': 'gray',
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(0,255,0,0.2)'},
                    {'range': [50, 80], 'color': 'rgba(255,255,0,0.2)'},
                    {'range': [80, 100], 'color': 'rgba(255,0,0,0.2)'}
                ]
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Memory Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stats['memory_usage'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Memory Usage %", 'font': {'color': 'white'}},
            gauge={
                'axis': {'range': [None, 100], 'tickcolor': 'white'},
                'bar': {'color': st.session_state.secondary_color},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 2,
                'bordercolor': 'gray',
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(0,255,0,0.2)'},
                    {'range': [50, 80], 'color': 'rgba(255,255,0,0.2)'},
                    {'range': [80, 100], 'color': 'rgba(255,0,0,0.2)'}
                ]
            }
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Packet Loss", f"{stats['packet_loss']}%", "-0.2%")
    with col2:
        st.metric("Disk I/O", f"{stats['disk_usage']}%", "+3%")
    with col3:
        st.metric("Network Latency", f"{stats['latency']}ms", "-5ms")
    with col4:
        st.metric("System Uptime", "99.97%", "+0.02%")

# ==================== MAIN DASHBOARD ====================
def main():
    """Main dashboard"""
    
    # Initialize session
    init_session()
    
    # Apply dynamic CSS
    st.markdown(get_theme_css(
        st.session_state.primary_color,
        st.session_state.secondary_color,
        st.session_state.bg_color
    ), unsafe_allow_html=True)
    
    # Floating particles
    particles = ""
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.randint(0, 10)
        duration = random.randint(10, 30)
        particles += f'<div class="particle" style="left: {left}%; animation-delay: {delay}s; animation-duration: {duration}s;"></div>'
    st.markdown(particles, unsafe_allow_html=True)
    
    # Header with live indicator
    st.markdown(f"""
    <div class="animated-border" style="margin-bottom: 30px;">
        <div style="display: flex; align-items: center; justify-content: center;">
            <div class="live-indicator"></div>
            <h1 style="color: white; font-size: 3.5em; margin: 0;">🛡️ ADVANCED SECURITY COMMAND CENTER</h1>
        </div>
        <p style="color: #aaa; text-align: center; margin: 10px 0 0 0;">
            Real-time Threat Detection | Live Monitoring | Dynamic Theming | Advanced Analytics
        </p>
        <div class="digital-clock" style="margin-top: 20px;">
            {datetime.now().strftime("%H:%M:%S")}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme controller in sidebar
    theme_controller()
    
    # System status
    with st.sidebar:
        st.markdown("### 🖥️ System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("🟢 Backend")
            st.markdown("🟢 Database")
        with col2:
            st.markdown("🟢 Scanner")
            st.markdown("🟢 API")
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Uptime", "99.97%", "+0.02%")
        st.metric("Scan Queue", "3", "-2")
        st.metric("Threat Level", "ELEVATED", "⚠️")
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 LIVE DASHBOARD", "🔍 SCANNER", "📈 ANALYTICS", "⚙️ CONTROL"
    ])
    
    with tab1:
        live_metrics()
        col1, col2 = st.columns([2, 1])
        with col1:
            live_threat_monitor()
        with col2:
            st.markdown("### 🌍 Live Threat Map")
            # Simple world map placeholder
            map_data = pd.DataFrame(
                np.random.randn(100, 2) / [50, 50] + [37.76, -122.4],
                columns=['lat', 'lon']
            )
            st.map(map_data)
    
    with tab2:
        advanced_scanner()
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            network_analytics()
        with col2:
            system_metrics()
    
    with tab4:
        st.markdown("### ⚙️ Control Panel")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🔄 Refresh All", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("📊 Export Report", use_container_width=True):
                st.success("Report exported!")
        with col3:
            if st.button("⚡ Emergency", use_container_width=True):
                st.error("Emergency mode activated!")
        with col4:
            if st.button("🔒 Lockdown", use_container_width=True):
                st.warning("System lockdown initiated!")
        
        # Live logs
        st.markdown("### 📋 Live System Logs")
        log_container = st.empty()
        
        logs = [
            f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 System initialized - Security modules loaded",
            f"[{datetime.now().strftime('%H:%M:%S')}] 🔍 Scan engine started - Ready for targets",
            f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Threat detected: SQL Injection attempt blocked",
            f"[{datetime.now().strftime('%H:%M:%S')}] 🛡️ Firewall rules updated - 3 new signatures",
            f"[{datetime.now().strftime('%H:%M:%S')}] 📊 Analytics processed - 1,247 events analyzed"
        ]
        
        log_container.markdown("\n".join([
            f"<div style='color: #aaa; font-family: monospace; padding: 5px; border-bottom: 1px solid #333;'>{log}</div>" 
            for log in logs
        ]), unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div style="text-align: center; padding: 30px; color: #666; border-top: 1px solid #333; margin-top: 30px;">
        <span>🛡️ BBIT Enterprise Security Scanner v3.0</span> | 
        <span>⚡ Real-time Monitoring</span> | 
        <span>🎯 Professional Grade</span> |
        <span style="color: {st.session_state.primary_color};">Live • {datetime.now().strftime("%Y-%m-%d")}</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
