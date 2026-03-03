from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import scans, validation
from datetime import datetime
import random

app = FastAPI(
    title="Security Scanner API",
    description="Professional security scanning tool with certificate & communication validation",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
app.include_router(validation.router, tags=["validation"])

@app.get("/")
async def root():
    return {
        "name": "Security Scanner API",
        "version": "2.0.0",
        "status": "operational",
        "features": [
            "Port Scanning",
            "Vulnerability Detection",
            "SSL/TLS Certificate Validation",
            "Email Security Validation",
            "SMS Sender Verification",
            "Phishing Detection"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/stats")
async def get_stats():
    return {
        "total_scans": 1247,
        "total_threats": 342,
        "certificates_validated": 892,
        "emails_validated": 2341,
        "sms_validated": 567,
        "phishing_detected": 89,
        "critical": 23,
        "high": 45,
        "medium": 89,
        "low": 156
    }
