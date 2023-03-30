from typing import Optional

from .cone import Cone
from .dimension_vector import DimensionVector


class StandardCone(Cone):
    def __init__(self, rank: int, name: Optional[str] = None) -> None:
        def is_contained(d: DimensionVector) -> bool:
            if len(d) != rank:
                return False
            if min(d) < 0:
                return False
            return True

        def pred_of(d: DimensionVector, upper_bound: DimensionVector) -> DimensionVector:
            """
            returns the maximum of the finite set { e | e < d and e <<= upper_bound } with respect to <
            """
            assert not d.is_zero(), "Cannot make zero vector smaller"
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
                    return DimensionVector(*predecessor)
                else:
                    predecessor[idx] = upper_bound[idx]
                idx -= 1

        super().__init__(rank=rank, is_contained=is_contained, pred_of=pred_of, name=name)
