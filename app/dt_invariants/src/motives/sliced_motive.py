from typing import Callable, Optional, Union, cast

from ..linear_algebra.cone import Cone
from ..linear_algebra.dimension_vector import DimensionVector
from ..linear_algebra.phase import Phase
from .graded_motive import GradedMotive
from .motivic_series import MotivicSeries
from .types import FractionalMotive

VectorOrPhase = Union[DimensionVector, Phase]
MotiveOrSeries = Union[FractionalMotive, MotivicSeries]


class SlicedMotive(GradedMotive):
    def __init__(
        self,
        rank: int,
        name: Optional[str] = None,
        cone_at: Optional[Callable[[Phase], Cone]] = None,
        phase_of: Optional[Callable[[DimensionVector], Phase]] = None,
    ) -> None:
        self._cone_at = cone_at
        self._phase_of = phase_of
        super().__init__(rank=rank, name=name)
        self._cache: dict[VectorOrPhase, MotiveOrSeries] = {}  # type: ignore[assignment]

    def __call__(self, arg: VectorOrPhase) -> MotiveOrSeries:  # type: ignore[override]
        try:
            return self._cache[arg]
        except KeyError:
            if isinstance(arg, DimensionVector):
                self._cache[arg] = self.at(arg)
            elif isinstance(arg, Phase):
                self._cache[arg] = self.of(arg)
            else:
                raise ValueError("arg must be a dimension vector or a phase")
            return self._cache[arg]

    def of(self, phi: Phase) -> MotivicSeries:
        try:
            result: MotivicSeries = self._of(phi)
        except NotImplementedError:
            result = MotivicSeries(
                cone=cast(Callable[[Phase], Cone], self._cone_at)(phi),
                at_dv=lambda d: self.at(d),
                name=f"{self.name}({float(phi)})",
            )
        self._cache[phi] = result
        return result

    def at(self, d: DimensionVector) -> FractionalMotive:
        try:
            result: FractionalMotive = super().at(d)
        except NotImplementedError:
            phi: Phase = cast(Callable[[DimensionVector], Phase], self._phase_of)(d)
            result = cast(MotivicSeries, self(phi))(d)
        self._cache[d] = result
        return result

    def _of(self, phi: Phase) -> MotivicSeries:
        raise NotImplementedError("_of method must be implemented in subclass")
