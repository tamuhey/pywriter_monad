import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, TypeVar

T = TypeVar("T", covariant=True)
W = TypeVar("W")


def add_inner(x: W, y: W) -> W:
    if isinstance(x, dict):
        # https://github.com/microsoft/pyright/issues/1388
        return {**x, **y}  # type: ignore
    if hasattr(x, "__add__"):
        return x + y  # type: ignore
    raise TypeError(f"Unsupported type: {type(x)}, {type(y)}")


@dataclass
class Writer(Generic[T, W]):
    """Writer Monad"""

    a: T
    w: W


# TODO: https://github.com/microsoft/pyright/issues/1384
def bind(f: Callable[[T], Writer[T, W]],) -> Callable[[Writer[T, W]], Writer[T, W]]:
    def fn(a: Writer[T, W]) -> Writer[T, W]:
        b = f(a.a)
        return a.__class__(b.a, add_inner(a.w, b.w))

    return fn


def map(f: Callable[[T], T]) -> Callable[[Writer[T, W]], Writer[T, W]]:
    def fn(a: Writer[T, W]) -> Writer[T, W]:
        b = f(a.a)
        return a.__class__(b, a.w)

    return fn


def add(
    f: Callable[[T, T], T],
) -> Callable[[Writer[T, W], Writer[T, W]], Writer[T, W]]:
    def fn(a: Writer[T, W], b: Writer[T, W]):
        if a.__class__ is not b.__class__:
            raise ValueError(
                "The arguments `a` and `b` must have same type, but found \n"
                f"\ta {a} : {a.__class__} \n"
                f"\tb {b} : {b.__class__} "
            )
        c = f(a.a, b.a)
        w = add_inner(a.w, b.w)
        return a.__class__(c, w)

    return fn


def compose(*funcs: Callable[[T], Writer[T, W]]) -> Callable[[T], Writer[T, W]]:
    if len(funcs) == 0:
        raise ValueError(f"One or more functions must be passed")

    last = funcs[-1]
    funcs = funcs[:-1]

    def f(a: T) -> Writer[T, W]:
        m = last(a)
        for fn in funcs[::-1]:
            m = bind(fn)(m)
        return m

    return f
