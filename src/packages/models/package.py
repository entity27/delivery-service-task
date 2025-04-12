from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.packages.constraints.package import COST, MAX_NAME, PRICE, WEIGHT
from src.utils.models import IDModel

if TYPE_CHECKING:
    from src.packages.models.package_type import PackageType
    from src.sessions.models.session import Session


class Package(IDModel):
    """
    Посылка

    Attributes:
        name: Название посылки
        weight: Вес посылки в килограммах
        price: Стоимость содержимого в долларах
        cost: Стоимость доставки в рублях
        package_type_id: FK на тип посылки
        package_type: Объект типа посылки
        session_id: FK на сессию пользователя
        session: Объект сессии пользователя
    """

    __tablename__ = 'packages'

    name: Mapped[str] = mapped_column(String(MAX_NAME), nullable=False)
    weight: Mapped[Decimal] = mapped_column(
        Numeric(WEIGHT.precision, WEIGHT.scale), nullable=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(PRICE.precision, PRICE.scale), nullable=False
    )
    cost: Mapped[Decimal] = mapped_column(
        Numeric(COST.precision, COST.scale), nullable=True
    )
    package_type_id: Mapped[int] = mapped_column(
        ForeignKey('package_types.id'), nullable=False
    )
    package_type: Mapped['PackageType'] = relationship(back_populates='packages')
    session_id: Mapped[int] = mapped_column(ForeignKey('sessions.id'), nullable=False)
    session: Mapped['Session'] = relationship(back_populates='packages')
