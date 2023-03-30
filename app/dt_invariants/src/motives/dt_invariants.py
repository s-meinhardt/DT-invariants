from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import sympy

from ..linear_algebra.dimension_vector import DimensionVector
from ..linear_algebra.phase import Phase
from ..linear_algebra.pairing import Pairing
from .log import Log
from .motivic_series import MotivicSeries
from .sliced_motive import SlicedMotive
from .symbols import L, R
from .types import FractionalMotive

if TYPE_CHECKING:
    from ..categories.slicing import Slicing


class DTInvariants(SlicedMotive):
    def __init__(self, slicing: Slicing, name: Optional[str] = None) -> None:
        self.slicing = slicing
        self.euler_pairing: Pairing = slicing.euler_pairing
        super().__init__(
            rank=slicing.rank,
            name=name if name else f"DT({slicing.name})",
            phase_of=slicing.motive_of_objects._phase_of,
            cone_at=slicing.motive_of_objects._cone_at,
        )
        self._log_cache: dict[Phase, MotivicSeries] = {}

    def _of(self, phi: Phase) -> MotivicSeries:
        try:
            return self._log_cache[phi]
        except KeyError:
            log: MotivicSeries = Log(self.slicing(phi).normalized_motive_of_objects)
            self._log_cache[phi] = log
            return MotivicSeries(cone=log.cone, at_dv=lambda d: (L - 1) / R * log(d), name=f"{(L-1)/R} * {log.name}")

    def at(self, d: DimensionVector) -> FractionalMotive:
        return R ** (-self.vdim(d)) * sympy.expand(sympy.factor(R ** self.vdim(d) * super().at(d)))

    def vdim(self, d: DimensionVector) -> int:
        return 1 - self.euler_pairing(d, d)
