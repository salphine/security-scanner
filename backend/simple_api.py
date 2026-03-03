from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "online", "message": "Security Scanner API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/validate/certificate/{target}")
async def validate_cert(target: str):
    return {
        "target": target,
        "grade": "A",
        "risk_level": "low",
        "expires": "2025-12-31",
        "days_remaining": 365
    }

@app.post("/api/validate/email/validate")
async def validate_email(email: str):
    return {
        "email": email,
        "valid": True,
        "risk_level": "low",
        "issues": []
    }

@app.post("/api/validate/sms/validate")
async def validate_sms(sender: str, message: str = ""):
    return {
        "sender": sender,
        "valid": True,
        "risk_level": "low",
        "issues": []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
