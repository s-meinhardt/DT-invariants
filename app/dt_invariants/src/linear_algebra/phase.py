from __future__ import annotations

from cmath import phase
from math import pi


from .immutable import Immutable


class Phase(Immutable):
    __slots__ = ["_real", "_imag", "branch"]

    def __init__(self, value: int = 0) -> None:
        assert isinstance(value, int), "Only integer values are allowed"

        branch, remainder = divmod(value, 2)
        object.__setattr__(self, "_real", (-1) ** remainder)
        object.__setattr__(self, "_imag", 0)
        object.__setattr__(self, "branch", branch)

        super().__init__()

    @classmethod
    def of(cls, z: tuple[int, int], branch: int = 0) -> Phase:
        phase = cls()
        object.__setattr__(phase, "_real", z[0])
        object.__setattr__(phase, "_imag", z[1])
        object.__setattr__(phase, "branch", branch)
        return phase

    def covers(self, z: tuple[int, int]) -> bool:
        return self == Phase.of(z, branch=self.branch)

    @property
    def slope(self) -> float:
        if self._imag:
            return -self._real / self._imag
        else:
            return float("inf")

    @property
    def is_in_upper_half_plane(self) -> bool:
        return self._imag > 0 or self._imag == 0 and self._real > 0

    @property
    def value(self) -> float:
        return float(self)

    def __repr__(self) -> str:
        return f"Phase({float(self)})"

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash((self._real, self._imag, self.branch))

    def __eq__(self, other: Phase) -> bool:  # type: ignore[override]
        return (
            int(self) == int(other) and self._real * other._imag == other._real * self._imag  # both have the same slope
        )

    def __lt__(self, other: Phase) -> bool:
        if int(self) < int(other):
            return True
        elif int(self) > int(other):
            return False
        elif self._imag * other._real - self._real * other._imag < 0:
            return True
        else:
            return False

    def __le__(self, other: Phase) -> bool:
        return self < other or self == other

    def __float__(self) -> float:
        return 2 * (self.branch + (self._imag < 0)) + phase(complex(self._real, self._imag)) / pi

    def __int__(self) -> int:
        if self.is_in_upper_half_plane:
            return 2 * self.branch
        else:
            return 2 * self.branch + 1

    def __bool__(self) -> bool:
        return self.branch != 0 or self._imag != 0 or self._real != 0

    def __add__(self, other: int | Phase) -> Phase:
        if isinstance(other, int):
            other = Phase(other)
        if not isinstance(other, Phase):
            ValueError("The second summand must be a Phase or an integer!")

        real = self._real * other._real - self._imag * other._imag
        imag = self._imag * other._real + self._real * other._imag
        sum_is_in_upper_half_plane = imag > 0 or imag == 0 and real > 0
        if self.is_in_upper_half_plane and other.is_in_upper_half_plane:
            branch: int = self.branch + other.branch
        elif self.is_in_upper_half_plane and not sum_is_in_upper_half_plane:
            branch = self.branch + other.branch
        elif other.is_in_upper_half_plane and not sum_is_in_upper_half_plane:
            branch = self.branch + other.branch
        else:
            branch = self.branch + other.branch + 1
        return Phase.of(z=(real, imag), branch=branch)

    def __radd__(self, other: int) -> Phase:
        return self + other

    def __neg__(self) -> Phase:
        return Phase.of(z=(self._real, -self._imag), branch=-self.branch - 1)

    def __sub__(self, other: int | Phase) -> Phase:
        return self + -other

    def __rsub__(self, other: int) -> Phase:
        return -self + other
