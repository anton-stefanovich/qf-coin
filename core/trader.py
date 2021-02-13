
class Trader:
    from account import Offer
    from argparse import Namespace

    def __init__(self, config: Namespace):
        from .factory import target_account
        self.__account = target_account(config)
        self.__file = config.trade_status_file

        self.__data = self._load()
        from .supervisor import Supervisor
        self.__supervisor = Supervisor(
            self.__data or self.__account.rates,
            config.trade_rebound)

    def _load(self) -> dict:
        from pathlib import Path
        if Path(self.__file).is_file():
            from json import load
            with open(self.__file, 'r') as file:
                return load(file) or False

    def _dump(self) -> bool:
        from json import dump
        with open(self.__file, 'w') as file:
            return dump(self.__supervisor.serialize(),
                        file, indent=2) or True

    def go(self, attempts_limit: int = None):
        while ((attempts_limit is None) or attempts_limit > 0) \
                and self.__supervisor.feed(self.__account.rates):
            self._dump()  # saving the current status

            if isinstance(attempts_limit, int):
                attempts_limit -= 1

            if deal := self.__supervisor.deal():
                self._perform(deal)

        print('Final cash amounts:',
              sum(self.__account.cash.values()),
              self.__account.cash)

    def _perform(self, offer: Offer):
        if self.__account.perform(offer):
            self.__supervisor.reset(
                dict.fromkeys(offer.coins))
