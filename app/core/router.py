# FastAPI
from fastapi import APIRouter

# Routers
from app.api.v1.router import api_v1_router

core_router = APIRouter()
core_router.include_router(api_v1_router, prefix="/v1", tags=["v1"])

