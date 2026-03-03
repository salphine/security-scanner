from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.app.database import database, crud
from reports.report_generator import ReportGenerator
import os

router = APIRouter()
report_gen = ReportGenerator()

@router.get("/generate/{scan_id}")
async def generate_report(scan_id: str, db: Session = Depends(database.get_db)):
    scan = crud.get_scan(db, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # Get vulnerabilities and ports
    vulns = db.query(database.models.Vulnerability).filter(
        database.models.Vulnerability.scan_id == scan_id
    ).all()
    
    ports = db.query(database.models.OpenPort).filter(
        database.models.OpenPort.scan_id == scan_id
    ).all()
    
    scan_data = {
        'target': scan.target,
        'scan_type': scan.scan_type,
        'started_at': scan.started_at,
        'duration': scan.duration,
        'vulnerabilities': [{'name': v.name, 'risk_level': v.risk_level, 
                            'description': v.description, 'remediation': v.remediation} 
                           for v in vulns],
        'open_ports': [{'port': p.port, 'service': p.service, 'risk': p.risk} 
                      for p in ports]
    }
    
    report_path = report_gen.generate_report(scan_data, scan_id)
    
    if os.path.exists(report_path):
        return FileResponse(report_path, media_type='application/pdf', 
                          filename=f"security_report_{scan_id}.pdf")
    
    raise HTTPException(status_code=500, detail="Report generation failed")

@router.get("/stats")
async def get_statistics(db: Session = Depends(database.get_db)):
    return crud.get_scan_statistics(db)
