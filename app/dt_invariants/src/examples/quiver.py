from typing import Optional, cast

from ..categories.abelian_category import AbelianCategory
from ..linear_algebra.pairing import Pairing
from ..linear_algebra.standard_cone import StandardCone
from ..motives.gl import GL
from ..motives.motivic_series import MotivicSeries
from ..motives.symbols import L


class Quiver:
    def __init__(self, num_vertices: int, arrow_matrix: dict[tuple[int, int], int], name: Optional[str] = None) -> None:
        self.num_vertices = num_vertices
        self.vertices: range = range(num_vertices)
        self.arrow_matrix = arrow_matrix
        self.name = name if name else repr(self)
        self._reps: Optional[AbelianCategory] = None

        self.hom: Pairing = Pairing(rank=num_vertices)  # the standard scalar product
        self.ext: Pairing = Pairing(rank=num_vertices, coeff_matrix=arrow_matrix)

        # Euler pairing
        coeff_matrix: dict[tuple[int, int], int] = {
            (source, target): -num_arrows for (source, target), num_arrows in arrow_matrix.items()
        }
        coeff_matrix.update({(i, i): 1 + coeff_matrix.get((i, i), 0) for i in self.vertices})
        self.euler_pairing: Pairing = Pairing(
            rank=num_vertices, coeff_matrix={k: v for k, v in coeff_matrix.items() if v != 0}
        )

    @property
    def reps(self) -> AbelianCategory:
        if self._reps:
            return self._reps
        else:
            self.set_quiver_reps()
            return cast(AbelianCategory, self._reps)

    def set_quiver_reps(self) -> None:
        motive_of_objects: MotivicSeries = MotivicSeries(
            cone=StandardCone(rank=self.num_vertices),
            at_dv=lambda d: L ** self.ext(d, d) / GL(d),
            name=f"Generating Series({self.name})",
        )

        self._reps = AbelianCategory(
            motive_of_objects=motive_of_objects, euler_pairing=self.euler_pairing, name=f"{self.name}-Reps"
        )


# antisymmetrized Euler pairing of quiver reps
# chi_matrix = quiver.chi.coeff_matrix
# matrix = {(i, j): v - chi_matrix.get((j, i), 0) for (i, j), v in chi_matrix.items()}
# matrix_tr = {(j, i): chi_matrix.get((j, i), 0) - v for (i, j), v in chi_matrix.items()}
# euler_pairing = Pairing(rank=quiver.num_vertices, coeff_matrix={**matrix, **matrix_tr})
