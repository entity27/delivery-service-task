from pydantic import BaseModel
from typing_extensions import TypedDict


class CurrencyInfo(TypedDict):
    """
    Информация о валюте с CBR
    """

    ID: str
    NumCode: str
    CharCode: str
    Nominal: int
    Name: str
    Value: float
    Previous: float


class CurrencyDaily(TypedDict):
    """
    Ежедневный перечень курсов валют с CBR
    """

    Date: str
    PreviousDate: str
    PreviousURL: str
    Timestamp: str
    Valute: dict[str, CurrencyInfo]


class CurrencyDailyModel(BaseModel):
    """
    Модель для валидации ответа с CBR
    """

    Date: str
    PreviousDate: str
    PreviousURL: str
    Timestamp: str
    Valute: dict[str, CurrencyInfo]
