from typing import Optional

from .dimension_vector import DimensionVector


class Pairing:
    def __init__(self, rank: int, coeff_matrix: Optional[dict[tuple[int, int], int]] = None) -> None:
        self.rank = rank
        if not coeff_matrix:
            # use unit matrix
            self.coeff_matrix: dict[tuple[int, int], int] = {(i, i): 1 for i in range(rank)}
        else:
            self.coeff_matrix = coeff_matrix

    def __call__(self, d: DimensionVector, e: DimensionVector) -> int:
        assert len(d) == self.rank, f"DimensionVector must have length {self.rank}"
        assert len(e) == self.rank, f"DimensionVector must have length {self.rank}"
        return sum(d[i] * e[j] * coeff for (i, j), coeff in self.coeff_matrix.items())
