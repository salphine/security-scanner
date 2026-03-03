import streamlit as st
import pandas as pd

def render_results_table(results, title="Scan Results"):
    if not results:
        st.info("No results to display")
        return
    
    st.subheader(f"?? {title}")
    
    # Create tabs for different result types
    tab1, tab2, tab3 = st.tabs(["Vulnerabilities", "Open Ports", "Summary"])
    
    with tab1:
        if results.get('vulnerabilities'):
            df_vuln = pd.DataFrame(results['vulnerabilities'])
            
            # Color code by risk level
            def color_risk(val):
                colors = {
                    'critical': 'background-color: #ff4d4d',
                    'high': 'background-color: #ffa64d',
                    'medium': 'background-color: #ffff4d',
                    'low': 'background-color: #4dff4d'
                }
                return colors.get(val, '')
            
            st.dataframe(
                df_vuln.style.applymap(color_risk, subset=['risk_level']),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("No vulnerabilities found!")
    
    with tab2:
        if results.get('open_ports'):
            df_ports = pd.DataFrame(results['open_ports'])
            st.dataframe(df_ports, use_container_width=True, hide_index=True)
        else:
            st.info("No open ports detected")
    
    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Vulnerabilities", len(results.get('vulnerabilities', [])))
        with col2:
            st.metric("Open Ports", len(results.get('open_ports', [])))
        with col3:
            st.metric("Scan Duration", f"{results.get('scan_duration', 0)}s")
        
        if results.get('risk_summary'):
            st.subheader("Risk Summary")
            risk_df = pd.DataFrame([
                {"Risk Level": k.capitalize(), "Count": v} 
                for k, v in results['risk_summary'].items()
            ])
            st.bar_chart(risk_df.set_index('Risk Level'))
