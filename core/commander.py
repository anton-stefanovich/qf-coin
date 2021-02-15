class Commander:
    from account import Offer
    from argparse import Namespace

    def __init__(self, config: Namespace, rates: dict):
        from core.coin import Coin
        self.__coins = dict(
            (currency, Coin(data))
            for currency, data in rates.items())
        self.__trade_rebound = config.trade_rebound

    def serialize(self) -> dict:
        return dict((key, data.serialize())
                    for key, data in self.__coins.items())

    def reset(self, rates: dict = None):
        for currency, rate in rates.items():
            if currency in self.__coins.keys():
                self.__coins[currency].reset(rate)

    def feed(self, rates: dict) -> bool:
        if not rates:  # incorrect input data
            return False

        for currency, rate in rates.items():
            if currency in self.__coins.keys():
                self.__coins[currency].update(rate)

        return True  # all data has been processed

    def deal(self) -> Offer:
        from account import Offer

        release_items = tuple(sorted(
            self.__coins, reverse=True, key=lambda key:
                self.__coins[key].factor))

        source, target = tuple(currency for currency in (
            release_items[key] for key in (0, -1)))

        source_info, target_info = (
            self.__coins[key] for key in (source, target))

        return Offer(source, target) if any(
            self.__trade_rebound < rebound_value for rebound_value in
            (source_info.rebound, target_info.rebound)) else None
