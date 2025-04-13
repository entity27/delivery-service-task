from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import Select, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.settings import settings

T = TypeVar('T', bound=BaseModel)


class PaginationIn(BaseModel):
    """
    Параметры пагинации
    """

    page: int = Field(default=1, ge=1, description='Номер страницы')
    size: int = Field(
        default=20, ge=1, le=100, description='Количество элементов на странице'
    )


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
    prefix: str,
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
        prefix: Префикс к пути запроса
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
        next_page = _make_url(host, pagination.page + 1, pagination.size, prefix)
    if pagination.page > 1:
        previous_page = _make_url(host, pagination.page - 1, pagination.size, prefix)

    return PaginationOut(
        count=count, next=next_page, previous=previous_page, results=items
    )


async def _count(statement: Select[Any], db_session: AsyncSession) -> int:
    subquery = statement.subquery()
    count_statement = select(func.count()).select_from(subquery)
    result = await db_session.execute(count_statement)
    count = result.scalar_one_or_none()
    return count or 0


def _make_url(host: str, page: int, size: int, prefix: str) -> str:
    return f'{host}{prefix}?page={page}&size={size}'
