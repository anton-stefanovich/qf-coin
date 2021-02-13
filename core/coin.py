class Coin:

    __KEY_RATE_BASE__ = 'base'
    __KEY_RATE_PEAK__ = 'peak'
    __KEY_RATE_LAST__ = 'last'

    def __init__(self, data: (dict, float)):

        self.__data = dict()
        if isinstance(data, dict):
            assert all(key in data.keys() for key in (
                self.__KEY_RATE_BASE__, self.__KEY_RATE_PEAK__,
                self.__KEY_RATE_LAST__)), 'Invalid Coin data provided'
            self.__data.update(data)

        elif isinstance(data, float):
            self.reset(data)

    def serialize(self) -> dict:
        from copy import deepcopy
        return deepcopy(self.__data)

    def reset(self, rate: float):
        (self.__data[self.__KEY_RATE_BASE__],
         self.__data[self.__KEY_RATE_PEAK__],
         self.__data[self.__KEY_RATE_LAST__]) = (
            rate or self.__data[self.__KEY_RATE_LAST__],) * 3

    def update(self, rate: float):
        self.__data[self.__KEY_RATE_PEAK__] = \
            max(rate, self.__data[self.__KEY_RATE_PEAK__]) \
            if rate > self.__data[self.__KEY_RATE_BASE__] else \
            min(rate, self.__data[self.__KEY_RATE_PEAK__])

        self.__data[self.__KEY_RATE_LAST__] = rate

    @property
    def rebound(self) -> float:
        return ((self.__data[self.__KEY_RATE_PEAK__] - self.__data[self.__KEY_RATE_LAST__]) /
                (self.__data[self.__KEY_RATE_PEAK__] - self.__data[self.__KEY_RATE_BASE__])) if \
                (self.__data[self.__KEY_RATE_PEAK__] - self.__data[self.__KEY_RATE_BASE__]) else 0

    @property
    def factor(self) -> float:
        return self.__data[self.__KEY_RATE_LAST__] / self.__data[self.__KEY_RATE_BASE__]
