# main.py
from fastapi import FastAPI

from config.settings import settings

from api.routes.health_routes import router as health_router

from api.routes.search_routes import router as search_router

from dotenv import load_dotenv

import uvicorn

# =========================================================
# LOAD ENVIRONMENT CONFIGURATION
# =========================================================
load_dotenv()


# =========================================================
# FASTAPI APPLICATION INITIALIZATION
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


# =========================================================
# REGISTER API ROUTES
# =========================================================

app.include_router(health_router)

app.include_router(search_router)


# =========================================================
# ROOT ENDPOINT
# =========================================================

@app.get("/")
async def root():

    return {
        "message": "Event Search Agent",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


# =========================================================
# APPLICATION STARTUP EVENT
# =========================================================

@app.on_event("startup")
async def startup_event():

    print("Application startup completed")


# =========================================================
# APPLICATION SHUTDOWN EVENT
# =========================================================

@app.on_event("shutdown")
async def shutdown_event():

    print("Application shutdown completed")