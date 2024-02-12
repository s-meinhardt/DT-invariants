from typing import Optional

from .dimension_vector import DimensionVector


class Pairing:
  def __init__(
    self, rank: int, coeff_matrix: Optional[dict[tuple[int, int], int]] = None
  ) -> None:
    self.rank = rank
    if not coeff_matrix:
      # use unit matrix
      self.coeff_matrix: dict[tuple[int, int], int] = {(i, i): 1 for i in range(rank)}
    else:
      self.coeff_matrix = coeff_matrix

    self._validate()

  def __call__(self, d: DimensionVector, e: DimensionVector) -> int:
    assert len(d) == self.rank, f"DimensionVector must have length {self.rank}"
    assert len(e) == self.rank, f"DimensionVector must have length {self.rank}"
    return sum(d[i] * e[j] * coeff for (i, j), coeff in self.coeff_matrix.items())

  def _validate(self) -> None:
    if not isinstance(self.rank, int) or self.rank < 0:
      raise ValueError("The rank must be a positive integer.")
    if not isinstance(self.coeff_matrix, dict):
      raise ValueError("The coeff_matrix must be of type dict[tuple[int, int], int].")
    for key, value in self.coeff_matrix.items():
      if not isinstance(key, tuple) or len(key) != 2:
        raise ValueError(
          "The keys of the coeff_matrix must be a tuple of two integers."
        )
      if key[0] not in range(self.rank) and key[1] not in range(self.rank):
        raise ValueError(
          f"The indices of the coeff_matrix be called 0,...,{self.rank-1}."
        )
      if not isinstance(value, int):
        raise ValueError("The elements of the coeff_matrix must be integers.")
