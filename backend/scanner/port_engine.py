import socket
import asyncio
from typing import List, Dict

class PortScanner:
    def __init__(self, target: str):
        self.target = target
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 
                             443, 445, 993, 995, 1723, 3306, 3389, 5432, 8080]
        self.services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 1723: "PPTP",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt"
        }
    
    async def scan_port(self, port: int) -> Dict:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))
            
            if result == 0:
                service = self.services.get(port, "unknown")
                risk = "high" if port in [21, 23, 445, 3389] else "medium" if port in [22, 25, 3306] else "low"
                
                return {
                    "port": port,
                    "state": "open",
                    "service": service,
                    "risk": risk
                }
            sock.close()
        except:
            pass
        return None
    
    async def scan(self) -> List[Dict]:
        tasks = [self.scan_port(port) for port in self.common_ports]
        results = await asyncio.gather(*tasks)
        return [r for r in results if r]
