from pydantic import BaseModel


class SessionOut(BaseModel):
    message: str = 'Сессия установлена (cookie)'
