import itertools as it
from functools import partial, wraps
from typing import Any, Union, Sequence, Callable, Iterator
from io import IOBase

ps_dict = {'var1': [1, 2], 'var2': [3, 4], 'var3': [1, 2]}
ps_set = [[{key: entry} for entry in ps_dict[key]] for key in ps_dict]

test_prod = list(it.product(*ps_set))
test_zip = list(zip(*ps_set))
def merge_dicts(args: Sequence[dict]):
    dct = {}
    for entry in args:
        dct.update(entry)
    return dct

ret = [merge_dicts(entry) for entry in test_prod]




def itr(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args):
        # (arg1,)
        if len(args) == 1:
            arg = args[0]
            return func(arg if is_seq(arg) else [arg])
        # (arg1,...,argN)
        else:
            return func(args)

    return wrapper


# https://github.com/elcorto/pwtools
def is_seq(seq) -> bool:
    # проверяет что последовательность
    if (
            isinstance(seq, str)
            or isinstance(seq, IOBase)
            or isinstance(seq, dict)
    ):
        return False
    else:
        try:
            iter(seq)
            return True
        except TypeError:
            return False


def flatten(seq):
    for item in seq:
        if not is_seq(item):
            yield item
        else:
            for subitem in flatten(item):
                yield subitem


@itr
def merge_dicts(args: Sequence[dict]):
    """Start with an empty dict and update with each arg dict
    left-to-right."""
    dct = {}
    assert is_seq(args), f"input {args} is no sequence"
    for entry in args:
        assert isinstance(entry, dict), f"{entry} is no dict"
        dct.update(entry)
    return dct


ret = [merge_dicts(flatten(entry)) for entry in test_prod]


test = {'var1': 23, 'var2': 24, 'var3': {'var4': 25}}
test2 = {'var1': 23, 'var2': 24, 'var3': {'var4': 25,
                                          'var5': 26}}

def collect_fun(*dcts, resum = dict()):
    for dct in dcts:
        for key, val in dct.items():
            if type(val) is not dict:
                resum[key] = val
            else:
                collect_fun(val)
    return resum
collect_fun(test, test2, {'var73': 'hello'})