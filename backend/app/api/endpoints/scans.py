from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
import random

router = APIRouter()

@router.get("/")
async def get_all_scans():
    """Get all scans"""
    return [
        {
            "id": "SCAN-001",
            "target": "example.com",
            "scan_type": "Quick Scan",
            "status": "completed",
            "started_at": "2024-03-03 10:30:00",
            "duration": 45
        },
        {
            "id": "SCAN-002",
            "target": "192.168.1.1",
            "scan_type": "Full Scan",
            "status": "running",
            "started_at": "2024-03-03 10:45:00",
            "duration": 120
        }
    ]

@router.post("/start")
async def start_scan(target: str, scan_type: str):
    """Start a new scan"""
    return {
        "scan_id": f"SCAN-{random.randint(100, 999)}",
        "status": "started",
        "target": target,
        "scan_type": scan_type,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/{scan_id}")
async def get_scan(scan_id: str):
    """Get scan by ID"""
    return {
        "id": scan_id,
        "target": "example.com",
        "scan_type": "Full Scan",
        "status": "completed",
        "started_at": "2024-03-03 10:30:00",
        "completed_at": "2024-03-03 10:32:30",
        "duration": 150,
        "open_ports": [80, 443, 22, 3306],
        "vulnerabilities": [
            {
                "name": "Missing Security Headers",
                "severity": "medium",
                "port": 80
            }
        ]
    }
