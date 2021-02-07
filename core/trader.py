
class Trader:
    from account import Account
    from argparse import Namespace

    def __init__(self, account: Account, config: Namespace):
        self.__account, self.__source = account, account.source

        from .analyst import Analyst
        self.__analyst = Analyst(
            self.__account.amounts,
            self.__source.pop(),
            config.trade_percentage,
            config.trade_amount)

    def go(self):
        attempt = 0  # to show the number of attempts
        while self.__analyst.feed(self.__source.pop()):
            attempt += 1  # new attempt started
            if transaction := self.__analyst.transaction:
                if self.__account.perform(transaction):
                    attempt = print('.' * attempt) or 0
                    self.__analyst.reset(self.__account.amounts)
                    print(f'{transaction.source} -> {transaction.target} ('
                          f'{transaction.amount}):\t{self.__account.amounts}')
