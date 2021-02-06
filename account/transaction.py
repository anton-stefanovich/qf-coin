from abc import ABC


class Transaction (ABC):
    from abc import abstractmethod

    @abstractmethod
    def commit(self) -> bool: pass
