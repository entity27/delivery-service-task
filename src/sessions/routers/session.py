from fastapi import APIRouter, status

from src.sessions.schemas.session import SessionOut
from src.sessions.services.session import SessionServiceDep

router = APIRouter(tags=['Сессии пользователей'])


@router.get(
    path='/new/',
    response_model=SessionOut,
    status_code=status.HTTP_200_OK,
    summary='Получить сессию',
    description='Генерирует токен сессии для пользователя, устанавливая в cookie',
)
async def session_new(service: SessionServiceDep) -> SessionOut:
    return service.new()
