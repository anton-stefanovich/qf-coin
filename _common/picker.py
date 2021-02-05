__PATH_DELIMITER__ = '>'
__PATH_KEY_ANY__ = '*'


def __collection_keys(container) -> list:
    return \
        (range(len(container))) if isinstance(container, (list, tuple)) else \
        (list(container.keys()) if isinstance(container, (dict, )) else list())


def pick_index(elements, index: int = None):
    from _common.converter import any_to_int
    index = any_to_int(index)

    # normalizing the index (None means 0, -1 means last, etc)
    index += len(elements)
    from sys import maxsize as max_int
    index %= len(elements) or max_int

    return elements[index] \
        if index in range(len(elements)) \
        else None


def pick_first(elements):
    return pick_index(elements, 0)


def pick_last(elements):
    return pick_index(elements, -1)


def pick_keys(element, *attrs):
    attr_value = element

    for attr in attrs:
        attr_value = getattr(
            attr_value, attr, None)

    return attr_value


def pick_key(element, key):
    return pick_keys(element, key)


def cherry_pick(container, keys=None, index: int = None, **kwargs):
    from _common.converter import iterable
    if kwargs or isinstance(keys, (dict, )):
        assert any((keys, kwargs,)) and not all((keys, kwargs,)), \
            f'Wrong parameters provided for picking elements: {locals()}'
        result = pick_blocks(container, **(keys or kwargs))

    else:
        # making a string path from input parameters
        keys = __PATH_DELIMITER__.join(str(key) for key in iterable(keys))

        # dropping extra spaces from delimiters
        keys = (key.strip() for key in keys.split(__PATH_DELIMITER__))

        # joining back to the string
        keys = __PATH_DELIMITER__.join(keys)

        # getting the result
        result = pick_values(container, keys)

    return result if index is None \
        else pick_index(result, index)


def cherry_pick_single(container, keys=None, allow_none: bool = True, **kwargs):
    values = cherry_pick(container, keys, **kwargs) or list()
    assert len(values) <= 1 and (allow_none or len(values)), \
        f'Not just one value presented for the path: {keys}'

    return pick_first(values)


def cherry_pick_first(container, keys=None, **kwargs):
    return cherry_pick(container, keys, 0, **kwargs)


def cherry_pick_last(container, keys=None, **kwargs):
    return cherry_pick(container, keys, -1, **kwargs)


def pick_values(container, path: str) -> list:
    assert path, 'Invalid container path provided'

    # setting the flag about deep search
    allow_deep_search = not path.startswith(2*__PATH_DELIMITER__)

    # stripping the path delimiters
    keys = path.lstrip(__PATH_DELIMITER__)

    # separate current key and other path
    key, *keys = keys.split(__PATH_DELIMITER__, 1)

    # converting the key value type
    key = int(key) if key.isdecimal() else key

    # restore end path
    keys = f'{__PATH_DELIMITER__}{keys.pop()}' if keys else None

    # getting keys for current nodes
    current_keys = __collection_keys(container)

    result = list()
    if key in current_keys:
        result.extend(
            pick_values(container[key], keys)
            if keys else [container[key]])

    if key == __PATH_KEY_ANY__:
        allow_deep_search = True
        path = keys  # avoid current

    if allow_deep_search:
        for key in current_keys:
            result.extend(pick_values(
                container[key], path))

    return result


def pick_blocks(container, **filter_dict) -> list:
    matched = list()  # list of filtered values
    assert isinstance(filter_dict, (dict, )), \
        'Not valid filter object type provided'

    if isinstance(container, (dict, )):
        # container = type(filter_dict)(container)

        if all(container.get(key, None) == value
                for key, value in filter_dict.items()):
            matched.append(container)

    for index in __collection_keys(container):
        matched.extend(pick_blocks(
            container[index], **filter_dict))

    return matched
