from ..account import Account


class DebugAccount (Account):
    from argparse import Namespace
    from ..transaction import Transaction

    def __init__(self, config: Namespace):
        from .source import DebugSource
        super().__init__(dict(
            (currency, config.debug_amount) for currency in
            config.trade_currencies), DebugSource(config))
        self.__exchange_fee = config.debug_exchange_fee

    def perform(self, transaction: Transaction) -> bool:
        self.amounts.update(transaction.expected_current_amounts or dict())
        self.amounts[transaction.target] += transaction.amount * (1 - self.__exchange_fee)
        self.amounts[transaction.source] -= transaction.amount
        return True
