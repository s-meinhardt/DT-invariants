from typing import Callable, Optional
from .motivic_series import MotivicSeries
from ..linear_algebra import DimensionVector
from ..motives import FractionalMotive


class SeriesFromFun(MotivicSeries):
    def __init__(
        self, coeff_fn: Callable[[DimensionVector], FractionalMotive], num_vertices: int, name: Optional[str] = None
    ) -> None:
        super().__init__(num_vertices=num_vertices, name=name)
        self.coeff_fn = coeff_fn

    def _at(self, d: DimensionVector) -> FractionalMotive:
        return self.coeff_fn(d)
