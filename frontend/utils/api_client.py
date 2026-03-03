import requests
from typing import Dict, List, Optional

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def start_scan(self, target: str, scan_type: str) -> Optional[int]:
        try:
            response = requests.post(
                f"{self.base_url}/api/scans/start",
                params={"target": target, "scan_type": scan_type}
            )
            if response.status_code == 200:
                return response.json()['scan_id']
        except:
            pass
        return None
    
    def get_scan(self, scan_id: int) -> Optional[Dict]:
        try:
            response = requests.get(f"{self.base_url}/api/scans/{scan_id}")
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def get_all_scans(self) -> List[Dict]:
        try:
            response = requests.get(f"{self.base_url}/api/scans/")
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
