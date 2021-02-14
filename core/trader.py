
class Trader:
    from account import Offer
    from argparse import Namespace

    def __init__(self, config: Namespace):
        from .factory import target_account
        from logging import info, basicConfig

        self.__account = target_account(config)
        self.__file = config.trade_status_file

        # noinspection PyArgumentList
        basicConfig(style=str().join(filter(
            lambda x: x in config.log_record_format, '%{$')),
                    format=config.log_record_format,
                    level=config.log_level.upper(),
                    datefmt=config.log_date_format,
                    filename=config.log_file_name)

        self.__data = self._load()
        from .supervisor import Supervisor
        self.__supervisor = Supervisor(
            self.__data or self.__account.last_rates,
            config.trade_rebound)

        info('The new trader instance '
             'has been initialized')

    def _load(self) -> dict:
        from pathlib import Path
        if Path(self.__file).is_file():
            from json import load
            with open(self.__file, 'r') as file:
                return load(file) or False

    def _save(self) -> bool:
        from json import dump
        with open(self.__file, 'w') as file:
            return dump(self.__supervisor.serialize(),
                        file, indent=2) or True

    def go(self, attempts_limit: int = None):
        while ((attempts_limit is None) or attempts_limit > 0) \
                and self.__supervisor.feed(self.__account.rates):
            if isinstance(attempts_limit, int):
                attempts_limit -= 1

            if deal := self.__supervisor.deal():
                self._perform(deal)

            self._save()

        from logging import info, shutdown
        info('Final cash amounts: %s %s',
             sum(self.__account.cash.values()),
             self.__account.cash)
        shutdown()

    def _perform(self, offer: Offer):
        if self.__account.perform(offer):
            self.__supervisor.reset(
                dict.fromkeys(offer.coins))
