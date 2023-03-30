from typing import Optional

from .dimension_vector import DimensionVector
from .phase import Phase


class CentralCharge:
    def __init__(self, real: Optional[list[int]] = None, imag: Optional[list[int]] = None) -> None:
        if isinstance(real, list):
            self.rank: int = len(real)
        elif isinstance(imag, list):
            self.rank = len(imag)
        else:
            raise ValueError("Real or imaginary part must be provided.")
        self.real: list[int] = real if real else self.rank * [0]
        self.imag: list[int] = imag if imag else self.rank * [1]

        self._validate()

    def _validate(self) -> None:
        assert len(self.real) == self.rank, "the real and the imaginary part must have the same length"
        assert len(self.imag) == self.rank, "the real and the imaginary part must have the same length"
        assert all(isinstance(a, int) for a in self.real), "the real part must consist of integers"
        assert all(isinstance(b, int) for b in self.imag), "the imaginary part must consist of integers"

    def _real(self, d: DimensionVector) -> int:
        return sum(a * x for a, x in zip(self.real, d))

    def _imag(self, d: DimensionVector) -> int:
        return sum(a * x for a, x in zip(self.imag, d))

    def __call__(self, d: DimensionVector) -> tuple[int, int]:
        assert len(d) == self.rank, f"dimension vector must have {self.rank} components"
        return (self._real(d), self._imag(d))

    def slope(self, d: DimensionVector) -> float:
        assert len(d) == self.rank, f"dimension vector must have {self.rank} components"
        return -self._real(d) / self._imag(d)

    def phase(self, d: DimensionVector) -> Phase:
        if self._imag(d) > 0 or self._imag(d) == 0 and self._real(d) < 0:
            return Phase(real=self._real(d), imag=self._imag(d), branch=0)
        else:
            return Phase(real=self._real(d), imag=self._imag(d), branch=1)
