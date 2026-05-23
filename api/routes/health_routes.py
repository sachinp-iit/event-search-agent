# api/routes/health_routes.py

from fastapi import APIRouter

from config.settings import settings


# ================================================
# API ROUTER INITIALIZATION
# ================================================
router = APIRouter(
    prefix = "/health",
    tags = ["Health"]
)


# ================================================
# BASIC API HEALTH CHECK
# ================================================
@router.get("/")
async def health_check():
    
    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
    
    
# ================================================
# READINESS CHECK
# ================================================
@router.get("/ready")
async def readiness_check():
    
    return {
        "status": "ready",
        "services": {
            "api": "running"
        }
    }
    

# ================================================
# LIVENESS CHECK
# ================================================
@router.get("/live")
async def liveness_check():
    
    return {
        "status": "alive"
    }