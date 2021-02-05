from abc import ABC, abstractmethod


class Source (ABC):

    @abstractmethod
    def pop(self):
        pass
