from __future__ import annotations
from typing import Optional, Generator
from collections.abc import Iterable


class DimensionVector(tuple):
    def __new__(cls, *args) -> DimensionVector:
        if isinstance(args[0], Iterable):
            vector = super(DimensionVector, cls).__new__(cls, args[0])
        else:
            vector = super(DimensionVector, cls).__new__(cls, args)
        assert all(
            map(lambda x: isinstance(x, int) and x >= 0, vector)
        ), f"Coordinates of {vector} must be non-negative integers!"
        return vector

    @classmethod
    def zero(cls, num_vertices: int) -> DimensionVector:
        return DimensionVector(0 for _ in range(num_vertices))

    def __add__(self, other: DimensionVector) -> DimensionVector:
        return DimensionVector(map(lambda x: x[0] + x[1], zip(self, other)))

    def __iadd__(self, other: DimensionVector) -> DimensionVector:
        # for idx, x in enumerate(other):
        #   self[idx] +=x
        return self + other

    def __sub__(self, other: DimensionVector) -> DimensionVector:
        return DimensionVector(map(lambda x: x[0] - x[1], zip(self, other)))

    def __mul__(self, factor: int) -> DimensionVector:
        return DimensionVector(map(lambda x: factor * x, self))

    def __rmul__(self, factor: int) -> DimensionVector:
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

    def pred(self, upper_bound: DimensionVector) -> DimensionVector:
        """
        returns the maximum of the finite set { d | d < self and d <<= upper_bound } with respect to <
        """
        assert not self.is_zero(), "Cannot make zero vector smaller"
        predecessor = list(self)
        for idx, x in enumerate(self):
            if upper_bound[idx] < x:
                predecessor[idx:] = upper_bound[idx:]
                return DimensionVector(*predecessor)
        # at this point we have returned or self <<= upper_bound
        idx = -1
        while True:
            if self[idx] > 0:
                predecessor[idx] -= 1
                return DimensionVector(*predecessor)
            else:
                predecessor[idx] = upper_bound[idx]
            idx -= 1

    def succ(self, upper_bound: Optional[DimensionVector] = None) -> DimensionVector:
        """
        returns the minimum of the set { d | self < d and (optional) d << upper_bound } with respect to <
        """
        successor = list(self)
        if not upper_bound:
            successor[-1] += 1
            return DimensionVector(*successor)
        assert self < upper_bound, f"{self} must be < {upper_bound}"
        assert self << upper_bound, f"{self} should be << {upper_bound} for simplicity"
        idx = -1
        while True:
            if self[idx] < upper_bound[idx]:
                successor[idx] += 1
                return DimensionVector(*successor)
            else:
                successor[idx] = upper_bound[idx]
            idx -= 1

    def summands(self) -> Generator[DimensionVector, None, None]:
        e = self.copy()
        yield e
        while not e.is_zero():
            e = e.pred(upper_bound=self)
            yield e

    def partitions(self, below: Optional[DimensionVector] = None) -> Generator[dict[DimensionVector, int], None, None]:
        if below is None:
            below = 2 * self
        if below.is_zero():
            return
        d = below.pred(upper_bound=self)
        if d.is_zero():
            return
        q, r = divmod(self, d)
        i = 0
        while i < 10_000:
            if r.is_zero():
                yield {d: q}
            else:
                for part in r.partitions(below=d):
                    yield {d: q, **part}
            if q > 1:
                q -= 1
                r += d
            else:
                d = d.pred(upper_bound=self)
                if d.is_zero():
                    return
                q, r = divmod(self, d)
            i += 1
