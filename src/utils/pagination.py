from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import Select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings

T = TypeVar('T', bound=BaseModel)


class PaginationIn(BaseModel):
    """
    Параметры пагинации
    """

    page: int = Field(default=1, ge=1, description='Номер страницы')
    size: int = Field(default=20, ge=1, description='Количество элементов на странице')


class PaginationOut(BaseModel, Generic[T]):
    """
    Страница пагинации
    """

    count: int
    next: str | None
    previous: str | None
    results: Sequence[T]


async def paginate(
    statement: Select[Any],
    pagination: PaginationIn,
    db_session: AsyncSession,
    model: type[T],
) -> PaginationOut[T]:
    """
    Выполняет пагинацию запроса списка репозитория

    Notes:
        Подразумевается, что модель запроса имеет колонку с ID

    Args:
        statement: Query запроса
        pagination: Настройки пагинации
        db_session: Сессия БД
        model: Pydantic модель, используемая в качестве элементов страницы
    """
    offset = (pagination.page - 1) * pagination.size
    limit = pagination.size
    count = await _count(statement, db_session)

    statement = statement.offset(offset).limit(limit).order_by(text('id desc'))
    result = (await db_session.execute(statement)).scalars().all()

    items = [model.model_validate(item, from_attributes=True) for item in result]
    left = offset + pagination.size < count

    host = str(settings.HOST_URL)
    next_page = None
    previous_page = None

    if left:
        next_page = _make_url(host, pagination.page + 1, pagination.size)
    if pagination.page > 1:
        previous_page = _make_url(host, pagination.page - 1, pagination.size)

    return PaginationOut(
        count=count, next=next_page, previous=previous_page, results=items
    )


async def _count(statement: Select[Any], db_session: AsyncSession) -> int:
    result = await db_session.execute(statement)
    count = result.scalar_one_or_none()
    return count or 0


def _make_url(host: str, page: int, size: int) -> str:
    return f'{host}?page={page}&size={size}'
