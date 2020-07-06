from dataclasses import dataclass, field
from typing import Callable, Generic, Protocol, TypeVar, runtime_checkable
from toolz import curry
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


@curry
def bind(f: Callable[[T], Writer[T]], a: Writer[T]) -> Writer[T]:
    b = f(a.a)
    return a.__class__(b.a, a.w + b.w)


@curry
def map(f: Callable[[T], T], a: Writer[T]) -> Writer[T]:
    b = f(a.a)
    return a.__class__(b, a.w)

