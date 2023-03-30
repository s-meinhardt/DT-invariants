from __future__ import annotations

from typing import Callable, Generator, Optional

from .dimension_vector import DimensionVector


class Cone:
    def __init__(
        self,
        rank: int,
        is_contained: Callable[[DimensionVector], bool],
        pred_of: Callable[[DimensionVector, DimensionVector], DimensionVector],
        name: Optional[str] = None,
    ) -> None:
        assert rank > 0
        self.rank = rank
        self.is_contained = is_contained
        self.pred_of = pred_of
        self.name = name if name else repr(self)

    def contains(self, d: DimensionVector) -> bool:
        return self.is_contained(d)

    def summands(self, d: DimensionVector) -> Generator[DimensionVector, None, None]:
        e = d.copy()
        yield e
        while not e.is_zero():
            e = self.pred_of(e, d)
            yield e

    def partitions(
        self, d: DimensionVector, below: Optional[DimensionVector] = None
    ) -> Generator[dict[DimensionVector, int], None, None]:
        if below is None:
            below = 2 * d
        if below.is_zero():
            return
        e = self.pred_of(below, d)
        if e.is_zero():
            return
        q, r = divmod(d, e)
        i = 0
        while i < 10_000:
            if r.is_zero():
                yield {e: q}
            else:
                for part in self.partitions(r, below=e):
                    yield {e: q, **part}
            if q > 1:
                q -= 1
                r += e
            else:
                e = self.pred_of(e, d)
                if e.is_zero():
                    return
                q, r = divmod(d, e)
            i += 1

    def divmod(self, d: DimensionVector, e: DimensionVector):
        q = 0
        r = d
        while self.contains(r):
            q += 1
            r -= e
        return q - 1, r + e

    def __getitem__(self, shift: int) -> Cone:
        name = f"{self.name}[{shift}]"
        if shift % 2 == 0:
            return Cone(rank=self.rank, is_contained=self.is_contained, pred_of=self.pred_of, name=name)
        else:
            return Cone(
                rank=self.rank,
                is_contained=lambda d: self.contains(-d),
                pred_of=lambda d, upper_bound: -self.pred_of(-d, -upper_bound),
                name=name,
            )
