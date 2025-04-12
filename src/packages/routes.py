from fastapi import APIRouter

from src.packages.routers import package

router = APIRouter()
router.include_router(package.router, prefix='/packages')
