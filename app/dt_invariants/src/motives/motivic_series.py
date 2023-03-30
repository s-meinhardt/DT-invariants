from __future__ import annotations

from typing import Callable, Optional

import sympy

from ..linear_algebra.cone import Cone
from ..linear_algebra.dimension_vector import DimensionVector
from .graded_motive import GradedMotive
from .types import FractionalMotive


class MotivicSeries(GradedMotive):
    def __init__(
        self,
        cone: Cone,
        at_dv: Optional[Callable[[DimensionVector], FractionalMotive]] = None,
        name: Optional[str] = None,
    ) -> None:
        self.cone = cone
        super().__init__(rank=cone.rank, at_dv=at_dv, name=name)

    def at(self, d: DimensionVector) -> FractionalMotive:
        if not self.cone.contains(d):
            return sympy.Integer(0)
        return super().at(d)

    def __getitem__(self, shift: int) -> MotivicSeries:
        return MotivicSeries(
            cone=self.cone[shift], at_dv=lambda d: self((-1) ** shift * d), name=f"{self.name}[{shift}]"
        )

    def below(self, d: DimensionVector, expand: bool = False, factorize: bool = False) -> FractionalMotive:
        assert not expand or not factorize, "you cannot factorize and expand at the same time"

        def format(m: FractionalMotive) -> FractionalMotive:
            if expand:
                return sympy.expand(m)
            elif factorize:
                return sympy.factor(m)
            else:
                return m

        x = sympy.Symbol("x")
        return sum(format(self(e)) * (x ** sympy.Symbol(str(e))) for e in self.cone.summands(d))
