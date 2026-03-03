import requests
from urllib.parse import urlparse, parse_qs, urlencode
from typing import List, Dict

class PayloadInjector:
    def __init__(self, target: str):
        self.target = target
        self.sql_payloads = ["'", "' OR '1'='1", "' OR 1=1--"]
        self.xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
    
    def extract_parameters(self, url: str) -> Dict:
        parsed = urlparse(url)
        return {k: v[0] for k, v in parse_qs(parsed.query).items()}
    
    async def scan(self) -> List[Dict]:
        vulnerabilities = []
        params = self.extract_parameters(self.target)
        
        if not params:
            return []
        
        for param, value in params.items():
            # Simple SQLi test
            for payload in self.sql_payloads:
                try:
                    test_params = {param: value + payload}
                    test_url = self.target.split('?')[0] + '?' + urlencode(test_params)
                    response = requests.get(test_url, timeout=3)
                    
                    if any(x in response.text.lower() for x in ['sql', 'syntax', 'mysql']):
                        vulnerabilities.append({
                            'type': 'SQL Injection',
                            'parameter': param,
                            'risk_level': 'high'
                        })
                        break
                except:
                    continue
        
        return vulnerabilities
