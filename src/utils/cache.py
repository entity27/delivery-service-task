from abc import ABC, abstractmethod
from typing import Protocol

from redis.asyncio.client import Pipeline

from src.config.settings import settings
from src.utils.dependencies import RedisDep


class RedisCacheAttrs(Protocol):
    """
    Перечень необходимых аттрибутов при реализации кэша
    """

    cache_expire: int
    subtype: str


class RedisCache(ABC):
    cache_expire: int = settings.REDIS_CACHE_EXPIRE_SECONDS

    def __init__(self, redis: RedisDep):
        """
        Инициализируем соединение с редисом
        """
        self._con = redis
        self._prefix = settings.project_name

    @property
    @abstractmethod
    def subtype(self) -> str:
        """
        Подтип объекта, используется при составлении ключа
        """

    def _build_key(self, key: str | None) -> str:
        """
        Строит полный ключ
        """
        return f'{self._prefix}..{self.subtype}:{key}'

    async def _save(
        self, key: str | None, data: str, expire_duration: int | None = None
    ) -> None:
        """
        Сохраняет данные в кеш по ключу
        """
        if expire_duration is None:
            expire_duration = self.cache_expire

        key = f'{self._prefix}..{self.subtype}:{key}'
        pipe: Pipeline[str]
        async with self._con.pipeline() as pipe:
            await pipe.watch(key)
            await pipe.set(key, data, ex=expire_duration)

    async def _delete(self, key: str | None) -> None:
        """
        Удаляет значение по ключу
        """
        name = self._build_key(key)
        pipe: Pipeline[str]
        async with self._con.pipeline() as pipe:
            await pipe.watch(name)
            await pipe.delete(name)

    async def _get(self, key: str | None) -> str | None:
        """
        Получение данных из кеша
        """
        name = self._build_key(key)
        pipe: Pipeline[str]
        async with self._con.pipeline() as pipe:
            await pipe.watch(name)
            result: str = await pipe.get(name)
            return result
