from decimal import Decimal

from src.packages.constraints.package import COST


def calculate_delivery_cost(weight: Decimal, price: Decimal, rate: Decimal) -> Decimal:
    """
    Высчитывает значение стоимости доставки

    Args:
        weight: Вес в килограммах
        price: Цена в долларах
        rate: Рейт USD/RUB
    """
    cost = (Decimal('0.5') * weight + Decimal('0.01') * price) * rate
    cost = cost.normalize()
    cost = round(cost, COST.scale)
    return cost
