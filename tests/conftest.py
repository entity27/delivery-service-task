from collections.abc import AsyncGenerator, Callable
from typing import Any
from unittest.mock import patch

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.main import app
from src.packages.models import PackageType
from src.utils.dependencies import get_session_async
from src.utils.sqlaclhemy import Base


def override_dependency(key: Callable[..., Any], value: Callable[..., Any]) -> None:
    """
    Подменяет зависимость по ключу на значение
    """
    dependencies: dict[Callable[..., Any], Callable[..., Any]] = (
        app.dependency_overrides  # noqa
    )
    dependencies[key] = value


@pytest_asyncio.fixture(scope='function', loop_scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    """
    Асинхронный клиент для тестовых запросов в локальный FastAPI
    """
    host, port = '127.0.0.1', 9000

    async with AsyncClient(
        transport=ASGITransport(app=app, client=(host, port)), base_url='http://test'
    ) as client:
        yield client


@pytest_asyncio.fixture(scope='session', loop_scope='session', autouse=True)
async def session_async() -> AsyncGenerator[AsyncSession, None]:
    """
    Сессия асинхронных запросов в in-memory sqlite БД
    """
    in_memory_engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with in_memory_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(in_memory_engine, expire_on_commit=False) as test_session:
        # Патчим atomic
        with patch('src.utils.database.create_async_session') as mock:
            mock.return_value = test_session
            await populate_db(test_session)
            override_dependency(get_session_async, lambda: test_session)
            yield test_session


async def populate_db(test_session: AsyncSession) -> None:
    """
    Создаём некоторые объекты заранее
    """
    package_types = [
        PackageType(name='1'),
        PackageType(name='2'),
        PackageType(name='3'),
    ]

    test_session.add_all(package_types)
    await test_session.commit()
