# app/main.py

from fastapi import FastAPI
from app.api.correlation_routes import router as correlation_router
from app.api.admin_routes import router as admin_router
from app.api.phema_routes import router as phema_router
from app.db.base import Base, engine
from app.api.system_routes import router as system_router

app = FastAPI(
        title="PHEMA Security Intelligence Platform",
        description="""
    PHEMA (Phishing & Hybrid Event Monitoring Architecture)

    A multi-layer cyber defense platform that detects and correlates multiple attack signals including:

    • Phishing URLs  
    • Social engineering language manipulation  
    • Malicious file indicators  
    • Honeypot interactions  
    • Behavioral anomalies  

    The system correlates signals across modules to produce a unified risk score and attack classification.

    Core Capabilities:

    • Multi-module threat detection  
    • Event correlation engine  
    • MITRE ATT&CK mapping  
    • Attack timeline reconstruction  
    • Threat memory tracking  
    • Campaign detection  
    • Security analytics dashboard  
    • Live threat feed monitoring
    """,
        version="1.0.0",
        contact={
            "name": "PHEMA Security Platform",
            "url": "https://github.com/",
        },
    )

# Create DB tables
Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(phema_router)
app.include_router(correlation_router)
app.include_router(admin_router)
app.include_router(system_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}