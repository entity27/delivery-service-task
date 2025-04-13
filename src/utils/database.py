from collections.abc import AsyncGenerator, Iterator
from contextlib import asynccontextmanager
from typing import Never

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.dependencies import create_async_session


@asynccontextmanager
async def atomic(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[AsyncSession, Iterator[Never]]:
    """
    Атомарное взаимодействие с сессией
    """
    if db_session is None:
        session = create_async_session()
    else:
        session = db_session
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
