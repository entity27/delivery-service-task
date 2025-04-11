from fastapi import APIRouter

from src.package.routers import package

router = APIRouter()
router.include_router(package.router, prefix='/packages')
