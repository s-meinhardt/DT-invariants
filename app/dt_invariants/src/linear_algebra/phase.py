from __future__ import annotations

from cmath import phase
from dataclasses import dataclass
from math import pi


@dataclass(init=True, frozen=True)
class Phase:
    """A phase represents a float phi satisfying
    defined via z = |z| * exp(i * pi * phi)
    for z = real + i * imag.
    The 'branch' is related to the winding number
    via winding number == branch // 2.
    """

    real: int
    imag: int
    branch: int

    def __post_init__(self) -> None:
        # validate input
        if self.branch % 2:
            assert self.imag < 0 or self.real > 0
        else:
            assert self.imag > 0 or self.real < 0

    def slope(self) -> float:
        if self.imag:
            return -self.real / self.imag
        else:
            return float("inf")

    def __eq__(self, other: Phase) -> bool:  # type: ignore[override]
        "'self' and 'other' have the same branch and slope"
        return self.branch == other.branch and self.real * other.imag == other.real * self.imag

    def __lt__(self, other: Phase) -> bool:
        if self.branch < other.branch:
            return True
        elif self.branch > other.branch:
            return False
        else:
            return self.slope() < other.slope()

    def covers(self, z: tuple[int, int]) -> bool:
        """Checks if the complex number z[0] + i * z[1] has phase 'self' modulo 2

        Args:
            z (tuple[int, int]): a pair representing the real and imaginary part of a complex number

        Returns:
            bool: Has the complex number z[0] + i * z[1] phase 'self' modulo 2?
        """
        real, imag = z
        if real or imag:
            return self.real * imag == real * self.imag
        else:
            return True

    def __float__(self):
        return self.branch + phase((-1) ** self.branch * complex(self.real, self.imag)) / pi

    def __int__(self):
        return self.branch if self.imag != 0 else self.branch + 1

    def __getitem__(self, shift: int) -> Phase:
        if shift % 2 == 0:
            return Phase(real=self.real, imag=self.imag, branch=self.branch + shift)
        else:
            return Phase(real=-self.real, imag=-self.imag, branch=self.branch + shift)
