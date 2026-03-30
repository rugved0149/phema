# app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler

# Routers
from app.api.correlation_routes import router as correlation_router
from app.api.admin_routes import router as admin_router
from app.api.phema_routes import router as phema_router
from app.api.system_routes import router as system_router
from app.api.user_routes import router as user_router
from app.api.advice_routes import router as advice_router
from app.api.campaign_routes import router as campaign_router
from app.api.event_routes import router as event_router
from app.api.admin_user_routes import router as admin_user_router
from app.api.report_routes import router as report_router
# DB
from app.db.base import Base, engine

# Logger
from app.core.logger import logger

# RATE LIMITER

limiter = Limiter(
    key_func=get_remote_address
)

# FASTAPI APP

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
    version="1.0.0"
)

# ATTACH RATE LIMITER

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(SlowAPIMiddleware)

# GLOBAL ERROR HANDLER

@app.middleware("http")
async def global_exception_handler(
    request: Request,
    call_next
):
    """
    Catch unhandled exceptions globally.
    Prevents crashes and logs failures.
    """

    try:

        response = await call_next(request)

        return response

    except Exception as e:

        logger.error(
            f"Unhandled server error | "
            f"Path: {request.url.path} | "
            f"Error: {str(e)}"
        )

        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Internal server error"
            }
        )

# DATABASE INIT

Base.metadata.create_all(bind=engine)

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTERS

app.include_router(phema_router)
app.include_router(correlation_router)
app.include_router(admin_router)
app.include_router(system_router)
app.include_router(user_router)
app.include_router(advice_router)
app.include_router(campaign_router)
app.include_router(event_router)
app.include_router(admin_user_router)
app.include_router(report_router)
# HEALTH CHECK

@app.get("/health")
def health_check():

    try:

        # DB connectivity test
        with engine.connect() as conn:
            conn.execute("SELECT 1")

        return {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.utcnow()
        }

    except Exception as e:

        logger.error(
            f"Health check failed | Error: {str(e)}"
        )

        return {
            "status": "error",
            "database": "disconnected",
            "timestamp": datetime.utcnow()
        }