from cmath import phase
from typing import Optional, Generator
from ..linear_algebra import DimensionVector
from ..categories import Quiver


class StabilityCondition:
    def __init__(self, quiver: Quiver, real: Optional[list[int]] = None, imag: Optional[list[int]] = None) -> None:
        self.real = real if real else list(0 for _ in quiver.vertices)
        self.imag = imag if imag else list(1 for _ in quiver.vertices)
        self.quiver = quiver
        self.num_vertices = quiver.num_vertices

        self._validate()

    def _real(self, d: DimensionVector) -> int:
        return sum(a * x for a, x in zip(self.real, d))

    def _imag(self, d: DimensionVector) -> int:
        return sum(a * x for a, x in zip(self.imag, d))

    def central_charge(self, d: DimensionVector) -> complex:
        assert len(d) == self.num_vertices, f"dimension vector must have {self.num_vertices} components"
        return complex(self._real(d), self._imag(d))

    def slope(self, d: DimensionVector) -> float:
        assert len(d) == self.num_vertices, f"dimension vector must have {self.num_vertices} components"
        return -self._real(d) / self._imag(d)

    def phase(self, d: DimensionVector) -> float:
        assert len(d) == self.num_vertices, f"dimension vector must have {self.num_vertices} components"
        return phase(self.central_charge(d))

    def __call__(self, d: DimensionVector, e: DimensionVector) -> int:
        """Calabi-Yau pairing"""
        assert len(d) == self.num_vertices, f"first dimension vector must have {self.num_vertices} components"
        assert len(e) == self.num_vertices, f"second dimension vector must have {self.num_vertices} components"
        return self.quiver.chi(d, e) - self.quiver.chi(e, d)

    def _validate(self) -> None:
        assert len(self.real) == self.num_vertices, f"the real part must have {self.num_vertices} components"
        assert len(self.imag) == self.num_vertices, f"the imaginary part must have {self.num_vertices} components"
        assert all(isinstance(a, int) for a in self.real), "the real part must consist of integers"
        assert all(isinstance(b, int) for b in self.imag), "the imaginary part must consist of integers"

    def colinear(self, d: DimensionVector, e: DimensionVector) -> bool:
        assert len(d) == self.num_vertices, f"first dimension vector must have {self.num_vertices} components"
        assert len(e) == self.num_vertices, f"second dimension vector must have {self.num_vertices} components"
        return self._real(d) * self._imag(e) == self._real(e) * self._imag(d)

    def partitions(
        self, d: DimensionVector, k: Optional[DimensionVector] = None
    ) -> Generator[dict[DimensionVector, int], None, None]:
        assert len(d) == self.num_vertices, f"dimension vector must have {self.num_vertices} components"
        if k:
            assert len(k) == self.num_vertices, f"upper bound dimension vector must have {self.num_vertices} components"
        else:
            k = 2 * d
        if k.is_zero():
            return
        e = k.pred(upper_bound=d)
        if e.is_zero():
            return
        q, r = divmod(d, e)
        i = 0
        while i < 10_000:
            if self.colinear(d, e):
                if r.is_zero():
                    yield {e: q}
                else:
                    for part in self.partitions(r, e):
                        yield {e: q, **part}
            if q > 1:
                q -= 1
                r += e
            else:
                e = e.pred(upper_bound=d)
                if e.is_zero():
                    return
                q, r = divmod(d, e)
            i += 1

    def hn_partitions(
        self, d: DimensionVector, k: Optional[DimensionVector] = None
    ) -> Generator[tuple[set, int], None, None]:
        assert len(d) == self.num_vertices, f"dimension vector must have {self.num_vertices} components"
        if k:
            assert len(k) == self.num_vertices, f"upper bound dimension vector must have {self.num_vertices} components"
        else:
            k = 2 * d
        if k.is_zero():
            return
        e = k.pred(upper_bound=d)
        if e.is_zero():
            return
        r = d - e
        i = 0
        while i < 10_000:
            if r.is_zero():
                yield {e}, 0
            else:
                for part, exponent in self.hn_partitions(r, e):
                    if not any(self.colinear(e, p) for p in part):
                        exponent += sum((-1) ** (self.phase(e) < self.phase(p)) * self(e, p) for p in part)
                        part.add(e)
                        yield part, exponent
            e = e.pred(upper_bound=d)
            r = d - e
            if e.is_zero():
                return
            i += 1
