from ..transaction import Transaction


class DebugTransaction (Transaction):

    def commit(self) -> bool:
        return True
