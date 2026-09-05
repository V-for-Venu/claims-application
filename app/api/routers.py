from fastapi import APIRouter

from .endpoints import claims, providers

master_router = APIRouter()
master_router.include_router(claims.router)
master_router.include_router(providers.router)
