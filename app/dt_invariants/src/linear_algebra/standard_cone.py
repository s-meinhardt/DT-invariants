from typing import Optional

from .cone import Cone
from .dimension_vector import DimensionVector
from collections.abc import Iterator


class StandardCone(Cone):
    def __init__(self, rank: int, name: Optional[str] = None) -> None:
        self.rank = rank
        self.name = name if name else repr(self)

    def _pred_of(self, d: DimensionVector, upper_bound: DimensionVector) -> DimensionVector:
        assert not d.is_zero, "Cannot make zero vector smaller"
        assert d in self, "The dimension vector must be conained in the cone!"
        predecessor: list = list(d)
        for idx, x in enumerate(d):
            if upper_bound[idx] < x:
                predecessor[idx:] = upper_bound[idx:]
                return DimensionVector(*predecessor)
        # at this point we have returned or self <<= upper_bound
        idx = -1
        while True:
            if d[idx] > 0:
                predecessor[idx] -= 1
                return DimensionVector(predecessor)
            else:
                predecessor[idx] = upper_bound[idx]
            idx -= 1

    def __contains__(self, d: DimensionVector) -> bool:
        assert self.rank == len(d), f"The dimension vector must have length {self.rank}!"
        return all(x >= 0 for x in d)

    def summands(self, d: DimensionVector) -> Iterator[DimensionVector]:
        assert self.rank == len(d), f"The dimension vector must have length {self.rank}!"
        assert d in self, "The dimension vector must be conained in the cone!"
        e = d.copy()
        while e in self:
            yield e
            if e.is_zero:
                return
            else:
                e = self._pred_of(e, upper_bound=d)
