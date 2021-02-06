from abc import ABC


class Account (ABC):
    from .source import Source
    from abc import abstractmethod

    __amounts = dict()

    def __init__(self, amounts: dict):
        self.update(amounts)

    @property
    def amounts(self) -> dict:
        return self.__amounts

    def update(self, amounts: dict):
        self.__amounts.update(amounts or dict())

    @property
    @abstractmethod
    def source(self) -> Source: pass

    @abstractmethod
    def exchange(self, source: str, target: str, amount: float): pass

    def exchange_part(self, source: str, target: str, part: float):
        return self.exchange(source, target, self.__amounts.get(source) / part)

    def exchange_all(self, source: str, target: str):
        return self.exchange_part(source, target, 1)  # 1 = 100%
