from operator import add
from typing import Dict, List

import writer
from writer import Writer


def test_dictwriter():
    a = Writer(1, {"foo": "a"})

    def f(x: int):
        return Writer(x + 2, {"bar": "b"})

    assert writer.bind(f)(a) == Writer(3, {"foo": "a", "bar": "b"})


def test_add_dictwriter():
    a = Writer(1, {"foo": "a"})
    b = Writer(2, {"bar": "b"})
    assert writer.add(add)(a, b) == Writer(3, {"foo": "a", "bar": "b"})


def f(x: List[int]) -> Writer[List[int], Dict[str, str]]:
    return Writer(x + [1], {"foo": "a"})


def g(x: List[int]) -> Writer[List[int], Dict[str, str]]:
    return Writer([2, 3] + x, {"bar": "b"})


def test_dictwriter_compose():
    ret: Writer = writer.compose(g, f)([100])
    assert ret == Writer([2, 3, 100, 1], {"foo": "a", "bar": "b"})
