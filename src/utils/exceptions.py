from typing import Any

from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    status_code: int = NotImplemented
    detail: str = NotImplemented

    def __init__(self, **format_kwargs: str) -> None:
        if format_kwargs:
            self.detail = self.detail.format(**format_kwargs)
        super().__init__(status_code=self.status_code, detail=self.detail)


def generate_custom_exception_responses(
    exceptions: list[type[CustomHTTPException]],
    description_per_status_code: dict[int, str] | None = None,
) -> dict[int | str, dict[str, Any]]:
    """
    Генерируем схему возможных ошибок для openapi документации

    Args:
        exceptions: Все возможные CustomHTTPException ошибки
        description_per_status_code: По желанию можно указать описание для каждого кода ошибки
                                     (ключ - код, значение - описание)
    """
    if description_per_status_code is None:
        description_per_status_code = {}

    docs: dict[int | str, dict[str, Any]] = {}
    for exception in exceptions:
        description = description_per_status_code.get(exception.status_code, '')
        str_type = exception.__name__
        if exception.status_code in docs:
            examples = docs[exception.status_code]['content']['application/json'][
                'examples'
            ]
            if str_type not in examples:
                examples[str_type] = {'value': None}
            examples[str_type]['value'] = {'detail': exception.detail}
        else:
            docs[exception.status_code] = {
                'description': description,
                'content': {
                    'application/json': {
                        'examples': {
                            str_type: {
                                'value': {
                                    'detail': exception.detail,
                                }
                            }
                        }
                    }
                },
            }

    return docs


class Http404(CustomHTTPException):
    status_code = 404
    detail = 'Страница не найдена'
