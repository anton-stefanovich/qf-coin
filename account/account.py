from abc import ABC


class Account (ABC):
    from .source import Source
    from .transaction import Transaction
    from abc import abstractmethod

    __amounts = dict()

    def __init__(self, amounts: dict, source: Source):
        self.__amounts, self.__source = amounts, source

    @property
    def amounts(self) -> dict:
        return self.__amounts

    @property
    def rates(self) -> dict:
        return self.__source.pop()

    @abstractmethod
    def exchange(self, source: str, target: str, amount: float,
                 expected_current_amounts: dict = None) -> bool: pass

    def perform(self, transaction: Transaction) -> bool:
        return self.exchange(transaction.source, transaction.target,
                             transaction.amount, transaction.expected_current_amounts)

    def exchange_part(self, source: str, target: str, part: float):
        return self.exchange(source, target, self.__amounts.get(source) * part)

    def exchange_all(self, source: str, target: str):
        return self.exchange_part(source, target, 1)  # 1 = 100%
