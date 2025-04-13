from src.utils.cache import RedisCache, RedisCacheAttrs


class ExternalCache(RedisCache, RedisCacheAttrs):
    cache_expire = 60 * 60 * 24
    subtype = 'external'

    async def set(self, key: str, value: str) -> None:
        """
        Устанавливает значение по ключу
        """
        await self._save(key, value)

    async def get(self, key: str) -> str | None:
        """
        Получение значения по ключу
        """
        return await self._get(key)

    async def delete(self, key: str) -> None:
        """
        Удаляет значение по ключу
        """
        await self._delete(key)
