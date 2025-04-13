import json
from contextlib import suppress
from json import JSONDecodeError
from typing import Annotated, TypedDict
from uuid import UUID, uuid4

from fastapi import Depends

from src.packages.exceptions.package_status import (
    PackageStatusDecodeError,
    PackageStatusNotFoundError,
)
from src.utils.cache import RedisCache, RedisCacheAttrs


class PackageStatusDict(TypedDict):
    """
    Статус текущей посылки

    Attributes:
        pending: Посылка находится в обработке, ожидайте (celery задача не завершилась)
        error: Во время обработки посылки произошла ошибка
        id: ID зарегистрированной посылки
    """

    pending: bool
    error: bool
    id: int | None


class PackageStatusCache(RedisCache, RedisCacheAttrs):
    cache_expire = 60 * 60 * 24
    subtype = 'package_status'

    async def new_status(self, session_id: int) -> UUID:
        """
        Создаёт статус для новой посылки, возвращает UUID статуса

        Args:
            session_id: ID сессии пользователя
        """
        uuid = uuid4()
        key = self._status_key(session_id, uuid)
        status = PackageStatusDict(
            pending=True,
            error=False,
            id=None,
        )
        await self._save(key, json.dumps(status))
        return uuid

    async def get_status(self, session_id: int, uuid: UUID) -> PackageStatusDict:
        """
        Получает статус

        Args:
            session_id: ID сессии пользователя
            uuid: UUID статуса
        """
        key = self._status_key(session_id, uuid)

        data = await self._get(key)
        if data is None:
            raise PackageStatusNotFoundError

        with suppress(JSONDecodeError):
            status: PackageStatusDict = json.loads(data)
            return status

        raise PackageStatusDecodeError

    async def set_status(
        self, session_id: int, uuid: UUID, status: PackageStatusDict
    ) -> None:
        """
        Устанавливает статус для посылки

        Args:
            session_id: ID сессии пользователя
            uuid: UUID статуса
            status: Значение статуса
        """
        key = self._status_key(session_id, uuid)
        await self._save(key, json.dumps(status))

    @staticmethod
    def _status_key(session_id: int, uuid: UUID) -> str:
        """
        Статус сохраняется по ключу ID сессии пользователя и UUID статуса
        """
        return f'{session_id}..{uuid}'


PackageStatusCacheDep = Annotated[PackageStatusCache, Depends()]
