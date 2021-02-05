from ._base import Source
from json import load


class SourceDebug (Source):

    def __init__(self, key: str = None, *currencies):

        def load_test_data(currency: str) -> dict:
            with open(f'./source/data/{currency}.json') as file:
                return load(file)

        assert len(currencies)

        sources = dict(
            (currency, load_test_data(currency)
                ['data']['prices'][key or 'day']['prices'])
            for currency in currencies)

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
            lambda source: all(_key in source.keys() for _key in currencies),
            (_sources[_key] for _key in sorted(_sources.keys()))))

    def pop(self) -> dict:
        return self.__sources.pop(0) \
            if self.__sources else None
