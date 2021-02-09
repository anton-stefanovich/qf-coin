from ..account import Account


class DebugAccount (Account):
    from argparse import Namespace

    def __init__(self, config: Namespace):
        from .source import DebugSource
        super().__init__(dict(
            (currency, config.debug_amount) for currency in
            config.trade_currencies), DebugSource(config))
        self.__exchange_fee = config.debug_exchange_fee

    def exchange(self, source: str, target: str, amount: float,
                 expected_current_amounts: dict = None) -> bool:
        self.amounts.update(expected_current_amounts or dict())
        self.amounts[target] += amount * (1 - self.__exchange_fee)
        self.amounts[source] -= amount
        return True
