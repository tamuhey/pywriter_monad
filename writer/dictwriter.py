from dataclasses import dataclass, field
from typing import Dict, Generic, Iterable, Mapping, Tuple, TypeVar, Union, overload
from toolz import merge
from .writer import Writer


T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")
K_ = TypeVar("K_")
V_ = TypeVar("V_")


class DictM(Dict[K, V]):
    def __add__(
        self, other: Union[Dict[K, V], "DictM[K_,V_]"]
    ) -> "DictM[Union[K,K],Union[V,V_]]":
        return self.__class__(merge(self, other))

    @classmethod
    def mempty(cls) -> "DictM[K,V]":
        return cls()


@dataclass
class DictWriter(Writer[T], Generic[T, K, V]):
    """Like the writer monad, it holds a writer `w` as a dict. Useful for logging."""

    a: T
    # TODO https://stackoverflow.com/questions/62753881/how-to-annotate-the-type-of-field-in-dataclass-to-be-different-from-the-type-of
    w: DictM[K, V] = field(default_factory=DictM)  # type: ignore

    def __init__(self, a: T, w: Union[Iterable[Tuple[K, V]], Mapping[K, V]]) -> None:
        self.a = a
        self.w = DictM(w)

