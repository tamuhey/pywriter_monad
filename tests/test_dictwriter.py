from writer import DictWriter
from operator import add
from typing import List
import writer


def test_dictwriter():
    a = DictWriter(1, {"foo": "a"})

    def f(x):
        return DictWriter(x + 2, {"bar": "b"})

    assert writer.bind(f, a) == DictWriter(3, {"foo": "a", "bar": "b"})


def test_add_dictwriter():
    a = DictWriter(1, {"foo": "a"})
    b = DictWriter(2, {"bar": "b"})
    assert writer.add(add, a, b) == DictWriter(3, {"foo": "a", "bar": "b"})


def f(x: List[int]) -> DictWriter[List[int]]:
    return DictWriter(x + [1], {"foo": "a"})


def g(x: List[int]) -> DictWriter[List[int]]:
    return DictWriter([2, 3] + x, {"bar": "b"})


def test_dictwriter_compose():
    assert writer.compose(g, f)([100]) == DictWriter(
        [2, 3, 100, 1], {"foo": "a", "bar": "b"}
    )
