from typing import Optional
from ..linear_algebra import DimensionVector, ScalarProduct
from ..motives import L, R, GL, FractionalMotive
from ..motivic_series import MotivicSeries, SeriesFromFun


class Quiver:
    def __init__(self, num_vertices: int, arrow_matrix: dict[tuple[int, int], int], name: Optional[str] = None) -> None:
        self.num_vertices = num_vertices
        self.vertices: range = range(num_vertices)
        self.arrow_matrix = arrow_matrix
        self.name = name if name else repr(self)

        self.hom: ScalarProduct = ScalarProduct(dim=num_vertices)  # the standard scalar product
        self.ext: ScalarProduct = ScalarProduct(dim=num_vertices, coeff_matrix=arrow_matrix)

        # Euler pairing
        coeff_matrix = {(source, target): -num_arrows for (source, target), num_arrows in arrow_matrix.items()}
        coeff_matrix.update({(i, i): 1 + coeff_matrix.get((i, i), 0) for i in self.vertices})
        self.chi: ScalarProduct = ScalarProduct(
            dim=num_vertices, coeff_matrix={k: v for k, v in coeff_matrix.items() if v != 0}
        )

    def generating_series(self) -> MotivicSeries:
        def coeff_fn(d: DimensionVector) -> FractionalMotive:
            return R ** self.chi(d, d) * L ** self.ext(d, d) / GL(d)

        return SeriesFromFun(num_vertices=self.num_vertices, coeff_fn=coeff_fn)
