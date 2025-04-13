from fastapi import APIRouter

from src.packages.routers import package, package_type

router = APIRouter()
router.include_router(package.router, prefix='/packages')
router.include_router(package_type.router, prefix='/types')
