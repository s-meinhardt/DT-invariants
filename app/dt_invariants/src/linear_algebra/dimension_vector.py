from __future__ import annotations

from collections.abc import Iterable


class DimensionVector(tuple):
    def __new__(cls, *args) -> DimensionVector:
        if isinstance(args[0], Iterable):
            vector = super(DimensionVector, cls).__new__(cls, args[0])
        else:
            vector = super(DimensionVector, cls).__new__(cls, args)
        return vector

    @classmethod
    def zero(cls, num_vertices: int) -> DimensionVector:
        return DimensionVector(0 for _ in range(num_vertices))

    def __add__(self, other: DimensionVector) -> DimensionVector:  # type: ignore[override]
        return DimensionVector(map(lambda x: x[0] + x[1], zip(self, other)))

    def __iadd__(self, other: DimensionVector) -> DimensionVector:  # type: ignore[override]
        # for idx, x in enumerate(other):
        #   self[idx] +=x
        return self + other

    def __sub__(self, other: DimensionVector) -> DimensionVector:
        return DimensionVector(map(lambda x: x[0] - x[1], zip(self, other)))

    def __neg__(self) -> DimensionVector:
        return DimensionVector(-x for x in self)

    def __mul__(self, factor: int) -> DimensionVector:  # type: ignore[override]
        return DimensionVector(map(lambda x: factor * x, self))

    def __rmul__(self, factor: int) -> DimensionVector:  # type: ignore[override]
        return self * factor

    def __truediv__(self, divisor: int) -> DimensionVector:
        return DimensionVector(map(lambda x: x // divisor, self))

    def __floordiv__(self, other: DimensionVector) -> int:
        assert not other.is_zero(), "Cannot divide by zero vector!"
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
        return f"d({','.join(map(lambda x: str(x), self))})"

    def copy(self) -> DimensionVector:
        return DimensionVector((x for x in self))

    def is_zero(self) -> bool:
        return all(map(lambda x: x == 0, self))

    def __lshift__(self, other: DimensionVector) -> bool:
        """
        implements the partial order relation << meaning that all coordinates
        are <= and both vectors do not coincide

        Note: d << e implies d < e
        """
        return all(map(lambda x: x[0] <= x[1], zip(self, other))) and self != other

    def __rshift__(self, other: DimensionVector) -> bool:
        """
        implements the partial order relation >> meaning that all coordinates
        are >= and both vectors do not coincide

        Note: d >> e implies d > e
        """
        return all(map(lambda x: x[0] >= x[1], zip(self, other))) and self != other
