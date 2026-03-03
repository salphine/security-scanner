from fpdf import FPDF
from datetime import datetime
import os
from typing import Dict, List

class SecurityReport(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
    
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(self.WIDTH - 20, 10, 'Security Assessment Report', 0, 0, 'L')
        self.ln(20)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()
    
    def risk_color(self, risk):
        colors = {
            'critical': (255, 0, 0),
            'high': (255, 165, 0),
            'medium': (255, 255, 0),
            'low': (0, 255, 0)
        }
        return colors.get(risk.lower(), (0, 0, 0))

class ReportGenerator:
    def __init__(self, output_dir="reports/exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_report(self, scan_data: Dict, scan_id: str) -> str:
        pdf = SecurityReport()
        pdf.add_page()
        
        # Report metadata
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 10, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.cell(0, 10, f"Scan ID: {scan_id}", 0, 1)
        pdf.cell(0, 10, f"Target: {scan_data.get('target', 'N/A')}", 0, 1)
        pdf.cell(0, 10, f"Scan Type: {scan_data.get('scan_type', 'N/A')}", 0, 1)
        pdf.cell(0, 10, f"Scan Date: {scan_data.get('started_at', 'N/A')}", 0, 1)
        pdf.ln(10)
        
        # Executive Summary
        pdf.chapter_title("Executive Summary")
        vuln_count = len(scan_data.get('vulnerabilities', []))
        port_count = len(scan_data.get('open_ports', []))
        
        summary = f"""
        This security assessment identified {vuln_count} potential vulnerabilities 
        and {port_count} open ports on the target system.
        
        Risk Distribution:
        """
        pdf.chapter_body(summary)
        
        # Risk summary table
        risk_counts = {}
        for vuln in scan_data.get('vulnerabilities', []):
            risk = vuln.get('risk_level', 'low').lower()
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        if risk_counts:
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(60, 10, 'Risk Level', 1, 0, 'C')
            pdf.cell(60, 10, 'Count', 1, 1, 'C')
            
            pdf.set_font('Arial', '', 10)
            for risk, count in risk_counts.items():
                pdf.set_text_color(*pdf.risk_color(risk))
                pdf.cell(60, 10, risk.capitalize(), 1, 0, 'C')
                pdf.set_text_color(0, 0, 0)
                pdf.cell(60, 10, str(count), 1, 1, 'C')
        
        pdf.ln(10)
        
        # Vulnerabilities section
        if scan_data.get('vulnerabilities'):
            pdf.add_page()
            pdf.chapter_title("Detailed Vulnerabilities")
            
            for i, vuln in enumerate(scan_data['vulnerabilities'], 1):
                pdf.set_font('Arial', 'B', 11)
                pdf.set_text_color(*pdf.risk_color(vuln.get('risk_level', 'low')))
                pdf.cell(0, 8, f"{i}. {vuln.get('name', 'Unknown')}", 0, 1)
                pdf.set_text_color(0, 0, 0)
                
                pdf.set_font('Arial', '', 10)
                pdf.multi_cell(0, 5, f"Risk: {vuln.get('risk_level', 'Unknown')}")
                pdf.multi_cell(0, 5, f"Description: {vuln.get('description', 'N/A')}")
                pdf.multi_cell(0, 5, f"Remediation: {vuln.get('remediation', 'N/A')}")
                pdf.ln(5)
        
        # Open Ports section
        if scan_data.get('open_ports'):
            pdf.add_page()
            pdf.chapter_title("Open Ports Detected")
            
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(40, 10, 'Port', 1, 0, 'C')
            pdf.cell(60, 10, 'Service', 1, 0, 'C')
            pdf.cell(40, 10, 'Risk', 1, 1, 'C')
            
            pdf.set_font('Arial', '', 10)
            for port in scan_data['open_ports']:
                pdf.set_text_color(*pdf.risk_color(port.get('risk', 'low')))
                pdf.cell(40, 10, str(port.get('port', '')), 1, 0, 'C')
                pdf.set_text_color(0, 0, 0)
                pdf.cell(60, 10, port.get('service', 'unknown'), 1, 0, 'C')
                pdf.set_text_color(*pdf.risk_color(port.get('risk', 'low')))
                pdf.cell(40, 10, port.get('risk', 'low').upper(), 1, 1, 'C')
                pdf.set_text_color(0, 0, 0)
        
        # Recommendations
        pdf.add_page()
        pdf.chapter_title("Recommendations")
        
        recommendations = [
            "1. Implement security headers (HSTS, CSP, X-Frame-Options)",
            "2. Close unnecessary open ports",
            "3. Update outdated software versions",
            "4. Implement input validation to prevent injection attacks",
            "5. Enable comprehensive logging and monitoring",
            "6. Use strong encryption protocols (TLS 1.2+)",
            "7. Regular security assessments and penetration testing"
        ]
        
        for rec in recommendations:
            pdf.cell(5)
            pdf.multi_cell(0, 7, rec)
        
        # Save file
        filename = f"{self.output_dir}/report_{scan_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        
        return filename
