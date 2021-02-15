class Backup:
    __DUMP_KEY_RATES__ = 'rates'
    __DUMP_KEY_AMOUNT__ = 'amount'
    from argparse import Namespace

    def __init__(self, config: Namespace):
        self.__filename = config.trade_status_file
        self.__amounts, self.__rates = None, None
        self.reload()

    def save(self, amounts: dict = None,
             rates: dict = None) -> bool:
        amounts = amounts or self.__amounts
        rates = rates or self.__rates

        data = dict((key, {
            self.__DUMP_KEY_AMOUNT__: amounts.get(key),
            self.__DUMP_KEY_RATES__:  rates.get(key),
        }) for key in amounts.keys())

        from json import dump
        with open(self.__filename, 'w') as file:
            return dump(data, file, indent=2) or True

    def reload(self) -> bool:
        data = dict()  # initial data set

        from pathlib import Path
        if Path(self.__filename).is_file():
            from json import load
            with open(self.__filename, 'r') as file:
                data = load(file)  # reading the file

        if not data:      # means the data
            return False  # hasn't been loaded

        self.__amounts, self.__rates = tuple(dict(
            (currency, data[currency].get(key)) for currency in data.keys())
            for key in (self.__DUMP_KEY_AMOUNT__, self.__DUMP_KEY_RATES__))

        return True

    @property
    def amounts(self):
        from copy import deepcopy
        return deepcopy(self.__amounts)

    @property
    def rates(self):
        from copy import deepcopy
        return deepcopy(self.__rates)
