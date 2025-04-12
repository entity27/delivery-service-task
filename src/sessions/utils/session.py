from secrets import token_urlsafe


def generate_session_token() -> str:
    """
    Генерирует токен сессии
    """
    # 'nbytes' используется только здесь, так что выносить в constraint'ы необязательно
    return token_urlsafe(nbytes=32)
