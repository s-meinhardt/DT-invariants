from __future__ import annotations

from collections.abc import Iterable, Sequence
from .immutable import Immutable


class DimensionVector(Immutable, Sequence):
    # __slots__ = ["_coord"]

    def __init__(self, *args) -> None:
        if isinstance(args[0], Iterable):
            object.__setattr__(self, "_coord", tuple(args[0]))
        else:
            object.__setattr__(self, "_coord", tuple(args))
        assert all(map(lambda x: isinstance(x, int), self._coord)), "Coordinates must be integers!"
        super().__init__()

    @classmethod
    def zero(cls, length: int) -> DimensionVector:
        return DimensionVector(0 for _ in range(length))

    @property
    def is_zero(self) -> bool:
        return all(map(lambda x: x == 0, self))

    def copy(self) -> DimensionVector:

        return DimensionVector(x for x in self)

    def __len__(self) -> int:
        return len(self._coord)

    def __getitem__(self, position: int) -> int:
        return self._coord[position]

    def __add__(self, other: DimensionVector) -> DimensionVector:
        assert len(self) == len(other), "Both dimension vectors must have the same length!"
        return DimensionVector(map(lambda x: x[0] + x[1], zip(self, other)))

    def __iadd__(self, other: DimensionVector) -> DimensionVector:
        return self + other

    def __neg__(self) -> DimensionVector:
        return DimensionVector(-x for x in self)

    def __sub__(self, other: DimensionVector) -> DimensionVector:
        return self + -other

    def __isub__(self, other: DimensionVector) -> DimensionVector:
        return self - other

    def __mul__(self, factor: int) -> DimensionVector:
        return DimensionVector(map(lambda x: factor * x, self))

    def __rmul__(self, factor: int) -> DimensionVector:
        return self * factor

    def __imul__(self, factor: int) -> DimensionVector:
        return self * factor

    def __truediv__(self, divisor: int) -> DimensionVector:
        return DimensionVector(map(lambda x: x // divisor, self))

    def __floordiv__(self, other: DimensionVector) -> int:
        assert len(self) == len(other), "Both dimension vectors must have the same length!"
        assert not other.is_zero, "Cannot divide by zero vector!"
        eligible_pairs = filter(lambda x: x[1] != 0, zip(self, other))
        quotients = map(lambda x: x[0] // x[1], eligible_pairs)
        return min(quotients)

    def __mod__(self, other: DimensionVector) -> DimensionVector:
        return self - other * (self // other)

    def __divmod__(self, other: DimensionVector) -> tuple[int, DimensionVector]:
        """
        returns the pair (self // other, self % other)
        """
        quotient = self // other
        return quotient, self - quotient * other

    def __repr__(self) -> str:
        return repr(tuple(self))

    def __lshift__(self, other: DimensionVector) -> bool:
        """
        implements the partial order relation << meaning that all coordinates
        are <= and both vectors do not coincide

        Note: d << e implies d < e
        """
        assert len(self) == len(other), "Both dimension vectors must have the same length!"
        return all(map(lambda x: x[0] <= x[1], zip(self, other))) and self != other

    def __rshift__(self, other: DimensionVector) -> bool:
        """
        implements the partial order relation >> meaning that all coordinates
        are >= and both vectors do not coincide

        Note: d >> e implies d > e
        """
        assert len(self) == len(other), "Both dimension vectors must have the same length!"
        return all(map(lambda x: x[0] >= x[1], zip(self, other))) and self != other

    def __eq__(self, other: DimensionVector) -> bool:
        assert len(self) == len(other), "Both dimension vectors must have the same length!"
        return all(map(lambda x: x[0] == x[1], zip(self, other)))

    def __lt__(self, other: DimensionVector) -> bool:
        assert len(self) == len(other), "Both dimension vectors must have the same length!"
        for x, y in zip(self, other):
            if x == y:
                continue
            return x < y

    def __le__(self, other: DimensionVector) -> bool:
        return self < other or self == other
