class Supervisor:
    from account import Offer

    def __init__(self, rates: dict,
                 trade_rebound: float):
        from core.coin import Coin
        self.__data = dict(
            (currency, Coin(currency, rate))
            for currency, rate in rates.items())
        self.__trade_rebound = trade_rebound

    def reset(self, rates: dict = None):
        for currency, rate in rates.items():
            if currency in self.__data.keys():
                self.__data[currency].reset(rate)

    def feed(self, rates: dict) -> bool:
        if not rates:  # incorrect input data
            return False

        for currency, rate in rates.items():
            if currency in self.__data.keys():
                self.__data[currency].update(rate)

        return True  # all data has been processed

    def deal(self) -> Offer:
        from account import Offer

        release_items = tuple(sorted(
            self.__data, reverse=True, key=lambda key:
                self.__data[key].factor))

        source, target = tuple(currency for currency in (
            release_items[key] for key in (0, -1)))

        source_info, target_info = (
            self.__data[key] for key in (source, target))

        return Offer(source, target) if any(
            self.__trade_rebound < rebound_value for rebound_value in
            (source_info.rebound, target_info.rebound)) else None
