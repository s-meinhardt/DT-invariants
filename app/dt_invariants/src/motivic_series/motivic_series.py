from __future__ import annotations
from typing import Optional
from .series_from_fun import SeriesFromFun
from ..linear_algebra import DimensionVector
from ..motives import FractionalMotive


class MotivicSeries:
    def __init__(self, num_vertices: int, name: Optional[str] = None) -> None:
        self.name = name if name else repr(self)
        self.num_vertices = num_vertices
        self._cache: dict[DimensionVector, FractionalMotive] = {}

    def at(self, d: DimensionVector) -> FractionalMotive:
        assert len(d) == self.num_vertices, f"DimensionVector must have length {self.num_vertices}"
        result = self._cache.get(d)
        if result is None:
            result = self._at(d)
            self._cache[d] = result
        return result

    def _at(self, d: DimensionVector) -> FractionalMotive:
        raise NotImplementedError("_at method must be implemented in subclass")

    def __add__(self, other: MotivicSeries) -> MotivicSeries:
        assert self.num_vertices == other.num_vertices, "both summands must have the same number of vertices"

        def coeff_fn(d: DimensionVector) -> FractionalMotive:
            return self.at(d) + other.at(d)

        return SeriesFromFun(coeff_fn=coeff_fn, num_vertices=self.num_vertices, name=f"{self.name}+{other.name}")

    def __mul__(self, other: MotivicSeries) -> MotivicSeries:
        assert self.num_vertices == other.num_vertices, "both summands must have the same number of vertices"

        def coeff_fn(d: DimensionVector) -> FractionalMotive:
            return sum(self.at(e) * other.at(d - e) for e in d.summands())

        return SeriesFromFun(coeff_fn=coeff_fn, num_vertices=self.num_vertices, name=f"{self.name}*{other.name}")

    def __rmul__(self, other: FractionalMotive) -> MotivicSeries:
        def coeff_fn(d: DimensionVector) -> FractionalMotive:
            return other * self.at(d)

        return SeriesFromFun(coeff_fn=coeff_fn, num_vertices=self.num_vertices, name=f"{other}*{self.name}")
