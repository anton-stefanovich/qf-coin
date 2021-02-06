
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
            if exchange_data := self.__analyst.exchange_data:

                self.__account.update(dict(
                    record for record in exchange_data))

                exchange_currencies, exchange_amounts = zip(*exchange_data)
                exchange_amount = (exchange_amounts[0] - exchange_amounts[-1]) / 2
                if transaction := self.__account.exchange(
                        exchange_currencies[0], exchange_currencies[-1], exchange_amount):
                    attempt = print('.' * attempt) or 0  # printing the number of attempts
                    print(f'{exchange_data}\t-> {exchange_amount}\t-> {self.__account.amounts}')
                    self.__analyst.reset(self.__account.amounts)
                    assert transaction.commit()
