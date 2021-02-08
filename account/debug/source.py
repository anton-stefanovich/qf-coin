from ..source import Source


class DebugSource (Source):
    from argparse import Namespace

    def __init__(self, config: Namespace):

        def load_test_data(currency: str) -> dict:
            with open(f'./data/{currency.lower()}.json') as file:
                from json import load
                return load(file)

        sources = dict(
            (currency, load_test_data(currency)['data']['prices']
                [config.debug_scope or 'day']['prices'])
            for currency in config.trade_currencies)

        sources = dict((currency, dict(
            (timestamp, value) for value, timestamp in source))
                for currency, source in sources.items())

        _sources = dict()
        for currency, values in sources.items():
            for timestamp, value in values.items():
                target = (_sources.get(timestamp) or dict())
                target.update({currency: float(value)})
                _sources[timestamp] = target

        self.__sources = list(filter(
            lambda source: all(_key in source.keys() for _key in sources.keys()),
            (_sources[_key] for _key in sorted(_sources.keys()))))

    def pop(self) -> dict:
        return self.__sources.pop(0) \
            if self.__sources else None
