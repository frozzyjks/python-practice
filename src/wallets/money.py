from dataclasses import dataclass, field

from src.wallets.exceptions import NegativeValueException, NotComparisonException


@dataclass
class Money:
    value: float
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise NotComparisonException(
                f"Нельзя складывать {self.currency} и {other.currency}"
            )
        return Money(value=self.value + other.value, currency=self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise NotComparisonException(
                f"Нельзя вычитать {self.currency} и {other.currency}"
            )
        return Money(value=self.value - other.value, currency=self.currency)


@dataclass
class Wallet:
    currencies: dict = field(default_factory=dict)

    def __init__(self, *args: Money):
        self.currencies = {}
        for money in args:
            self.currencies[money.currency] = money

    def __getitem__(self, currency: str) -> Money:
        return self.currencies.get(currency, Money(value=0, currency=currency))

    def __delitem__(self, currency: str) -> None:
        if currency in self.currencies:
            del self.currencies[currency]

    def __len__(self) -> int:
        return len(self.currencies)

    def __contains__(self, currency: str) -> bool:
        return currency in self.currencies

    def add(self, money: Money) -> "Wallet":
        if money.currency in self.currencies:
            self.currencies[money.currency] = self.currencies[money.currency] + money
        else:
            self.currencies[money.currency] = money
        return self

    def sub(self, money: Money) -> "Wallet":
        current = self[money.currency]
        new_balance = current - money

        if new_balance.value < 0:
            raise NegativeValueException(
                f"Недостаточно средств: есть {current.value} {money.currency}, "
                f"пытаетесь снять {money.value}"
            )

        self.currencies[money.currency] = new_balance
        return self
