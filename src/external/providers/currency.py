import json
from typing import Self

from src.external.api.currency import CurrencyAPI
from src.external.cache import ExternalCache
from src.external.schemas.currency import CurrencyDaily, CurrencyDailyModel
from src.utils.dependencies import get_redis


class _Key:
    daily = 'daily'


class CurrencyProvider:
    def __init__(self, cache: ExternalCache, api: CurrencyAPI) -> None:
        """
        Кеширует запросы к CBR
        """
        self._cache = cache
        self._api = api

    @classmethod
    def default(cls) -> Self:
        """
        Создаёт провайдер со значениями по умолчанию
        """
        return cls(cache=ExternalCache(redis=get_redis()), api=CurrencyAPI())

    async def get_daily(self) -> CurrencyDaily:
        """
        Если есть запись в кеше, возвращает, в противном случае производит запрос ежедневных курсов валют с CBR
        """
        value = await self._cache.get(_Key.daily)

        if value is None:
            data: CurrencyDaily = await self._api.get_daily()
            CurrencyDailyModel(**data)
            await self._cache.set(_Key.daily, json.dumps(data))
            return data

        data = json.loads(value)
        return data
