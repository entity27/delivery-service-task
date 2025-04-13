import asyncio
import json
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Any
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.backgrounds.tasks.register_package import _task  # noqa
from src.config.settings import BASE_DIR
from src.external.schemas.currency import CurrencyDaily, CurrencyDailyModel
from src.packages.cache.package_status import PackageStatusCache
from src.packages.models import Package
from tests.conftest import override_dependency


@pytest.fixture(autouse=True)
def patch_set_status(monkeypatch):  # type: ignore[no-untyped-def]
    """
    Патчим установку статуса
    """

    async def _(*_: Any, **__: Any) -> None: ...

    monkeypatch.setattr(
        'src.packages.cache.package_status.PackageStatusCache.set_status',
        _,
    )


@pytest.fixture(autouse=True)
def patch_celery_delay(monkeypatch):  # type: ignore[no-untyped-def]
    """
    Патчим вызов задачки
    """

    def sync_run(func, *args, **kwargs):  # type: ignore[no-untyped-def]
        with ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, func(*args, **kwargs))
            return future.result()

    monkeypatch.setattr(
        'src.backgrounds.tasks.register_package.delay',
        lambda *args, **kwargs: sync_run(_task, *args, **kwargs),  # type: ignore[no-untyped-call]
    )


@pytest.fixture(autouse=True)
def patch_currency_provider(monkeypatch):  # type: ignore[no-untyped-def]
    """
    Возвращаем тестовые данные CBR
    """

    async def get_daily(_):  # type: ignore[no-untyped-def]
        return load_cbr_data()

    monkeypatch.setattr(
        'src.external.providers.currency.CurrencyProvider.get_daily', get_daily
    )


def status_cache_mock() -> AsyncMock:
    """
    Мок создания статуса заявки
    """
    mock = AsyncMock()
    mock.new_status.return_value = uuid4()
    return mock


def load_cbr_data() -> CurrencyDaily:
    """
    Загружаем тестовые данные и одновременно проверяем, что они отражают актуальную CurrencyDaily схему
    """
    cbr = BASE_DIR / 'tests' / 'resources' / 'cbr.json'
    data = cbr.read_text(encoding='utf-8')
    daily: CurrencyDaily = json.loads(data)
    CurrencyDailyModel(**daily)
    return daily


@pytest.mark.asyncio(loop_scope='session')
async def test_registration(
    client: AsyncClient, session_token: str, session_async: AsyncSession
) -> None:
    """
    Проверяет, что API регистрации исправно работает
    """
    override_dependency(PackageStatusCache, status_cache_mock)
    url = '/packages/'

    payload = {'name': 'SOME UNIQUE NAME', 'weight': 1.5, 'price': 10.99, 'type': 1}
    client.cookies['session'] = session_token
    response = await client.post(url, json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data['uuid'] == str(UUID(data['uuid']))

    stm = select(Package).where(Package.name == 'SOME UNIQUE NAME')
    result = await session_async.execute(stm)
    package = result.scalar_one_or_none()
    assert package is not None, 'Посылка не зарегистрирована'
    assert package.cost is not None, 'Стоимость доставки не рассчитана'
