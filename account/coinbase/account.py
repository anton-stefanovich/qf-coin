from ..account import Account


class CoinbaseAccount (Account):
    from argparse import Namespace

    def __init__(self, config: Namespace):

        from .session import CoinbaseSession
        from .source import CoinbaseSourceAPI

        super().__init__(
            dict.fromkeys(config.trade_currencies),
            CoinbaseSourceAPI(config))

        from tools.picker import cherry_pick_first
        from pycoinbase.wallet.client import Client

        self.__session = CoinbaseSession(config)
        self.__client = Client(
            config.api_key, config.api_secret,
            api_version=config.api_version)

        known_accounts = self.__client \
            .get_accounts().response.json()
        self.__accounts = dict((currency, dict(
            (key, cherry_pick_first(account_details, key)) for key in ('id', 'asset_id')))
            for currency, account_details in dict((currency, cherry_pick_first(
                known_accounts, name=f'{currency.upper()} Wallet'))
                for currency in config.trade_currencies).items())

        self.__sync_amounts()

    def __sync_amounts(self):
        # FixMe: convert to the client usage
        from ._constants import __CB_BASE_URL__
        accounts_response = self.__session.get(
            f'{__CB_BASE_URL__}/accounts?limit=100')

        accounts_response = accounts_response.json() \
            if accounts_response else None

        # getting the map of native amounts
        from tools.picker import cherry_pick_first
        native_amounts = None if not accounts_response else dict(
            (currency, float(cherry_pick_first(cherry_pick_first(
                accounts_response, id=info.get('id')), 'balance > amount')))
            for currency, info in self.__accounts.items())

        self.amounts.update(dict(
            (currency, native_amounts[currency] * amount)
            for currency, amount in self.rates.items()))

    def exchange(self, source: str, target: str, amount: float,
                 expected_current_amounts: dict = None) -> bool:

        # perform transaction

        self.__sync_amounts()
        return all(0.05 > abs(self.amounts[currency] /
                   expected_current_amounts[currency] - 1)
                   for currency in self.amounts.keys())
