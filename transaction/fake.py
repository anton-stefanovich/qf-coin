from ._base import Transaction


class TransactionFake (Transaction):

    def commit(self) -> bool:
        return True
