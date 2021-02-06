from ..account import Account


class CoinbaseAccount (Account):
    from ..source import Source
    from ..transaction import Transaction

    @property
    def source(self) -> Source:
        from .source import CoinbaseSourceAPI
        return CoinbaseSourceAPI(None)  # FixMe

    __CB_BASE_URL__ = 'https://www.coinbase.com/api/v2'

    def __init__(self, assets: dict, auth_cookie: str, amounts: dict):
        super().__init__(amounts)

        self.__alias_map = dict(
            (alias, asset.get('asset_id', None))
            for alias, asset in assets.items())

        self.__accounts_map = dict((
            asset.get('id', None),
            asset.get('asset_id', None))
                for asset in assets.values())

        from requests import Session
        self.__session = Session()
        self.__session.cookies.update(
            dict(jwt=auth_cookie))

    def get_rates(self, base: str = 'USD') -> dict:
        rates_response = self.__session.get(
            f'{self.__CB_BASE_URL__}/assets/prices'
            f'?base={base}&filter=listed&resolution=latest')

        from tools.picker import cherry_pick_first
        return None if not rates_response else dict(
            (currency, float(cherry_pick_first(
                cherry_pick_first(rates_response.json(), base=currency),
                'latest'))) for currency in self.__alias_map.keys())

    def get_amounts(self) -> dict:
        accounts_response = self.__session.get(
            f'{self.__CB_BASE_URL__}/accounts?limit=100')

        from tools.picker import cherry_pick_first
        return None if not accounts_response else dict((
            cherry_pick_first(item, 'balance > currency'),
            float(cherry_pick_first(item, 'balance > amount')))
            for item in cherry_pick_first(
                accounts_response.json(), '_common'))

    def __decode_asset(self, value: str) -> str:
        return self.__alias_map.get(value, None) or \
               self.__accounts_map.get(value, value)

    def __decode_currency(self, value: str) -> str:
        return next((alias for alias, asset in self.__alias_map.items()
                     if asset == self.__decode_asset(value)), None)

    def exchange(self, source: str, target: str,
                 amount: float, currency: str = 'USD') -> Transaction:

        from .transaction import CoinbaseTransaction
        return None if not amount else CoinbaseTransaction(
            self.__session, self.__decode_asset(source),
            self.__decode_asset(target), amount, currency)

    def exchange_part(self, source: str, target: str, part: float) -> Transaction:
        part = part if part <= 1 else part / 100
        code = self.__decode_currency(source)
        amount = self.get_amounts().get(code)

        return self.exchange(source, target, part * amount, code) \
            if 0 <= part <= 1 and amount else None
