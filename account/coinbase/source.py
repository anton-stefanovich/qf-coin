from ..source import Source


class CoinbaseSourceAPI (Source):

    def __init__(self, config):
        from requests import Session
        self.__session = Session()
        self.__session.cookies.update(
            dict(jwt=config.trade_cookie))

        self.__trade_currencies = \
            (key.upper() for key in
             config.trade_currencies)

    def pop(self):
        from ._constants import __CB_BASE_URL__
        rates_response = self.__session.get(
            f'{__CB_BASE_URL__}/assets/prices'
            f'?base=USD&filter=listed&resolution=latest')

        from tools.picker import cherry_pick_first
        return None if not rates_response else dict(
            (currency.lower(), float(cherry_pick_first(
                cherry_pick_first(rates_response.json(), base=currency),
                'latest'))) for currency in self.__trade_currencies)
