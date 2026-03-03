import streamlit as st

def render_scan_form():
    with st.form("scan_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            target = st.text_input(
                "Target", 
                placeholder="example.com or 192.168.1.1",
                help="Enter IP address or domain name"
            )
            
            scan_type = st.selectbox(
                "Scan Type",
                ["Quick Port Scan", "Web Audit", "SSL/TLS Check", "Full Scan"],
                help="Select the type of security scan to perform"
            )
        
        with col2:
            timeout = st.slider(
                "Timeout (seconds)", 
                min_value=1, 
                max_value=30, 
                value=5,
                help="Maximum time to wait for responses"
            )
            
            threads = st.slider(
                "Threads", 
                min_value=1, 
                max_value=50, 
                value=10,
                help="Number of concurrent threads"
            )
        
        advanced = st.expander("Advanced Options")
        with advanced:
            st.checkbox("Aggressive Mode", help="Enable aggressive scanning (may be detected)")
            st.checkbox("Stealth Mode", help="Slow scan to avoid detection")
            st.number_input("Port Range Start", min_value=1, max_value=65535, value=1)
            st.number_input("Port Range End", min_value=1, max_value=65535, value=1024)
        
        submitted = st.form_submit_button("?? Start Scan", type="primary", use_container_width=True)
        
        return target, scan_type, {'timeout': timeout, 'threads': threads} if submitted else (None, None, None)
