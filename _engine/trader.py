
class Trader:
    from account import Account
    from argparse import Namespace

    def __init__(self, account: Account, config: Namespace):
        self.__account, self.__source = account, account.source

        from .analyst import Analyst
        self.__analyst = Analyst(
            self.__account.amounts,
            self.__source.pop(),
            config.trade_value)

    def go(self):
        while self.__analyst.feed(self.__source.pop()):
            if exchange_data := self.__analyst.exchange_data:
                source, target = exchange_data
                amount_source, amount_target = (
                    self.__analyst.amount(key)
                    for key in (source, target))

                self.__account.update({
                    source: amount_source,
                    target: amount_target})

                if transaction := \
                        self.__account.exchange(source, target, (
                        amount_source - amount_target) / 2):
                    self.__analyst.reset(self.__account.amounts)
                    print(self.__account.amounts)
                    assert transaction.commit()
