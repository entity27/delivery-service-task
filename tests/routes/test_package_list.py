from decimal import Decimal

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.packages.models import Package
from src.packages.repositories.package import PackageRepository
from src.sessions.models import Session


@pytest.mark.asyncio(loop_scope='session')
async def test_registration(
    client: AsyncClient, user_session: Session, session_async: AsyncSession
) -> None:
    """
    Проверяет, что API списка посылок исправно работает (есть фильтрация, пагинация)
    """
    url = '/packages/'
    repo = PackageRepository(session_async)

    p1 = Package(
        name='это мы не получим',
        weight=Decimal('1.0'),
        price=Decimal('1.0'),
        cost=Decimal('1.0'),
        package_type_id=1,
        session_id=user_session.id,
    )
    p2 = Package(
        name='это мы получим',
        weight=Decimal('1.0'),
        price=Decimal('1.0'),
        cost=None,
        package_type_id=3,
        session_id=user_session.id,
    )

    await repo.create(p1)
    await repo.create(p2)

    client.cookies['session'] = user_session.token
    response = await client.get(url, params={'type': 3, 'has_cost': False})

    assert response.status_code == 200
    data = response.json()
    assert 'results' in data
    assert len(data['results']) == 1
