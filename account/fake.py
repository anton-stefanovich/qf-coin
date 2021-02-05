from ._base import Account, Source


class AccountFake (Account):
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

        from transaction import TransactionFake
        return TransactionFake()

    @property
    def source(self) -> Source:
        from source import SourceDebug
        return SourceDebug(self.__scope,
                           *super().amounts.keys())
