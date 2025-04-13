from json import JSONDecodeError

from httpx import AsyncClient, RequestError

from src.external.exceptions.currency import CurrencyInvalidError, CurrencyRequestError
from src.external.schemas.currency import CurrencyDaily


class CurrencyAPI:
    _url = 'https://www.cbr-xml-daily.ru/daily_json.js'

    async def get_daily(self) -> CurrencyDaily:
        """
        Делает запрос к CBR для получения актуального ежедневного курса валют
        """
        try:
            async with AsyncClient() as client:
                response = await client.get(self._url)
        except RequestError:
            raise CurrencyRequestError

        try:
            data: CurrencyDaily = response.json()
        except JSONDecodeError:
            raise CurrencyInvalidError

        return data
