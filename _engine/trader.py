
class Trader:
    from account import Account
    from argparse import Namespace

    def __init__(self, account: Account, config: Namespace):
        self.__account, self.__source = account, account.source

        from .analyst import Analyst
        self.__analyst = Analyst(
            self.__account.amounts,
            self.__source.pop(),
            config.trade_percentage)

    def go(self):
        while self.__analyst.feed(self.__source.pop()):
            if exchange_data := self.__analyst.exchange_data:

                self.__account.update(dict(
                    record for record in exchange_data))

                exchange_currencies, exchange_amounts = zip(*exchange_data)
                if transaction := self.__account.exchange(
                        exchange_currencies[0], exchange_currencies[-1],
                        exchange_amounts[0]/2 - exchange_amounts[-1]/2):
                    self.__analyst.reset(self.__account.amounts)
                    print(self.__account.amounts)
                    assert transaction.commit()
