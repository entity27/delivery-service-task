from decimal import Decimal

from src.external.exceptions.currency import CurrencyNotFoundError
from src.external.schemas.currency import CurrencyDaily


def get_usd_rate(daily: CurrencyDaily) -> Decimal:
    """
    Отдаёт значение рейтов по USD
    """
    if 'USD' not in daily['Valute']:
        raise CurrencyNotFoundError(currency='USD')
    rate = daily['Valute']['USD']['Value']
    return Decimal(rate)
