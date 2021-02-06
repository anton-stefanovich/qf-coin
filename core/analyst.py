class Analyst:

    # all data for analyzing the market
    __data = dict()

    __KEY_AMOUNT__, __KEY_BASE__ = 'amount', 'base'
    __KEY_LAST__, __KEY_EDGE__ = 'last', 'edge'

    def __init__(self, amounts: dict, rates: dict = None,
                 trade_percentage: float = 0.01):
        self.__trade_percentage = trade_percentage
        self.reset(amounts, rates)

    @staticmethod
    def __pick_currency_rate(data: dict, key: str) -> float:
        return float(data.get(key, 0)) if data else 0

    def reset(self, amounts: dict, currencies: dict = None):
        currencies = currencies or dict(
            (currency, self.__data[currency][self.__KEY_LAST__])
            for currency in amounts.keys())

        self.__data = dict((currency, {
            self.__KEY_AMOUNT__: amount,
            self.__KEY_BASE__: currencies.get(currency),
            self.__KEY_EDGE__: currencies.get(currency),
            self.__KEY_LAST__: currencies.get(currency),
        }) for currency, amount in amounts.items())

    def feed(self, currencies: dict) -> bool:
        if not currencies:  # incorrect input data
            return False

        for key, value in currencies.items():
            target_dict = self.__data.get(key, dict())
            target_dict[self.__KEY_EDGE__] = \
                max(value, target_dict[self.__KEY_LAST__]) \
                if value > target_dict[self.__KEY_LAST__] else \
                min(value, target_dict[self.__KEY_LAST__])

            target_dict[self.__KEY_LAST__] = value

        return True  # all data has been processed

    @property
    def exchange_data(self):

        def amount(currency: str):
            currency_data = self.__data.get(currency)
            return currency_data[self.__KEY_AMOUNT__] / \
                currency_data[self.__KEY_BASE__] * \
                currency_data[self.__KEY_LAST__]

        # def actual_index_by_currency(currency: str):
        #     return self.__data.get(currency, dict())[self.__KEY_LAST__]

        ordered_data = tuple(sorted(
            self.__data, reverse=True,
            key=lambda key: amount(key)))

        exchange_pair = tuple(
            (key, amount(key))
            for key in (ordered_data[index]
                        for index in (0, -1)))

        return exchange_pair if self.__trade_percentage < \
            exchange_pair[0][1] / exchange_pair[1][1] - 1 else None
