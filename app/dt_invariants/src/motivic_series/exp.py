from typing import Optional
from sympy import Integer, Rational, factor, divisors
from math import prod, factorial, gcd
from .motivic_series import MotivicSeries
from ..motives import FractionalMotive, R
from ..linear_algebra import DimensionVector
from ..stability import StabilityCondition


class Exp(MotivicSeries):
    def __init__(self, arg: MotivicSeries, stab_cond: Optional[StabilityCondition] = None) -> None:
        super().__init__(num_vertices=arg.num_vertices, name=f"Exp({arg.name})")
        self.arg = arg
        self.stab_cond = stab_cond
        self._psi_cache: dict[DimensionVector, FractionalMotive] = {}
        self._validate()

    def _validate(self) -> None:
        assert (
            self.arg.at(DimensionVector.zero(self.arg.num_vertices)) == 0
        ), "coeff of argument at zero dimension vector must be 0"
        if self.stab_cond:
            assert (
                self.stab_cond.num_vertices == self.num_vertices
            ), f"stability condition must have {self.num_vertices} complex components"

    def _at(self, d: DimensionVector) -> FractionalMotive:
        if d.is_zero():
            return Integer(1)
        if self.stab_cond:
            parts = self.stab_cond.partitions(d)
        else:
            parts = d.partitions()
        return factor(sum(prod(self._psi(e) ** m * Rational(1, factorial(m)) for e, m in p.items()) for p in parts))

    def _psi(self, d: DimensionVector) -> FractionalMotive:
        result = self._psi_cache.get(d)
        if result is None:
            n = d[0] if len(d) == 1 else gcd(*d)
            result = factor(sum(self.arg.at(d / k).subs(R, -((-R) ** k)) * Rational(1, k) for k in divisors(n)))
            self._psi_cache[d] = result
        return result
