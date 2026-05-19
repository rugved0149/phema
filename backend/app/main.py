from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from slowapi.middleware import SlowAPIMiddleware

from app.core.rate_limiter import (
    limiter,
    rate_limit_handler,
    rate_limit_exception
)

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
from app.api.auth_routes import router as auth_router

from app.db.base import Base,engine
from app.core.logger import logger


app=FastAPI(
    title="PHEMA Security Intelligence Platform",
    version="1.0.0"
)


app.state.limiter=limiter

app.add_exception_handler(
    rate_limit_exception,
    rate_limit_handler
)

app.add_middleware(SlowAPIMiddleware)


@app.middleware("http")
async def global_exception_handler(
    request:Request,
    call_next
):

    try:

        response=await call_next(request)

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
                "status":"error",
                "message":"Internal server error"
            }
        )


Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(auth_router)


@app.get("/health")
def health_check():

    try:

        with engine.connect() as conn:
            conn.execute("SELECT 1")

        return {
            "status":"ok",
            "database":"connected",
            "timestamp":datetime.utcnow()
        }

    except Exception as e:

        logger.error(
            f"Health check failed | Error: {str(e)}"
        )

        return {
            "status":"error",
            "database":"disconnected",
            "timestamp":datetime.utcnow()
        }