
class Trader:
    from argparse import Namespace
    from account import Account, Transaction

    def __init__(self, config: Namespace):
        from account import DebugAccount
        from account import CoinbaseAccount
        self.__account = DebugAccount(config) \
            if config.debug else CoinbaseAccount(config)

        from .analyst import Analyst
        self.__analyst = Analyst(
            self.__account.amounts,
            self.__account.rates,
            config.trade_percentage,
            config.trade_amount)

        if transaction := self.__analyst.transaction(force=True):
            if transaction.amount > config.trade_amount:
                self.__perform(transaction)

    def go(self):
        attempt = 0  # to show the number of attempts
        while self.__analyst.feed(self.__account.rates):
            attempt += 1  # new attempt started
            if transaction := self.__analyst.transaction():
                attempt = print('.' * attempt) or 0
                self.__perform(transaction)

    def __perform(self, transaction: Transaction):
        if self.__account.perform(transaction):
            self.__analyst.reset(self.__account.amounts)
            print(f'{transaction.source} -> {transaction.target} ('
                  f'{transaction.amount}):\t{self.__account.amounts}')
