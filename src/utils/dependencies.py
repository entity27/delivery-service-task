from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.connections import engine_async, redis_pool


async def get_session_async() -> AsyncGenerator[AsyncSession, None]:
    """
    Возвращает асинхронную БД сессию

    otes:
        expire_on_commit=False, в противном случае,
        если мы не будет refresh'ить объект после коммита,
        то при передаче в pydantic или же явном обращении к аттрибутам
        мы словим ошибку, связанную с тредами greenlet'ов
    """
    async with AsyncSession(engine_async, expire_on_commit=False) as session:
        yield session


def get_redis() -> 'Redis[str]':
    """
    Возвращает соединение к Redis
    """
    return Redis(connection_pool=redis_pool, decode_responses=True)


if TYPE_CHECKING:
    RedisDep = Annotated[Redis[str], Depends(get_redis)]
else:
    RedisDep = Annotated[Redis, Depends(get_redis)]


AsyncSessionDep = Annotated[AsyncSession, Depends(get_session_async)]
