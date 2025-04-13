from contextlib import suppress
from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends

from src.sessions.exceptions.cookie import (
    SessionCookieInvalidError,
    SessionCookieRequiredError,
)


async def get_session_cookie(session: str | None = Cookie(None)) -> str:
    """
    Извлекает токен сессии из cookie
    """
    if session is None:
        raise SessionCookieRequiredError
    with suppress(ValueError):
        return str(UUID(session))
    raise SessionCookieInvalidError


SessionCookieDep = Annotated[str, Depends(get_session_cookie)]
