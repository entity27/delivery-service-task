from typing import Annotated

from fastapi import Depends

from src.sessions.dependencies.cookie import SessionCookieDep
from src.sessions.exceptions.session import SessionInvalidError
from src.sessions.models import Session
from src.sessions.repositories.session import SessionRepositoryDep


async def get_session(
    token: SessionCookieDep, session_repo: SessionRepositoryDep
) -> Session:
    """
    Извлекает объект сессии по токену пользователя
    """
    session = await session_repo.get_by_token(token)
    if session is None:
        raise SessionInvalidError
    return session


SessionDep = Annotated[Session, Depends(get_session)]
