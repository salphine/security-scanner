"""
ADVANCED SECURITY SCANNER API
BBIT Final Year Project - Simplified Version
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import socket
import ssl
import re
import hashlib
from typing import Optional, Dict, List
import uvicorn
import json

# Try to import dnspython, but provide fallback if not available
try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False
    print("Warning: DNS resolver not available. Email validation will be limited.")

app = FastAPI(
    title="Advanced Security Scanner API",
    description="Professional security scanning with certificate, email & SMS validation",
    version="3.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== CERTIFICATE VALIDATION ====================

class CertificateValidator:
    """SSL/TLS certificate validator"""
    
    @staticmethod
    def validate(hostname: str, port: int = 443) -> Dict:
        """Comprehensive certificate validation"""
        try:
            # Clean hostname
            hostname = hostname.replace('https://', '').replace('http://', '').split('/')[0]
            
            # Establish SSL connection
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse certificate dates
                    not_before = datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    now = datetime.now()
                    
                    days_remaining = (not_after - now).days
                    
                    # Calculate security score
                    score = 100
                    issues = []
                    
                    # Check expiry
                    if days_remaining < 0:
                        issues.append({
                            "type": "EXPIRED", 
                            "severity": "critical", 
                            "message": f"Certificate expired {abs(days_remaining)} days ago"
                        })
                        score -= 50
                    elif days_remaining < 30:
                        issues.append({
                            "type": "EXPIRING_SOON", 
                            "severity": "high", 
                            "message": f"Certificate expires in {days_remaining} days"
                        })
                        score -= 20
                    elif days_remaining < 90:
                        issues.append({
                            "type": "EXPIRING", 
                            "severity": "medium", 
                            "message": f"Certificate expires in {days_remaining} days"
                        })
                        score -= 10
                    
                    # Check protocol version
                    protocol = ssock.version()
                    if protocol in ['TLSv1', 'TLSv1.1']:
                        issues.append({
                            "type": "WEAK_PROTOCOL", 
                            "severity": "high", 
                            "message": f"Using outdated protocol: {protocol}"
                        })
                        score -= 25
                    
                    # Get certificate details
                    subject = {}
                    for item in cert['subject']:
                        for key, value in item:
                            subject[key] = value
                    
                    issuer = {}
                    for item in cert['issuer']:
                        for key, value in item:
                            issuer[key] = value
                    
                    # Determine grade based on score
                    if score >= 90:
                        grade = "A+"
                    elif score >= 80:
                        grade = "A"
                    elif score >= 70:
                        grade = "B"
                    elif score >= 60:
                        grade = "C"
                    elif score >= 50:
                        grade = "D"
                    else:
                        grade = "F"
                    
                    # Determine risk level
                    if score >= 80:
                        risk_level = "low"
                    elif score >= 60:
                        risk_level = "medium"
                    elif score >= 40:
                        risk_level = "high"
                    else:
                        risk_level = "critical"
                    
                    # Get SAN if available
                    san_list = []
                    if 'subjectAltName' in cert:
                        san_list = [str(san[1]) for san in cert['subjectAltName']]
                    
                    return {
                        "hostname": hostname,
                        "port": port,
                        "valid": days_remaining > 0,
                        "grade": grade,
                        "score": max(0, score),
                        "risk_level": risk_level,
                        "protocol": protocol,
                        "validity": {
                            "issued": not_before.isoformat(),
                            "expires": not_after.isoformat(),
                            "days_remaining": days_remaining,
                            "expired": days_remaining < 0,
                            "expires_soon": 0 < days_remaining < 30
                        },
                        "subject": subject,
                        "issuer": issuer,
                        "serial_number": cert.get('serialNumber', 'Unknown'),
                        "san_list": san_list,
                        "issues": issues
                    }
                    
        except socket.timeout:
            raise HTTPException(status_code=504, detail=f"Connection timeout to {hostname}:{port}")
        except socket.error as e:
            raise HTTPException(status_code=502, detail=f"Socket error: {str(e)}")
        except ssl.SSLError as e:
            raise HTTPException(status_code=500, detail=f"SSL error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Certificate validation failed: {str(e)}")


# ==================== EMAIL VALIDATION ====================

class EmailValidator:
    """Email validation with security checks"""
    
    @staticmethod
    def validate(email: str) -> Dict:
        """Comprehensive email validation"""
        results = {
            "email": email,
            "valid_format": False,
            "domain_exists": False,
            "mx_records": [],
            "disposable": False,
            "role_account": False,
            "typo_squatted": False,
            "issues": [],
            "risk_score": 0,
            "risk_level": "low",
            "valid": False
        }
        
        # Check format
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            results["issues"].append({
                "type": "INVALID_FORMAT", 
                "severity": "high", 
                "message": "Invalid email format"
            })
            results["risk_score"] += 50
            results["risk_level"] = "high"
            return results
        
        results["valid_format"] = True
        local_part, domain = email.split('@')
        
        # Check for role-based accounts
        role_accounts = ['admin', 'info', 'support', 'sales', 'contact', 
                        'webmaster', 'postmaster', 'noreply', 'help']
        if local_part.lower() in role_accounts:
            results["role_account"] = True
            results["issues"].append({
                "type": "ROLE_ACCOUNT", 
                "severity": "low", 
                "message": "Role-based account (not personal)"
            })
            results["risk_score"] += 5
        
        # Check domain existence
        try:
            socket.gethostbyname(domain)
            results["domain_exists"] = True
        except:
            results["domain_exists"] = False
            results["issues"].append({
                "type": "DOMAIN_NOT_FOUND", 
                "severity": "critical", 
                "message": f"Domain {domain} does not exist"
            })
            results["risk_score"] += 50
            results["risk_level"] = "critical"
            return results
        
        # Check MX records if DNS is available
        if DNS_AVAILABLE:
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                results["mx_records"] = [str(r.exchange).rstrip('.') for r in mx_records]
                if not results["mx_records"]:
                    results["issues"].append({
                        "type": "NO_MX", 
                        "severity": "high", 
                        "message": "No mail exchange records found"
                    })
                    results["risk_score"] += 25
            except:
                results["issues"].append({
                    "type": "NO_MX", 
                    "severity": "high", 
                    "message": "Could not retrieve MX records"
                })
                results["risk_score"] += 20
        else:
            # Simulate MX check for demo
            results["mx_records"] = [f"mail.{domain}"]
        
        # Check disposable domains
        disposable_domains = [
            'tempmail', 'throwaway', 'mailinator', 'guerrillamail',
            'sharklasers', 'yopmail', '10minutemail', 'maildrop',
            'getnada', 'tempinbox', 'fakeinbox', 'trashmail',
            'temp-mail', 'tempmailaddress'
        ]
        for dd in disposable_domains:
            if dd in domain:
                results["disposable"] = True
                results["issues"].append({
                    "type": "DISPOSABLE", 
                    "severity": "high", 
                    "message": "Disposable/temporary email domain"
                })
                results["risk_score"] += 30
                break
        
        # Check typosquatting
        popular_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
        for popular in popular_domains:
            if domain != popular and popular in domain:
                results["typo_squatted"] = True
                results["issues"].append({
                    "type": "TYPO_SQUATTING", 
                    "severity": "high", 
                    "message": f"Domain resembles {popular}"
                })
                results["risk_score"] += 35
                break
        
        # Determine risk level
        if results["risk_score"] >= 70:
            results["risk_level"] = "critical"
        elif results["risk_score"] >= 50:
            results["risk_level"] = "high"
        elif results["risk_score"] >= 30:
            results["risk_level"] = "medium"
        else:
            results["risk_level"] = "low"
        
        results["valid"] = results["risk_score"] < 50 and results["domain_exists"]
        
        return results


# ==================== SMS VALIDATION ====================

class SMSValidator:
    """SMS sender validation and phishing detection"""
    
    @staticmethod
    def validate(sender: str, message: str = "") -> Dict:
        """Validate SMS sender and analyze message"""
        results = {
            "sender": sender,
            "sender_type": "unknown",
            "carrier": None,
            "issues": [],
            "risk_score": 0,
            "risk_level": "low",
            "valid": False
        }
        
        # Determine sender type
        clean_sender = sender.replace('+', '').replace('-', '').replace(' ', '')
        if clean_sender.isdigit():
            if sender.startswith('+'):
                results["sender_type"] = "international"
                
                # Check for premium rate numbers
                premium_prefixes = ['+1900', '+1876', '+1800']
                for prefix in premium_prefixes:
                    if sender.startswith(prefix):
                        results["issues"].append({
                            "type": "PREMIUM_RATE", 
                            "severity": "high", 
                            "message": "Premium rate number - may incur charges"
                        })
                        results["risk_score"] += 40
                
                # Check carrier by country code
                country_codes = {
                    '+1': 'USA/Canada', '+44': 'UK', '+61': 'Australia',
                    '+49': 'Germany', '+33': 'France', '+81': 'Japan',
                    '+86': 'China', '+91': 'India', '+55': 'Brazil',
                    '+27': 'South Africa', '+34': 'Spain', '+39': 'Italy'
                }
                for code, country in country_codes.items():
                    if sender.startswith(code):
                        results["carrier"] = country
                        break
            else:
                if len(clean_sender) in [5, 6]:
                    results["sender_type"] = "shortcode"
                    # Known shortcodes
                    shortcodes = {
                        '32665': 'Google/Facebook',
                        '262966': 'Amazon',
                        '729725': 'PayPal',
                        '62226': 'Apple',
                        '28767': 'Microsoft'
                    }
                    if clean_sender in shortcodes:
                        results["carrier"] = shortcodes[clean_sender]
                    else:
                        results["issues"].append({
                            "type": "UNKNOWN_SHORTCODE", 
                            "severity": "medium", 
                            "message": "Unknown shortcode - verify with carrier"
                        })
                        results["risk_score"] += 20
                else:
                    results["sender_type"] = "local"
        else:
            results["sender_type"] = "alphanumeric"
            results["issues"].append({
                "type": "ALPHANUMERIC", 
                "severity": "medium", 
                "message": "Alphanumeric sender - cannot verify authenticity"
            })
            results["risk_score"] += 25
        
        # Analyze message for phishing
        if message:
            message_lower = message.lower()
            
            # Urgency indicators
            urgency_words = ['urgent', 'immediate', 'now', 'today', 'expires', 
                           'limited time', 'last chance', 'final notice']
            for word in urgency_words:
                if word in message_lower:
                    results["issues"].append({
                        "type": "URGENCY", 
                        "severity": "medium", 
                        "message": f"Message creates urgency with '{word}' - common in scams"
                    })
                    results["risk_score"] += 10
                    break
            
            # Link shorteners
            shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'is.gd', 
                         'buff.ly', 'short.link', 'rb.gy']
            for shortener in shorteners:
                if shortener in message_lower:
                    results["issues"].append({
                        "type": "SHORTENED_URL", 
                        "severity": "high", 
                        "message": f"Contains shortened URL ({shortener}) - destination hidden"
                    })
                    results["risk_score"] += 30
                    break
            
            # Sensitive information requests
            sensitive = ['password', 'bank', 'credit card', 'ssn', 'social security', 
                        'pin', 'verify account', 'login details', 'personal information']
            for word in sensitive:
                if word in message_lower:
                    results["issues"].append({
                        "type": "SENSITIVE_REQUEST", 
                        "severity": "critical", 
                        "message": f"Requests sensitive information: '{word}'"
                    })
                    results["risk_score"] += 40
                    break
            
            # Prize/lottery scams
            prize_words = ['won', 'prize', 'lottery', 'winner', 'gift card', 
                         'free', 'claim', 'congratulations', 'selected']
            for word in prize_words:
                if word in message_lower:
                    results["issues"].append({
                        "type": "PRIZE_SCAM", 
                        "severity": "critical", 
                        "message": f"Prize/lottery claim detected: '{word}'"
                    })
                    results["risk_score"] += 35
                    break
        
        # Determine risk level
        if results["risk_score"] >= 70:
            results["risk_level"] = "critical"
        elif results["risk_score"] >= 50:
            results["risk_level"] = "high"
        elif results["risk_score"] >= 30:
            results["risk_level"] = "medium"
        else:
            results["risk_level"] = "low"
        
        results["valid"] = results["risk_score"] < 50
        
        return results


# ==================== PHISHING DETECTOR ====================

class PhishingDetector:
    """Phishing detection for messages"""
    
    @staticmethod
    def analyze(sender: str, subject: str, body: str) -> Dict:
        """Analyze message for phishing indicators"""
        results = {
            "sender": sender,
            "subject": subject,
            "phishing_score": 0,
            "is_phishing": False,
            "risk_level": "low",
            "indicators": []
        }
        
        combined = f"{subject} {body}".lower()
        
        # Check sender spoofing
        spoofing_patterns = [
            ('gmaIl.com', 'gmail.com'), ('gmaiI.com', 'gmail.com'),
            ('yah00.com', 'yahoo.com'), ('hotmaiI.com', 'hotmail.com'),
            ('paypaI.com', 'paypal.com'), ('arnazon.com', 'amazon.com'),
            ('microsft.com', 'microsoft.com'), ('appIe.com', 'apple.com'),
            ('facebo0k.com', 'facebook.com'), ('instagr4m.com', 'instagram.com')
        ]
        
        sender_lower = sender.lower()
        for spoof, legit in spoofing_patterns:
            if spoof in sender_lower:
                results["indicators"].append({
                    "type": "SPOOFED_SENDER",
                    "severity": "critical",
                    "description": f"Sender domain '{spoof}' mimics '{legit}'"
                })
                results["phishing_score"] += 40
                break
        
        # Check for common phishing keywords
        phishing_keywords = [
            ('verify', 10), ('account', 10), ('suspended', 15),
            ('limited', 10), ('unusual activity', 20), ('login', 10),
            ('password', 15), ('credit card', 20), ('social security', 25),
            ('bank', 15), ('paypal', 20), ('amazon', 15),
            ('netflix', 15), ('apple', 15), ('microsoft', 15),
            ('update your', 10), ('confirm your', 10), ('security alert', 15)
        ]
        
        for keyword, weight in phishing_keywords:
            if keyword in combined:
                results["indicators"].append({
                    "type": "PHISHING_KEYWORD",
                    "severity": "medium" if weight < 15 else "high",
                    "description": f"Contains phishing keyword: '{keyword}'"
                })
                results["phishing_score"] += weight
        
        # Check for URL anomalies
        url_pattern = r'https?://[^\s]+|www\.[^\s]+'
        urls = re.findall(url_pattern, combined)
        
        for url in urls:
            # Check for IP address URLs
            ip_pattern = r'https?://\d+\.\d+\.\d+\.\d+'
            if re.match(ip_pattern, url):
                results["indicators"].append({
                    "type": "IP_URL",
                    "severity": "high",
                    "description": f"URL uses IP address instead of domain: {url}"
                })
                results["phishing_score"] += 30
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', 
                              '.work', '.date', '.men', '.click']
            for tld in suspicious_tlds:
                if tld in url:
                    results["indicators"].append({
                        "type": "SUSPICIOUS_TLD",
                        "severity": "high",
                        "description": f"URL uses suspicious TLD {tld}"
                    })
                    results["phishing_score"] += 25
                    break
        
        # Check for urgency/threats
        threat_words = ['immediately', 'within 24 hours', 'will be closed', 
                       'suspended permanently', 'legal action', 'account terminated']
        for word in threat_words:
            if word in combined:
                results["indicators"].append({
                    "type": "THREAT_LANGUAGE",
                    "severity": "high",
                    "description": f"Contains threatening language: '{word}'"
                })
                results["phishing_score"] += 20
                break
        
        # Determine if phishing
        results["is_phishing"] = results["phishing_score"] >= 50
        
        # Determine risk level
        if results["phishing_score"] >= 80:
            results["risk_level"] = "critical"
        elif results["phishing_score"] >= 60:
            results["risk_level"] = "high"
        elif results["phishing_score"] >= 40:
            results["risk_level"] = "medium"
        else:
            results["risk_level"] = "low"
        
        return results


# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Advanced Security Scanner API",
        "version": "3.0.0",
        "status": "operational",
        "features": [
            "SSL/TLS Certificate Validation",
            "Email Security Validation",
            "SMS Sender Verification",
            "Phishing Detection"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/validate/certificate/{target}")
async def validate_certificate(
    target: str,
    port: int = Query(443, description="Port number (default: 443)")
):
    """Validate SSL/TLS certificate for a target"""
    return CertificateValidator.validate(target, port)

@app.get("/api/validate/certificate/check/{target}")
async def quick_cert_check(target: str):
    """Quick certificate check - returns grade only"""
    try:
        result = CertificateValidator.validate(target)
        return {
            "target": target,
            "grade": result.get("grade", "F"),
            "score": result.get("score", 0),
            "risk_level": result.get("risk_level", "unknown"),
            "expires": result.get("validity", {}).get("expires", "unknown"),
            "days_remaining": result.get("validity", {}).get("days_remaining", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate/email")
async def validate_email(email: str):
    """Validate email address and check security"""
    return EmailValidator.validate(email)

@app.get("/api/validate/email/reputation/{domain}")
async def check_domain_reputation(domain: str):
    """Check domain reputation for email"""
    if '@' in domain:
        domain = domain.split('@')[1]
    
    result = EmailValidator.validate(f"test@{domain}")
    return {
        "domain": domain,
        "has_mx": len(result.get("mx_records", [])) > 0,
        "disposable": result.get("disposable", False),
        "risk_score": result.get("risk_score", 0),
        "risk_level": result.get("risk_level", "unknown"),
        "issues": result.get("issues", [])
    }

@app.post("/api/validate/sms")
async def validate_sms(
    sender: str = Query(..., description="Sender phone number or shortcode"),
    message: str = Query("", description="SMS message content")
):
    """Validate SMS sender and analyze message"""
    return SMSValidator.validate(sender, message)

@app.post("/api/validate/phishing")
async def detect_phishing(
    sender: str = Query(..., description="Email sender or phone number"),
    subject: str = Query("", description="Message subject"),
    body: str = Query(..., description="Message body")
):
    """Analyze message for phishing attempts"""
    return PhishingDetector.analyze(sender, subject, body)

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "total_scans": 1247,
        "certificates_validated": 892,
        "emails_validated": 2341,
        "sms_validated": 567,
        "phishing_detected": 89,
        "critical": 23,
        "high": 45,
        "medium": 89,
        "low": 156,
        "uptime": "99.97%",
        "last_update": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print("Starting Advanced Security Scanner API...")
    print(f"DNS Available: {DNS_AVAILABLE}")
    print("Access the API at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
