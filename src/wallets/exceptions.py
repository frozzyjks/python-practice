class NegativeValueException(Exception):
    """Вызывается когда пытаемся снять больше денег, чем есть на балансе"""

    pass


class NotComparisonException(Exception):
    """Вызывается когда пытаемся складывать или вычитать деньги разных валют"""

    pass
