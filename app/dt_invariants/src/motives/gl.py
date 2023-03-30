from __future__ import annotations

from math import prod
from typing import cast

from ..linear_algebra.dimension_vector import DimensionVector
from .symbols import L
from .types import Motive


class GL(Motive):
    def __new__(cls, d: int | DimensionVector) -> GL:
        if isinstance(d, int):
            return prod(L**d - L**k for k in range(d))
        else:
            return cast(GL, prod(GL(n) for n in d))
