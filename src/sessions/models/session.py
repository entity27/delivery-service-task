from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.sessions.constraints.session import TOKEN_SIZE
from src.utils.models import IDModel

if TYPE_CHECKING:
    from src.packages.models.package import Package


class Session(IDModel):
    """
    Сессия пользователя

    Attributes:
        token: Токен сессии пользователя
    """

    __tablename__ = 'sessions'

    token: Mapped[str] = mapped_column(String(TOKEN_SIZE), nullable=False, unique=True)
    packages: Mapped['Package'] = relationship(back_populates='session')
