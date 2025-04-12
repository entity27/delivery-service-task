from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.packages.constraints.package_type import MAX_NAME
from src.utils.models import IDModel

if TYPE_CHECKING:
    from src.packages.models.package import Package


class PackageType(IDModel):
    """
    Тип посылки

    Attributes:
        name: Название типа посылки
        packages: Список посылок по этому типу
    """

    __tablename__ = 'package_types'

    name: Mapped[str] = mapped_column(String(MAX_NAME), nullable=False, unique=True)
    packages: Mapped[list['Package']] = relationship(back_populates='package_type')
