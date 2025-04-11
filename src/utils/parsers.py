from typing import Any


def parse_nullable_value(v: Any) -> Any | None:
    """
    Если значение не истинно, возвращаем None
    """
    if isinstance(v, str) and v == 'None':
        return None
    if v:
        return v
    return None
