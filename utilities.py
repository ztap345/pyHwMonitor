from functools import reduce
from operator import getitem


def get_nested_item(data: list | dict, keys: list[str]):
    try:
        return reduce(getitem, keys, data)
    except LookupError as e:
        print("Lookup error")
        return None

