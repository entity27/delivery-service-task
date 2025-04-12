from typing import Annotated

from fastapi import Cookie, Depends

from src.sessions.exceptions.cookie import SessionCookieRequiredError


async def get_session_cookie(session: str | None = Cookie(None)) -> str:
    """
    Извлекает токен сессии из cookie
    """
    if session is None:
        raise SessionCookieRequiredError
    return session


SessionCookieDep = Annotated[str, Depends(get_session_cookie)]
