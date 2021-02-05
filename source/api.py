from _common.picker import cherry_pick_first
from ._base import Source


class SourceAPI (Source):

    __last_access = None

    def __init__(self, config, *currencies):
        from pycoinbase.wallet.client import Client

        self.__client = Client(
            config.api_key, config.api_secret,
            api_version=config.api_version)

        known_accounts = self.__client \
            .get_accounts().response.json()

        self.__currencies = currencies
        accounts_details = dict(
            (currency, cherry_pick_first(
                known_accounts, name=f'{currency} Wallet'))
            for currency in self.__currencies)

        from account.coinbase import AccountCoinbase
        self.__account = AccountCoinbase(dict((currency, dict(
                id=cherry_pick_first(account_details, 'id'),
                asset_id=cherry_pick_first(account_details, 'asset_id')))
                                              for currency, account_details in accounts_details.items()),
                                         config.trade_cookie)

    def pop(self):
        from time import sleep, time
        if not self.__last_access:
            self.__last_access = time()
        else:
            sleep(max(0.0, self.__last_access + 7 - time()))
            self.__last_access = time()

        return self.__account.get_rates()
