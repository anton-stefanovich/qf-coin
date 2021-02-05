from abc import ABC, abstractmethod


class Transaction (ABC):

    @abstractmethod
    def commit(self) -> bool: pass
