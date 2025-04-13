from src.utils.exceptions import CustomHTTPError


class CurrencyRequestError(CustomHTTPError):
    status_code = 500
    detail = 'Не удалось получить данные с CBR, ресурс не отвечает'


class CurrencyInvalidError(CustomHTTPError):
    status_code = 500
    detail = 'Не удалось извлечь JSON из ответа CBR'


class CurrencyNotFoundError(CustomHTTPError):
    status_code = 500
    detail = 'Данные CBR не содержат информации по валюте {currency}'
