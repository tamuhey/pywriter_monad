from dataclasses import dataclass, field
from typing import Callable, Generic, Protocol, TypeVar, runtime_checkable
import toolz
from typing_extensions import Protocol


T = TypeVar("T")


@runtime_checkable
class Monoid(Protocol):
    def __add__(self, other: "Monoid") -> "Monoid":
        ...

    @classmethod
    def mempty(cls) -> "Monoid":
        ...


@dataclass
class Writer(Generic[T]):
    """Writer Monad"""

    a: T
    w: Monoid = field(default_factory=Monoid.mempty)


@toolz.curry
def bind(f: Callable[[T], Writer[T]], a: Writer[T]) -> Writer[T]:
    b = f(a.a)
    return a.__class__(b.a, a.w + b.w)


@toolz.curry
def map(f: Callable[[T], T], a: Writer[T]) -> Writer[T]:
    b = f(a.a)
    return a.__class__(b, a.w)


@toolz.curry
def add(f: Callable[[T, T], T], a: Writer[T], b: Writer[T],) -> Writer[T]:
    if a.__class__ is not b.__class__:
        raise ValueError(
            "The arguments `a` and `b` must have same type, but found \n"
            f"\ta {a} : {a.__class__} \n"
            f"\tb {b} : {b.__class__} "
        )
    c = f(a.a, b.a)
    w = a.w + b.w
    return a.__class__(c, w)


def compose(*funcs: Callable[[T], Writer]) -> Callable[[T], Writer[T]]:
    if len(funcs) == 0:
        raise ValueError(f"One or more functions must be passed")
    last = funcs[-1]
    bind_funcs = [bind(f) for f in funcs[:-1]] + [last]
    return toolz.compose(*bind_funcs)

