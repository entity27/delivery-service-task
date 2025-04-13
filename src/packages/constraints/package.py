from src.utils.constraints import DecimalConstraint

# Максимальный размер именования
MAX_NAME = 512

# Максимальные границы по весу
WEIGHT = DecimalConstraint(precision=10, scale=2)

# Максимальные границы по цене содержимого
PRICE = DecimalConstraint(precision=10, scale=2)

# Максимальные границы по стоимости перевозки
COST = DecimalConstraint(precision=10, scale=2)
