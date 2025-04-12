from secrets import token_urlsafe


def generate_session_token() -> str:
    return token_urlsafe(32)
