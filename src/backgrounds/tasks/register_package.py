from asyncio import get_event_loop
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.backgrounds.celery import app
from src.external.actions.currency import get_usd_rate
from src.external.exceptions.currency import CurrencyRequestError
from src.external.providers.currency import CurrencyProvider
from src.packages.actions.currency import calculate_delivery_cost
from src.packages.cache.package_status import PackageStatusCache, PackageStatusDict
from src.packages.models import Package
from src.packages.repositories.package import PackageRepository
from src.packages.schemas.package import PackageIn
from src.utils.database import atomic


@app.task(
    retry_backoff=True,
    max_retries=4,
    default_retry_delay=4,
    rate_limit='666/m',
    autoretry_for=(CurrencyRequestError,),
)  # type: ignore[misc]
def register_package(data: dict[str, Any], session_id: int, status_uuid: UUID) -> None:
    """
    Выполняет регистрацию посылки и расчет стоимости доставки

    Args:
        data: Данные о посылке (PackageIn)
        session_id: ID сессии пользователя
        status_uuid: UUID статуса посылки
    """
    package = PackageIn(**data)
    get_event_loop().run_until_complete(_task(package, session_id, status_uuid))


async def _task(data: PackageIn, session_id: int, status_uuid: UUID) -> None:
    """
    Пытается зарегистрировать посылку и обновляет статус в зависимости от успеха
    """
    status = PackageStatusDict(
        pending=False,
        error=False,
        id=None,
    )
    cache = PackageStatusCache.default()
    try:
        status['id'] = await _register_package(data, session_id)
    except:
        status['error'] = True
        await cache.set_status(session_id, status_uuid, status)
        raise
    await cache.set_status(session_id, status_uuid, status)


async def _register_package(data: PackageIn, session_id: int) -> int:
    """
    Выполняет регистрацию и расчёт стоимости доставки, возвращает ID посылки
    """
    provider = CurrencyProvider.default()
    daily = await provider.get_daily()
    rate = get_usd_rate(daily)
    cost = calculate_delivery_cost(data.weight, data.price, rate)

    session: AsyncSession
    async with atomic() as session:
        package_repo = PackageRepository(session)
        package = Package(
            name=data.name,
            weight=data.weight,
            price=data.price,
            cost=cost,
            package_type_id=data.package_type_id,
            session_id=session_id,
        )
        await package_repo.create(package)

    return package.id
