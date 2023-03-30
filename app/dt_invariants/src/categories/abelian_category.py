from __future__ import annotations

from typing import Optional, cast

from ..linear_algebra.pairing import Pairing
from ..motives.motivic_series import MotivicSeries
from ..motives.symbols import R


class AbelianCategory:
    def __init__(self, motive_of_objects: MotivicSeries, euler_pairing: Pairing, name: Optional[str] = None) -> None:
        assert (
            euler_pairing.rank == motive_of_objects.rank
        ), "The motivic series and the euler pairing must have the same rank"

        self.rank = euler_pairing.rank
        self.euler_pairing = euler_pairing
        self.motive_of_objects = motive_of_objects
        self.name: str = name if name else repr(self)
        self._normalized_motive_of_objects: Optional[MotivicSeries] = None

    def __getitem__(self, shift: int) -> AbelianCategory:
        return AbelianCategory(
            motive_of_objects=self.motive_of_objects[shift],
            euler_pairing=self.euler_pairing,
            name=f"{self.name}[{shift}]",
        )

    @property
    def normalized_motive_of_objects(self) -> MotivicSeries:
        if self._normalized_motive_of_objects:
            return self._normalized_motive_of_objects
        else:
            self.set_normalized_motive_of_objects()
            return cast(MotivicSeries, self._normalized_motive_of_objects)

    def set_normalized_motive_of_objects(self) -> None:
        self._normalized_motive_of_objects = MotivicSeries(
            cone=self.motive_of_objects.cone,
            at_dv=lambda d: R ** self.euler_pairing(d, d) * self.motive_of_objects(d),
            name=f"{self.motive_of_objects.name}_vir",
        )
