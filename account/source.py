from abc import ABC


class Source (ABC):
    from abc import abstractmethod

    @abstractmethod
    def pop(self, trade_timeout: float = None) -> dict: pass
