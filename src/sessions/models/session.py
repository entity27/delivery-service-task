from secrets import token_urlsafe
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    token: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True, default=lambda: token_urlsafe(32)
    )
    packages: Mapped['Package'] = relationship(back_populates='session')
