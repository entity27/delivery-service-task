from sqlalchemy.orm import Mapped, mapped_column

from src.utils.sqlaclhemy import Base


class IDModel(Base):
    """
    Модель с ID в качестве PK
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
