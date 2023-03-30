from typing import Optional, cast

from ..linear_algebra.phase import Phase
from ..linear_algebra.pairing import Pairing
from ..motives.dt_invariants import DTInvariants
from ..motives.motivic_series import MotivicSeries
from ..motives.sliced_motive import SlicedMotive
from .abelian_category import AbelianCategory


class Slicing:
    def __init__(self, euler_pairing: Pairing, motive_of_objects: SlicedMotive, name: Optional[str] = None) -> None:
        assert (
            euler_pairing.rank == motive_of_objects.rank
        ), "euler pairing and motive of objects must have the same rank"
        self.rank = euler_pairing.rank
        self.euler_pairing = euler_pairing
        self.motive_of_objects = motive_of_objects
        self.name: str = name if name else repr(self)
        self._cache: dict[Phase, AbelianCategory] = {}
        self._dt_invariants: Optional[SlicedMotive] = None

    def __call__(self, phi: Phase) -> AbelianCategory:
        result = self._cache.get(phi)
        if result is None:
            result = AbelianCategory(
                motive_of_objects=cast(MotivicSeries, self.motive_of_objects(phi)),
                euler_pairing=self.euler_pairing,
                name=f"{self.name}({float(phi)})",
            )
            self._cache[phi] = result
        return result

    @property
    def dt_invariants(self) -> SlicedMotive:
        if self._dt_invariants:
            return self._dt_invariants
        else:
            self.set_dt_invariants()
            return cast(SlicedMotive, self._dt_invariants)

    def set_dt_invariants(self) -> None:
        self._dt_invariants = DTInvariants(slicing=self)
