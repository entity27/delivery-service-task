from starlette import status

from src.utils.exceptions import CustomHTTPError


class SessionCookieRequiredError(CustomHTTPError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Необходима cookie сессии'


class SessionCookieInvalidError(CustomHTTPError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Токен сессии невалиден'
