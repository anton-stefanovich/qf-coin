
class Trader:
    from account import Offer
    from argparse import Namespace

    def __init__(self, config: Namespace):
        from .factory import target_account
        self.__account = target_account(config)

        from .supervisor import Supervisor
        self.__analyst = Supervisor(
            self.__account.rates,
            config.trade_rebound)

        self._perform(
            self.__analyst.deal())

    def go(self):
        attempt = 0  # to show the number of attempts
        while self.__analyst.feed(self.__account.rates):
            attempt += 1  # new attempt started

            if deal := self.__analyst.deal():
                self._perform(deal)
                attempt = print('.' * attempt) or 0

        print('Final cash amounts:',
              sum(self.__account.cash.values()),
              self.__account.cash)

    def _perform(self, offer: Offer):
        if self.__account.perform(offer):
            self.__analyst.reset(
                dict.fromkeys(offer.coins))
