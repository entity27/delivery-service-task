from starlette import status

from src.utils.exceptions import CustomHTTPError


class SessionInvalidError(CustomHTTPError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Сессии не существует'
