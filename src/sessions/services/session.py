from typing import Annotated

from fastapi import Depends, Response

from src.sessions.schemas.session import SessionOut
from src.sessions.utils.cookie import SessionCookieManagerDep
from src.sessions.utils.session import generate_session_token


class SessionService:
    def __init__(self, manager: SessionCookieManagerDep, response: Response):
        self._manager = manager
        self._response = response

    def new(self) -> SessionOut:
        """
        Создаём токен сессии и устанавливаем в cookie response'а
        """
        token = generate_session_token()
        self._manager.set_cookie(self._response, token)
        return SessionOut()


SessionServiceDep = Annotated[SessionService, Depends()]
