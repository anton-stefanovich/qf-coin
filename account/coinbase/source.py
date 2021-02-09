from ..source import Source


class CoinbaseSourceAPI (Source):

    __last_access = None

    def __init__(self, config):
        from .session import CoinbaseSession
        self.__session = CoinbaseSession(config)
        self.__trade_timeout = config.trade_timeout
        self.__trade_currencies = config.trade_currencies

    def pop(self, trade_timeout: float = None):
        from time import sleep, time
        sleep(max((self.__last_access or 0) - time() +
              self.__trade_timeout if trade_timeout is None
              else trade_timeout, 0))
        self.__last_access = time()

        from ._constants import __CB_BASE_URL__
        rates_response = self.__session.get(
            f'{__CB_BASE_URL__}/assets/prices'
            f'?base=USD&filter=listed&resolution=latest')

        from tools.picker import cherry_pick_first
        return None if not rates_response else dict(
            (currency, float(cherry_pick_first(
                cherry_pick_first(rates_response.json(), base=currency.upper()),
                'latest'))) for currency in self.__trade_currencies)
