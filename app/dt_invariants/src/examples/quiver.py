from typing import Optional, cast

from ..categories.abelian_category import AbelianCategory
from ..linear_algebra.pairing import Pairing
from ..linear_algebra.standard_cone import StandardCone
from ..motives.gl import GL
from ..motives.motivic_series import MotivicSeries
from ..motives.symbols import L


class Quiver:
  def __init__(
    self,
    num_vertices: int,
    arrow_matrix: dict[tuple[int, int], int],
    name: Optional[str] = None,
  ) -> None:
    self.num_vertices = num_vertices
    self.vertices: range = range(num_vertices)
    self.arrow_matrix = arrow_matrix
    self.name = name if name else repr(self)
    self._reps: Optional[AbelianCategory] = None

    self._validate()

    self.hom: Pairing = Pairing(rank=num_vertices)  # the standard scalar product
    self.ext: Pairing = Pairing(rank=num_vertices, coeff_matrix=arrow_matrix)

    # Euler pairing
    coeff_matrix: dict[tuple[int, int], int] = {
      (source, target): -num_arrows
      for (source, target), num_arrows in arrow_matrix.items()
    }
    coeff_matrix.update(
      {(i, i): 1 + coeff_matrix.get((i, i), 0) for i in self.vertices}
    )
    self.euler_pairing: Pairing = Pairing(
      rank=num_vertices, coeff_matrix={k: v for k, v in coeff_matrix.items() if v != 0}
    )

  @property
  def reps(self) -> AbelianCategory:
    if self._reps:
      return self._reps
    else:
      self._set_quiver_reps()
      return cast(AbelianCategory, self._reps)

  def _set_quiver_reps(self) -> None:
    motive_of_objects: MotivicSeries = MotivicSeries(
      cone=StandardCone(rank=self.num_vertices),
      at_dv=lambda d: L ** self.ext(d, d) / GL(d),
      name=f"Generating Series({self.name})",
    )

    self._reps = AbelianCategory(
      motive_of_objects=motive_of_objects,
      euler_pairing=self.euler_pairing,
      name=f"{self.name}-Reps",
    )

  def _validate(self) -> None:
    if not isinstance(self.num_vertices, int) or self.num_vertices < 1:
      raise ValueError("The number over vertices must be a positive integer.")
    if not isinstance(self.arrow_matrix, dict):
      raise ValueError("The arrow_matrix must be of type dict[tuple[int, int], int].")
    for key, value in self.arrow_matrix.items():
      if not isinstance(key, tuple) or len(key) != 2:
        raise ValueError(
          "The keys of the arrow_matrix must be a tuple of two integers."
        )
      if key[0] not in self.vertices and key[1] not in self.vertices:
        raise ValueError(
          f"The vertices of the quiver must be called 0,...,{self.num_vertices-1}."
        )
      if not isinstance(value, int) or value < 0:
        raise ValueError(
          "The number of arrows between two vertices must be non-negative integer."
        )
    if not isinstance(self.name, str):
      raise ValueError("The name of the quiver must be a string.")
