from dataclasses import dataclass, field
from typing import Dict, Generic, Iterable, Mapping, Tuple, TypeVar, Union, overload

from .writer import Writer

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
K_ = TypeVar("K_")
V_ = TypeVar("V_")


class DictM(Dict[K, V]):
    def __add__(self, other: "DictM[K,V]") -> "DictM[K,V]":
        return self.__class__({**self, **other})

    @classmethod
    def mempty(cls) -> "DictM[K,V]":
        return cls()


@dataclass
class DictWriter(Writer[T], Generic[T, K, V]):
    """Like the writer monad, it holds a writer `w` as a dict. Useful for logging."""

    a: T
    w: DictM[K, V] = field(default_factory=DictM)

    @overload
    def __init__(self, a: T, w: Mapping[K, V]) -> None:
        ...

    @overload
    def __init__(self, a: T, w: Iterable[Tuple[K, V]]) -> None:
        ...

    def __init__(self, a: T, w) -> None:
        self.a = a
        self.w = DictM(w)
