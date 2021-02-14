from abc import ABC


class Source (ABC):
    from abc import abstractmethod

    @abstractmethod
    def pop(self, force: bool = False) -> dict: pass
