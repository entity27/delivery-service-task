from decimal import Decimal

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.packages.models import Package, PackageType
from src.sessions.models import Session
from src.sessions.utils.session import generate_session_token


@pytest.fixture(scope='module')
def _token() -> str:
    return generate_session_token()


@pytest.mark.asyncio(loop_scope='session')
async def test_session(session_async: AsyncSession, _token: str) -> None:
    """
    Проверяем, что создание объектов работает
    """
    first = Session(token=generate_session_token())
    second = Session(token=_token)
    third = Session(token=_token)
    session_async.add(first)
    session_async.add(second)
    await session_async.commit()

    stm_single = select(Session).where(Session.token == _token)
    single = (await session_async.execute(stm_single)).scalar_one()
    assert single.token == _token

    stm_count = select(func.count()).select_from(Session)
    count = (await session_async.execute(stm_count)).scalar()
    assert count is not None and count >= 2

    session_async.add(third)
    with pytest.raises(IntegrityError):
        await session_async.commit()
    await session_async.rollback()


@pytest.mark.asyncio(loop_scope='session')
async def test_package(session_async: AsyncSession, _token: str) -> None:
    """
    Проверяем, что создание объектов работает
    """
    stm = select(Session).where(Session.token == _token)
    user = (await session_async.execute(stm)).scalar_one()

    types = (
        PackageType(name='раз'),
        PackageType(name='два'),
        PackageType(name='три'),
    )
    session_async.add_all(types)
    await session_async.flush()

    first = Package(
        name='Посылка',
        weight=Decimal('42.52'),
        price=Decimal('499.99'),
        package_type=types[0],
        session=user,
    )
    session_async.add(first)
    await session_async.commit()

    second = Package(
        name='Посылка',
        weight=Decimal('11.11'),
        price=Decimal('244.99'),
        package_type=types[1],
    )
    session_async.add(second)
    with pytest.raises(IntegrityError):
        await session_async.commit()
    await session_async.rollback()
