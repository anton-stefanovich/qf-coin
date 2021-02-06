from ..account import Account


class DebugAccount (Account):
    from ..source import Source
    from argparse import Namespace

    def __init__(self, config: Namespace):
        super().__init__(
            dict((currency, config.debug_amount)
                 for currency in config.trade_currencies))
        self.__exchange_fee = config.debug_exchange_fee
        self.__scope = config.debug_scope

    def exchange(self, source: str, target: str, amount: float):
        super().amounts[target] += amount * (1 - self.__exchange_fee)
        super().amounts[source] -= amount

        from .transaction import DebugTransaction
        return DebugTransaction()

    @property
    def source(self) -> Source:
        from .source import DebugSource
        return DebugSource(self.__scope,
                           *super().amounts.keys())
