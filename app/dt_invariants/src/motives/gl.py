from __future__ import annotations
from math import prod
from .types import Motive
from .symbols import L
from ..linear_algebra import DimensionVector


class GL(Motive):
    def __new__(cls, d: int | DimensionVector) -> GL:
        if isinstance(d, int):
            return prod(L**d - L**k for k in range(d))
        else:
            return prod(GL(n) for n in d)
