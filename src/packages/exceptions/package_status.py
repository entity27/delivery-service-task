from src.utils.exceptions import CustomHTTPError


class PackageStatusDecodeError(CustomHTTPError):
    status_code = 500
    detail = 'Во время извлечения статуса произошла ошибка'


class PackageStatusNotFoundError(CustomHTTPError):
    status_code = 404
    detail = 'Посылки с таким UUID не существует'
