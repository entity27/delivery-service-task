import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.sessions.models import Session
from src.sessions.utils.session import generate_session_token


@pytest.fixture(scope='package')
def session_token() -> str:
    """
    Единый токен пользователя для тестов
    """
    return generate_session_token()


@pytest_asyncio.fixture(scope='package', loop_scope='session')
async def user_session(session_token: str, session_async: AsyncSession) -> Session:
    """
    Единая сессия пользователя
    """
    session = Session(token=session_token)
    session_async.add(session)
    await session_async.commit()
    await session_async.refresh(session)
    return session
