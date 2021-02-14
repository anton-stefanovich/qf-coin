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

    def _rates(self, force: bool = False) -> dict:
        current_rates = self.__source.pop(force)
        self.__last_rates = current_rates \
            if current_rates else self.last_rates
        return current_rates

    @property
    def rates(self) -> dict:
        return self._rates()

    @property
    def last_rates(self) -> dict:
        return self.__last_rates or self._rates(True)

    @property
    def cash(self):
        return dict(  # generating cash money amounts
            (key, value * self.__amounts.get(key, 0))
            for key, value in self.last_rates.items())

    @abstractmethod
    def _perform(self, deal: Deal) -> bool: pass

    def perform(self, offer: Offer) -> bool:
        from logging import error, info, debug
        if not ((exchange_rates := self.rates) and offer):
            return error('Illegal offer or rates') or False

        source_value, target_value = (
            self.amounts[key] * exchange_rates[key]
            for key in (offer.source, offer.target))

        from .deal import Deal
        deal = Deal(offer, (source_value - target_value) / 2)

        trade_limit = self.__trade_limit if self.__trade_limit >= 1 \
            else self.__trade_limit * source_value

        if trade_limit > deal.amount:
            return debug('It\'s too less for trade: '
                         '%s %s (min trade value: %s)',
                         deal.amount, deal.currency,
                         trade_limit) or False

        if not self._perform(deal):
            return error('Something went wrong and '
                         'the deal (%s %s) has not been performed',
                         deal.amount, deal.currency) or False

        return info('Exchange has been performed: %s %s -> %s',
                    deal.amount, deal.currency, self.cash) or True
