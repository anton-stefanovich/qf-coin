
class Trader:
    from account import Offer
    from argparse import Namespace

    def __init__(self, config: Namespace):

        # backup instance
        from .backup import Backup
        self.__backup = Backup(config)

        # account instance
        from .factory import target_account
        self.__account = target_account(
            config, self.__backup.amounts)

        # commander instance
        from .commander import Commander
        saved_rates = self.__backup.rates
        self.__commander = Commander(
            config, saved_rates
            if (isinstance(saved_rates, dict)
                and all(saved_rates.values()))
            else self.__account.last_rates)

        # getting the actual market info
        self.__account.amounts.update()

        from logging import info
        info('The new trader instance '
             'has been initialized')

    def go(self, attempts_limit: int = None):
        while ((attempts_limit is None) or attempts_limit > 0) \
                and self.__commander.feed(self.__account.rates):
            if isinstance(attempts_limit, int):
                attempts_limit -= 1

            if deal := self.__commander.deal():
                if self.__account.perform(deal):
                    self.__commander.reset(
                        dict.fromkeys(deal.coins))

            self.__backup.save(
                self.__account.amounts,
                self.__commander.serialize())

        from logging import info, shutdown
        info('Final cash amounts: %s %s',
             sum(self.__account.cash.values()),
             self.__account.cash)
        shutdown()
