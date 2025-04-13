from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.packages.constraints.package import MAX_NAME, WEIGHT


class PackageIn(BaseModel):
    """
    Модель регистрации посылки
    """

    name: str = Field(
        max_length=MAX_NAME,
        min_length=1,
        description='Название посылки',
    )
    weight: Decimal = Field(
        decimal_places=WEIGHT.scale,
        max_digits=WEIGHT.precision,
        description='Вес посылки в килограммах',
        gt=0,
    )
    price: Decimal = Field(
        decimal_places=WEIGHT.scale,
        max_digits=WEIGHT.precision,
        description='Стоимость содержимого посылки в долларах',
        gt=0,
    )
    package_type_id: int = Field(
        alias='package_type', description='ID типа посылки', gt=0
    )


class PackageOut(BaseModel):
    """
    Модель вывода информации о посылке
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    weight: Decimal
    price: Decimal
    cost: Decimal
    package_type: int = Field(alias='package_type_id')
