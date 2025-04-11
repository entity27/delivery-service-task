from fastapi import APIRouter

from src.package.routes import router as package_router

router = APIRouter()
router.include_router(package_router)
