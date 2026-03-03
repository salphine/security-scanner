import asyncio
import uuid
from typing import Dict
from datetime import datetime
from backend.app.database import crud
from backend.app.database.database import SessionLocal
from backend.app.core.scanner import SecurityScanner

class ScanTaskQueue:
    def __init__(self):
        self.tasks: Dict[str, dict] = {}
    
    async def start_scan(self, target: str, scan_type: str) -> str:
        scan_id = str(uuid.uuid4())
        
        # Create scan record in database
        db = SessionLocal()
        scan = crud.create_scan(db, scan_id, target, scan_type)
        db.close()
        
        # Start background task
        asyncio.create_task(self._run_scan(scan_id, target, scan_type))
        
        return scan_id
    
    async def _run_scan(self, scan_id: str, target: str, scan_type: str):
        db = SessionLocal()
        try:
            # Update status to in_progress
            crud.update_scan_status(db, scan_id, "in_progress")
            
            # Initialize scanner
            scanner = SecurityScanner(target)
            
            # Run scan
            results = await scanner.run_scan(scan_type)
            
            # Save results to database
            for vuln in results.get('vulnerabilities', []):
                crud.create_vulnerability(db, scan_id, vuln)
            
            for port in results.get('open_ports', []):
                crud.create_open_port(db, scan_id, port)
            
            # Update scan as completed
            crud.complete_scan(db, scan_id, results.get('scan_duration', 0))
            
        except Exception as e:
            crud.update_scan_status(db, scan_id, "failed", str(e))
        finally:
            db.close()

# Global task queue instance
task_queue = ScanTaskQueue()
