from dataclasses import dataclass, field
from typing import Dict, Generic, TypeVar, Union
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

    def __post_init__(self):
        if not isinstance(self.w, dict):  # type: ignore
            raise ValueError(
                f"expected `self.w` be `dict` type, but found {self.w} (type: {type(self.w)}"
            )
        self.w = DictM(self.w)

