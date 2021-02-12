class Offer:

    def __init__(self, source: str, target: str):
        self.__currencies = source, target

    @property
    def coins(self) -> tuple:
        return self.__currencies

    @property
    def source(self) -> str:
        return self.__currencies[0]

    @property
    def target(self) -> str:
        return self.__currencies[-1]
