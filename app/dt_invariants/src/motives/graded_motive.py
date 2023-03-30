from __future__ import annotations

from typing import Callable, Optional

from ..linear_algebra.dimension_vector import DimensionVector
from .types import FractionalMotive


class GradedMotive:
    def __init__(
        self,
        rank: int,
        at_dv: Optional[Callable[[DimensionVector], FractionalMotive]] = None,
        name: Optional[str] = None,
    ) -> None:
        assert rank > 0, "Rank must be positive!"
        self.name: str = name if name else repr(self)
        self.rank = rank
        self.at_dv = at_dv
        self._cache: dict[DimensionVector, FractionalMotive] = {}

    def at(self, d: DimensionVector) -> FractionalMotive:
        assert len(d) == self.rank, f"DimensionVector must have length {self.rank}"
        if self.at_dv:
            return self.at_dv(d)
        else:
            return self._at(d)

    def _at(self, d: DimensionVector) -> FractionalMotive:
        raise NotImplementedError("_at method must be implemented in subclass")

    def __call__(self, d: DimensionVector) -> FractionalMotive:
        try:
            return self._cache[d]
        except KeyError:
            self._cache[d] = self.at(d)
            return self._cache[d]
