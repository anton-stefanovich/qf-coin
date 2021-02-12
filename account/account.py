from abc import ABC


class Account (ABC):
    from abc import abstractmethod
    from argparse import Namespace

    from .source import Source
    from .offer import Offer
    from .deal import Deal

    __amounts = dict()

    def __init__(self, amounts: dict, source: Source, config: Namespace):
        self.__trade_limit, self.__last_rates = config.trade_limit, None
        self.__amounts, self.__source = amounts, source

    @property
    def amounts(self) -> dict:
        return self.__amounts

    @property
    def rates(self) -> dict:
        current_rates = self.__source.pop()
        self.__last_rates = current_rates \
            if current_rates else self.last_rates
        return current_rates

    @property
    def last_rates(self) -> dict:
        return self.__last_rates

    @property
    def cash(self):
        return dict(  # generating cash money amounts
            (key, value * self.__amounts.get(key, 0))
            for key, value in self.last_rates.items())

    @abstractmethod
    def _perform(self, deal: Deal) -> bool: pass

    def perform(self, offer: Offer) -> bool:
        if not ((exchange_rates := self.rates) and offer):
            return print('Illegal offer or rates') or False

        source_value, target_value = (
            self.amounts[key] * exchange_rates[key]
            for key in (offer.source, offer.target))

        from .deal import Deal
        deal = Deal(offer, (source_value - target_value) / 2)

        trade_limit = self.__trade_limit if self.__trade_limit >= 1 \
            else self.__trade_limit * source_value

        if trade_limit > deal.amount:
            return print(f'WARNING: It\'s too less for trade: '
                         f'{deal.amount} {deal.currency} '
                         f'(min trade value: {trade_limit})') or False

        if not self._perform(deal):
            return print('Something went wrong and the deal '
                         f'({deal.amount} {deal.currency}) '
                         f'has not been performed') or False

        return print('INFO: Exchange has been performed: '
                     f'{deal.amount} {deal.currency} -> '
                     f'{self.cash}') or True
