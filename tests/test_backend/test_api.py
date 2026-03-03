import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "operational"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "healthy" in response.json()["status"]

def test_start_scan():
    response = client.post("/api/scans/start", params={"target": "example.com", "scan_type": "quick"})
    assert response.status_code == 200
    assert "scan_id" in response.json()
