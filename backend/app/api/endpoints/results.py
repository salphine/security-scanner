from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import database, models
from typing import List, Dict

router = APIRouter()

@router.get("/{scan_id}/vulnerabilities")
async def get_vulnerabilities(scan_id: str, db: Session = Depends(database.get_db)):
    vulns = db.query(models.Vulnerability).filter(
        models.Vulnerability.scan_id == scan_id
    ).all()
    return vulns

@router.get("/{scan_id}/ports")
async def get_open_ports(scan_id: str, db: Session = Depends(database.get_db)):
    ports = db.query(models.OpenPort).filter(
        models.OpenPort.scan_id == scan_id
    ).all()
    return ports

@router.get("/{scan_id}/summary")
async def get_scan_summary(scan_id: str, db: Session = Depends(database.get_db)):
    scan = db.query(models.Scan).filter(models.Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    vuln_count = db.query(models.Vulnerability).filter(
        models.Vulnerability.scan_id == scan_id
    ).count()
    
    port_count = db.query(models.OpenPort).filter(
        models.OpenPort.scan_id == scan_id
    ).count()
    
    return {
        'scan_id': scan.id,
        'target': scan.target,
        'status': scan.status,
        'vulnerabilities_found': vuln_count,
        'open_ports_found': port_count,
        'duration': scan.duration
    }
