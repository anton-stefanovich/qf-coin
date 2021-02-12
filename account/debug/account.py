from ..account import Account


class DebugAccount (Account):
    from argparse import Namespace
    from ..deal import Deal

    def __init__(self, config: Namespace):
        from .source import DebugSource
        source = DebugSource(config)

        super().__init__(dict(
            (currency, config.debug_amount / rate)
            for currency, rate in source.pop().items()),
            source, config)

        self.__exchange_fee = \
            config.debug_exchange_fee

    def _perform(self, deal: Deal) -> bool:
        self.amounts[deal.source] -= deal.amount / self.last_rates[deal.source]
        self.amounts[deal.target] += deal.amount / self.last_rates[deal.target] * \
            (1 - self.__exchange_fee)  # exchange fee

        return True
