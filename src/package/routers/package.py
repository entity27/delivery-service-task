from fastapi import APIRouter, status

from src.utils.responses import OkResponse

router = APIRouter(tags=['Посылки'])


@router.get(
    path='/',
    response_model=OkResponse,
    status_code=status.HTTP_200_OK,
    summary='Заготовка',
    description='Проверяем, что болванка работает',
)
async def package_list() -> OkResponse:
    return OkResponse()
