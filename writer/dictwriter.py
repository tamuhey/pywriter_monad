from dataclasses import dataclass, field
from operator import add
from typing import Callable, Dict, Generic, List, Protocol, TypeVar, runtime_checkable
from toolz import compose, concat, curry, juxt, memoize, merge
from .writer import Monoid, Writer
import writer.writer as writer


T = TypeVar("T")


class DictM(dict):
    def __add__(self, other: Dict) -> Dict:
        return self.__class__(merge(self, other))


@dataclass
class DictWriter(Writer[T]):
    """Like the writer monad, it holds a writer `w` as a dict. Useful for logging."""

    a: T
    w: Dict = field(default_factory=DictM)

    def __post_init__(self):
        if not isinstance(self.w, dict):
            raise ValueError(
                f"expected `self.w` be `dict` type, but found {self.w} (type: {type(self.w)}"
            )
        self.w = DictM(self.w)


@curry
def add_dictwriter(
    add: Callable[[T, T], T], a: DictWriter[T], b: DictWriter[T],
) -> DictWriter[T]:
    c = add(a.a, b.a)
    w = merge(a.w, b.w)
    return DictWriter(c, w)


def dictwriter_compose(
    *funcs: Callable[[T], DictWriter]
) -> Callable[[T], DictWriter[T]]:
    assert len(funcs)
    last = funcs[-1]
    bind_funcs = [writer.bind(f) for f in funcs[:-1]] + [last]
    return compose(*bind_funcs)


# test


def test_dictwriter():
    a = DictWriter(1, {"foo": "a"})

    def f(x):
        return DictWriter(x + 2, {"bar": "b"})

    assert writer.bind(f, a) == DictWriter(3, {"foo": "a", "bar": "b"})


def test_add_dictwriter():
    a = DictWriter(1, {"foo": "a"})
    b = DictWriter(2, {"bar": "b"})
    assert add_dictwriter(add, a, b) == DictWriter(3, {"foo": "a", "bar": "b"})


def f(x: List[int]) -> DictWriter[List[int]]:
    return DictWriter(x + [1], {"foo": "a"})


def g(x: List[int]) -> DictWriter[List[int]]:
    return DictWriter([2, 3] + x, {"bar": "b"})


def test_dictwriter_compose():
    assert dictwriter_compose(g, f)([100]) == DictWriter(
        [2, 3, 100, 1], {"foo": "a", "bar": "b"}
    )

