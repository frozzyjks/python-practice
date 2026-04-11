from __future__ import annotations

import abc
from dataclasses import dataclass

__all__ = (
    "Order",
    "FixedDiscount",
    "PercentDiscount",
    "LoyaltyDiscount",
    "DiscountSelector",
)


@dataclass
class Order:
    total: float
    is_loyal: bool = False
    fixed_amount: float = 0
    percent: float = 0


class Discount(abc.ABC):
    @abc.abstractmethod
    def is_applicable(self, order: Order) -> bool:
        pass

    @abc.abstractmethod
    def apply(self, order: Order) -> None:
        pass


class FixedDiscount(Discount):
    def is_applicable(self, order: Order) -> bool:
        return order.fixed_amount > 0

    def apply(self, order: Order) -> None:
        pass


class PercentDiscount(Discount):
    def is_applicable(self, order: Order) -> bool:
        return order.percent > 0

    def apply(self, order: Order) -> None:
        pass


class LoyaltyDiscount(Discount):
    def is_applicable(self, order: Order) -> bool:
        return order.is_loyal

    def apply(self, order: Order) -> None:
        pass


class DiscountSelector:
    def __init__(self):
        self._discounts: list[Discount] = [
            FixedDiscount(),
            PercentDiscount(),
            LoyaltyDiscount(),
        ]

    def apply(self, order: Order) -> None:
        for discount in self._discounts:
            if discount.is_applicable(order):
                discount.apply(order)
