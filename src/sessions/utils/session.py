from uuid import uuid4


def generate_session_token() -> str:
    """
    Генерирует токен сессии
    """
    return str(uuid4())
