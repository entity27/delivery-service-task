from fastapi import APIRouter

from src.packages.routes import router as package_router

router = APIRouter()
router.include_router(package_router)
