from enum import IntEnum


__BOOL_MAPPER = {
    True:  ['true', 't', 'yes', 'y', 'on', 'enable', 'enabled', '1'],
    False: ['false', 'f', 'no', 'n', 'off', 'disable', 'disabled', '0'],
}


def any_to_bool(value: (bool, str)) -> bool:
    if isinstance(value, bool):
        return value

    for key, aliases in __BOOL_MAPPER.items():
        if str(value).lower() in aliases:
            return key

    else:
        from argparse import ArgumentTypeError
        raise ArgumentTypeError(f'Can\'t convert `{value}` to boolean value')


def any_to_int(index: any) -> int:
    if isinstance(index, IntEnum):
        index = index.value

    elif index is None:
        index = 0

    assert isinstance(index, int), \
        'Wrong index type provided'

    return index


def iterable(obj: any, save_none_value: bool = False) -> tuple:
    if obj is None and not save_none_value:
        return tuple()  # making empty tuple (None means empty tuple required)

    # from requests.structures import CaseInsensitiveDict
    if isinstance(obj, (str, dict,)):  # CaseInsensitiveDict)):
        return obj,     # making tuple from string or dict (string is iterable by characters)

    if hasattr(obj, '__iter__'):
        return obj      # returning iterable object as is without any conversion

    return obj,         # converting the object to the tuple by default
