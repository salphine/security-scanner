import requests
from typing import Dict
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HeaderAuditor:
    def __init__(self, target: str):
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        self.target = target
        
        self.security_headers = {
            'Strict-Transport-Security': 'Enforces HTTPS connections',
            'Content-Security-Policy': 'Prevents XSS and data injection',
            'X-Frame-Options': 'Prevents clickjacking',
            'X-Content-Type-Options': 'Prevents MIME sniffing',
            'Referrer-Policy': 'Controls referrer information'
        }
    
    async def scan(self) -> Dict:
        try:
            response = requests.get(self.target, timeout=5, verify=False)
            headers = response.headers
            
            findings = {
                'url': self.target,
                'status_code': response.status_code,
                'missing_headers': [],
                'vulnerabilities': []
            }
            
            for header, description in self.security_headers.items():
                if header not in headers:
                    findings['missing_headers'].append(header)
                    findings['vulnerabilities'].append({
                        'name': f'Missing {header}',
                        'description': description,
                        'risk_level': 'medium',
                        'remediation': f'Add the {header} header to your responses'
                    })
            
            # Check for server info disclosure
            if 'Server' in headers:
                findings['vulnerabilities'].append({
                    'name': 'Server Information Disclosure',
                    'description': f'Server header reveals: {headers["Server"]}',
                    'risk_level': 'low',
                    'remediation': 'Remove or obscure server version information'
                })
            
            return findings
            
        except Exception as e:
            return {'url': self.target, 'error': str(e), 'vulnerabilities': []}
