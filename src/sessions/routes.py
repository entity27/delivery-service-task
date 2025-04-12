from fastapi import APIRouter

from src.sessions.routers import session

router = APIRouter()
router.include_router(session.router, prefix='/sessions')
