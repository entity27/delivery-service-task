from typing import Annotated

from fastapi import Depends
from sqlalchemy import select

from src.sessions.models import Session
from src.utils.repository import BaseRepository


class SessionRepository(BaseRepository[Session]):
    """
    Взаимодействие с объектами сессий
    """

    model = Session

    async def get_by_token(self, token: str) -> Session | None:
        stm = select(Session).where(Session.token == token)
        result = await self._session.execute(stm)
        return result.scalar_one_or_none()

    async def get_or_create(self, token: str) -> Session:
        """
        Возвращает сессию по токену, или создаёт, если нет
        """
        session = await self.get_by_token(token)
        if session is None:
            return await self.create(Session(token=token))
        return session


SessionRepositoryDep = Annotated[SessionRepository, Depends()]
