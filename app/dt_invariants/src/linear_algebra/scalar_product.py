from typing import Optional
from .dimension_vector import DimensionVector


class ScalarProduct:
    def __init__(self, dim: int, coeff_matrix: Optional[dict[tuple[int, int], int]] = None) -> None:
        self.dimension = dim
        if not coeff_matrix:
            # use unit matrix
            self.coeff_matrix: dict[tuple[int, int], int] = {(i, i): 1 for i in range(dim)}
        else:
            self.coeff_matrix = coeff_matrix

    def __call__(self, d: DimensionVector, e: DimensionVector) -> int:
        assert len(d) == self.dimension, f"DimensionVector must have length {self.dimension}"
        assert len(e) == self.dimension, f"DimensionVector must have length {self.dimension}"
        return sum(d[i] * e[j] * coeff for (i, j), coeff in self.coeff_matrix.items())
