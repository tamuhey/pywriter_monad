from dataclasses import dataclass, field
from typing import Dict, TypeVar
from toolz import merge
from .writer import Writer


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

