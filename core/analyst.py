class Analyst:
    from account import Transaction

    # all data for analyzing the market
    __data = dict()

    __KEY_AMOUNT__, __KEY_BASE__ = 'amount', 'base'
    __KEY_LAST__, __KEY_EDGE__ = 'last', 'edge'

    def __init__(self, amounts: dict, rates: dict = None,
                 trade_percentage: float = 0.01,
                 trade_amount: float = 1):
        self.__trade_percentage = trade_percentage
        self.__trade_amount = trade_amount
        self.reset(amounts, rates)

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
                max(value, target_dict[self.__KEY_EDGE__]) \
                if value > target_dict[self.__KEY_BASE__] else \
                min(value, target_dict[self.__KEY_EDGE__])

            target_dict[self.__KEY_LAST__] = value

        return True  # all data has been processed

    def __is_valid(self, transaction: Transaction) -> bool:
        source_rate, target_rate = tuple(
            self.__data.get(key)[self.__KEY_LAST__] /
            self.__data.get(key)[self.__KEY_EDGE__] - 1
            for key in (transaction.source, transaction.target))

        trade_amount = self.__trade_amount \
            if self.__trade_amount >= 1 else \
            max(self.__expected_amount(transaction.source) *
                self.__trade_amount, 1)

        return transaction.amount > trade_amount and \
            abs(source_rate - target_rate) > self.__trade_percentage

    def __expected_amount(self, currency: str):
        currency_data = self.__data.get(currency)
        return (currency_data[self.__KEY_AMOUNT__] /
                currency_data[self.__KEY_BASE__] *
                currency_data[self.__KEY_LAST__])

    def transaction(self, force: bool = False) -> Transaction:
        from account import Transaction

        release_items = tuple(sorted(
            self.__data, reverse=True, key=lambda key:
                self.__expected_amount(key)))

        source_info, target_info = tuple(
            (currency, self.__expected_amount(currency))
            for currency in (release_items[key] for key in (0, -1)))

        transaction = Transaction(
            source_info[0], target_info[0],
            (source_info[-1] - target_info[-1]) / 2,
            dict(record for record in (source_info, target_info)))

        return transaction \
            if force or self.__is_valid(transaction) \
            else None
