from typing import Generator, Optional, cast

from ..categories.abelian_category import AbelianCategory
from ..categories.slicing import Slicing
from ..linear_algebra.central_charge import CentralCharge
from ..linear_algebra.cone import Cone
from ..linear_algebra.dimension_vector import DimensionVector
from ..linear_algebra.pairing import Pairing
from ..motives.motive_of_semistables import MotiveOfSemistables
from ..motives.motivic_series import MotivicSeries


class StabilityCondition:
    def __init__(self, abelian_category: AbelianCategory, charge: Optional[CentralCharge] = None) -> None:
        self.rank: int = abelian_category.rank
        self.abelian_category = abelian_category
        self.charge: CentralCharge = charge if charge else CentralCharge(real=self.rank * [0], imag=self.rank * [1])

        self.pairing: Pairing = abelian_category.euler_pairing
        self.motive_of_all_objects: MotivicSeries = abelian_category.motive_of_objects
        self.cone: Cone = self.motive_of_all_objects.cone
        self._semistables: Optional[Slicing] = None

        assert self.charge.rank == self.rank, "abelian_category and central charge must have the same rank"

    def collinear(self, d: DimensionVector, e: DimensionVector) -> bool:
        assert len(d) == self.rank, f"first dimension vector must have length {self.rank}"
        assert len(e) == self.rank, f"second dimension vector must have length {self.rank}"
        return self.charge.phase(d) == self.charge.phase(e)

    def hn_partitions(
        self, d: DimensionVector, k: Optional[DimensionVector] = None
    ) -> Generator[tuple[set, int], None, None]:
        assert len(d) == self.rank, f"dimension vector must have {self.rank} components"
        assert self.cone.contains(d), "dimension vector must be contained in abelian category"
        if k:
            assert len(k) == self.rank, f"upper bound dimension vector must have {self.rank} components"
        else:
            k = 2 * d
        if k.is_zero():
            return
        e: DimensionVector = self.cone.pred_of(k, d)
        if e.is_zero():
            return
        r: DimensionVector = d - e
        i: int = 0
        while i < 10_000:
            if r.is_zero():
                yield {e}, 0
            else:
                for part, exponent in self.hn_partitions(r, e):
                    if not any(self.collinear(e, p) for p in part):
                        exponent -= sum(
                            self.pairing(p, e) if self.charge.phase(e) < self.charge.phase(p) else self.pairing(e, p)
                            for p in part
                        )
                        part.add(e)
                        yield part, exponent
            e = self.cone.pred_of(e, d)
            r = d - e
            if e.is_zero():
                return
            i += 1

    @property
    def semistables(self) -> Slicing:
        if self._semistables:
            return self._semistables
        else:
            self.set_semistables()
            return cast(Slicing, self._semistables)

    def set_semistables(self) -> None:
        self._semistables = Slicing(
            motive_of_objects=MotiveOfSemistables(self),
            euler_pairing=self.abelian_category.euler_pairing,
            name=f"{self.abelian_category.name}_ss",
        )
