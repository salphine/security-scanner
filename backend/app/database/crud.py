from sqlalchemy.orm import Session
from backend.app.database import models
from datetime import datetime
from typing import Dict, List, Optional

def create_scan(db: Session, scan_id: str, target: str, scan_type: str) -> models.Scan:
    db_scan = models.Scan(
        id=scan_id,
        target=target,
        scan_type=scan_type,
        status="pending",
        started_at=datetime.utcnow()
    )
    db.add(db_scan)
    db.commit()
    db.refresh(db_scan)
    return db_scan

def get_scan(db: Session, scan_id: str) -> Optional[models.Scan]:
    return db.query(models.Scan).filter(models.Scan.id == scan_id).first()

def get_all_scans(db: Session, skip: int = 0, limit: int = 100) -> List[models.Scan]:
    return db.query(models.Scan).order_by(models.Scan.started_at.desc()).offset(skip).limit(limit).all()

def update_scan_status(db: Session, scan_id: str, status: str, error: str = None) -> models.Scan:
    scan = get_scan(db, scan_id)
    if scan:
        scan.status = status
        if error:
            scan.error_message = error
        db.commit()
        db.refresh(scan)
    return scan

def complete_scan(db: Session, scan_id: str, duration: int) -> models.Scan:
    scan = get_scan(db, scan_id)
    if scan:
        scan.status = "completed"
        scan.completed_at = datetime.utcnow()
        scan.duration = duration
        db.commit()
        db.refresh(scan)
    return scan

def create_vulnerability(db: Session, scan_id: str, vuln_data: Dict) -> models.Vulnerability:
    vuln = models.Vulnerability(
        scan_id=scan_id,
        name=vuln_data.get('name', 'Unknown'),
        description=vuln_data.get('description', ''),
        risk_level=vuln_data.get('risk_level', 'low'),
        affected_component=vuln_data.get('affected_component', ''),
        remediation=vuln_data.get('remediation', ''),
        cvss_score=vuln_data.get('cvss_score', 0)
    )
    db.add(vuln)
    db.commit()
    db.refresh(vuln)
    return vuln

def create_open_port(db: Session, scan_id: str, port_data: Dict) -> models.OpenPort:
    port = models.OpenPort(
        scan_id=scan_id,
        port=port_data.get('port', 0),
        service=port_data.get('service', 'unknown'),
        version=port_data.get('version', ''),
        state=port_data.get('state', 'open'),
        risk=port_data.get('risk', 'low')
    )
    db.add(port)
    db.commit()
    db.refresh(port)
    return port

def get_scan_statistics(db: Session) -> Dict:
    total_scans = db.query(models.Scan).count()
    completed_scans = db.query(models.Scan).filter(models.Scan.status == "completed").count()
    total_vulns = db.query(models.Vulnerability).count()
    
    risk_counts = {
        'critical': db.query(models.Vulnerability).filter(models.Vulnerability.risk_level == 'critical').count(),
        'high': db.query(models.Vulnerability).filter(models.Vulnerability.risk_level == 'high').count(),
        'medium': db.query(models.Vulnerability).filter(models.Vulnerability.risk_level == 'medium').count(),
        'low': db.query(models.Vulnerability).filter(models.Vulnerability.risk_level == 'low').count()
    }
    
    return {
        'total_scans': total_scans,
        'completed_scans': completed_scans,
        'total_vulnerabilities': total_vulns,
        'risk_distribution': risk_counts
    }
