from __future__ import annotations

import math
from typing import TYPE_CHECKING, cast

import sympy

from ..linear_algebra.cone import Cone
from ..linear_algebra.dimension_vector import DimensionVector
from ..linear_algebra.phase import Phase
from .motivic_series import MotivicSeries
from .sliced_motive import SlicedMotive
from .symbols import L
from .types import FractionalMotive

if TYPE_CHECKING:
    from ..stability.stability_condition import StabilityCondition


class MotiveOfSemistables(SlicedMotive):
    def __init__(self, stab_cond: StabilityCondition) -> None:
        self.stab_cond = stab_cond
        self.rank: int = stab_cond.rank
        self.motive_of_all_objects: MotivicSeries = stab_cond.abelian_category.motive_of_objects
        self.cone_of_all_objects: Cone = self.motive_of_all_objects.cone
        super().__init__(
            rank=self.rank,
            name=f"Semistables({self.stab_cond.abelian_category.name}",
            cone_at=self.cone_at,
            phase_of=self.phase_of,
        )

    def cone_at(self, phi: Phase) -> Cone:
        if phi.branch % 2:
            # we take the cone at phase + 1 and shift it back
            return self.cone_at(phi[1])[-1]

        def is_contained(d: DimensionVector) -> bool:
            return self.cone_of_all_objects.contains(d) and phi.covers(self.stab_cond.charge(d))

        def pred_of(d: DimensionVector, upper_bound: DimensionVector) -> DimensionVector:
            e: DimensionVector = self.cone_of_all_objects.pred_of(d, upper_bound)
            while not is_contained(e):
                e = self.cone_of_all_objects.pred_of(e, upper_bound)
            return e

        return Cone(rank=self.rank, is_contained=is_contained, pred_of=pred_of)

    def phase_of(self, d: DimensionVector) -> Phase:
        return self.stab_cond.charge.phase(d)

    def _at(self, d: DimensionVector) -> FractionalMotive:
        result: FractionalMotive = self.motive_of_all_objects(d) - sum(
            L**exponent * math.prod(cast(FractionalMotive, self(e)) for e in part)
            for part, exponent in self.stab_cond.hn_partitions(d)
            if part != {d}
        )
        return sympy.factor(result)
