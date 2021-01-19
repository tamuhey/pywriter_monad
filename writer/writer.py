import sys
from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


T = TypeVar("T")

M = TypeVar("M", bound="Monoid")


class Monoid(Protocol[M]):
    def __add__(self: M, other: M) -> M:
        ...

    @classmethod
    def mempty(cls) -> M:
        ...


@dataclass
class Writer(Generic[T]):
    """Writer Monad"""

    a: T
    w: Monoid = field(default_factory=Monoid.mempty)


R = TypeVar("R", bound=Writer)


def bind(
    f: Callable[[T], R[T]],
) -> Callable[[R[T]], R[T]]:
    def fn(a: R[T]) -> R[T]:
        b = f(a.a)
        return a.__class__(b.a, a.w + b.w)

    return fn


def map(f: Callable[[T], T]) -> Callable[[Writer[T]], Writer[T]]:
    def fn(a: Writer[T]):
        b = f(a.a)
        return a.__class__(b, a.w)

    return fn


def add(
    f: Callable[[T, T], T],
) -> Callable[[Writer[T], Writer[T]], Writer[T]]:
    def fn(a: Writer[T], b: Writer[T]):
        if a.__class__ is not b.__class__:
            raise ValueError(
                "The arguments `a` and `b` must have same type, but found \n"
                f"\ta {a} : {a.__class__} \n"
                f"\tb {b} : {b.__class__} "
            )
        c = f(a.a, b.a)
        w = a.w + b.w
        return a.__class__(c, w)

    return fn


def compose(*funcs: Callable[[T], R[T]]) -> Callable[[T], R[T]]:
    if len(funcs) == 0:
        raise ValueError(f"One or more functions must be passed")

    last = funcs[-1]
    funcs = funcs[:-1]

    def f(a: T) -> R:
        m = last(a)
        for fn in funcs[::-1]:
            fn = bind(fn)
            m = fn(m)
        return m

    return f
