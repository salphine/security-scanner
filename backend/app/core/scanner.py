from backend.scanner.port_engine import PortScanner
from backend.scanner.header_audit import HeaderAuditor
from backend.scanner.payload_injector import PayloadInjector
from backend.scanner.ssl_tls_checker import SSLTLChecker
import asyncio
import time
from typing import Dict

class SecurityScanner:
    def __init__(self, target: str):
        self.target = target
        self.port_scanner = PortScanner(target)
        self.header_auditor = HeaderAuditor(target)
        self.payload_injector = PayloadInjector(target)
        self.ssl_checker = SSLTLChecker(target)
    
    async def run_scan(self, scan_type: str = "full") -> Dict:
        start_time = time.time()
        results = {
            'target': self.target,
            'scan_type': scan_type,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'vulnerabilities': [],
            'open_ports': [],
            'scan_duration': 0
        }
        
        try:
            if scan_type == "ports":
                results['open_ports'] = await self.port_scanner.scan()
            elif scan_type == "web":
                header_results = await self.header_auditor.scan()
                results['vulnerabilities'].extend(header_results.get('vulnerabilities', []))
            elif scan_type == "ssl":
                ssl_results = await self.ssl_checker.check_ssl_tls()
                results['vulnerabilities'].extend(ssl_results.get('vulnerabilities', []))
            else:  # full scan
                # Run all scans concurrently
                port_task = self.port_scanner.scan()
                header_task = self.header_auditor.scan()
                ssl_task = self.ssl_checker.check_ssl_tls()
                payload_task = self.payload_injector.scan()
                
                port_results, header_results, ssl_results, payload_results = await asyncio.gather(
                    port_task, header_task, ssl_task, payload_task, return_exceptions=True
                )
                
                if not isinstance(port_results, Exception):
                    results['open_ports'] = port_results
                if not isinstance(header_results, Exception):
                    results['vulnerabilities'].extend(header_results.get('vulnerabilities', []))
                if not isinstance(ssl_results, Exception):
                    results['vulnerabilities'].extend(ssl_results.get('vulnerabilities', []))
                if not isinstance(payload_results, Exception):
                    results['vulnerabilities'].extend(payload_results)
            
            results['scan_duration'] = int(time.time() - start_time)
            results['risk_summary'] = self._summarize_risks(results['vulnerabilities'])
            
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def _summarize_risks(self, vulnerabilities: List) -> Dict:
        summary = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for vuln in vulnerabilities:
            risk = vuln.get('risk_level', 'low').lower()
            if risk in summary:
                summary[risk] += 1
        return summary
