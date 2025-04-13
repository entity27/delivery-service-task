from src.utils.exceptions import CustomHTTPError


class PackageTypeNotExistsError(CustomHTTPError):
    status_code = 400
    detail = 'Типа посылки с переданным ID не существует'
