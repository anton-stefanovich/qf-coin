class Transaction:

    def __init__(self, source: str, target: str, amount: float,
                 expected_current_amounts: dict = None):
        self.__expected_current_amounts = expected_current_amounts
        self.__source, self.__target, self.__amount = source, target, amount

    @property
    def source(self) -> str:
        return self.__source

    @property
    def target(self) -> str:
        return self.__target

    @property
    def amount(self) -> float:
        return self.__amount

    @property
    def expected_current_amounts(self) -> dict:
        return self.__expected_current_amounts
