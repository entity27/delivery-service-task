from fastapi import APIRouter

from src.packages.routes import router as package_router
from src.sessions.routes import router as session_router

router = APIRouter()
router.include_router(package_router)
router.include_router(session_router)
