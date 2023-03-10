from typing import Optional
from sympy import factor, Integer, Rational, divisors
from math import prod, factorial, gcd
from .motivic_series import MotivicSeries
from ..motives import FractionalMotive, R
from ..linear_algebra import DimensionVector
from ..stability import StabilityCondition


class Log(MotivicSeries):
    def __init__(self, arg: MotivicSeries, stab_cond: Optional[StabilityCondition] = None) -> None:
        super().__init__(num_vertices=arg.num_vertices, name=f"Log({arg.name})")
        self.arg = arg
        self.stab_cond = stab_cond
        self._psi_cache: dict[DimensionVector, FractionalMotive] = {}
        self._validate()

    def _validate(self) -> None:
        assert (
            self.arg.at(DimensionVector.zero(num_vertices=self.arg.num_vertices)) == 1
        ), "coeff of argument at zero dimension vector must be 1"
        if self.stab_cond:
            assert (
                self.stab_cond.num_vertices == self.num_vertices
            ), f"stability condition must have {self.num_vertices} complex components"

    def _at(self, d: DimensionVector) -> FractionalMotive:
        if d.is_zero():
            return Integer(0)
        if self.stab_cond:
            parts = self.stab_cond.partitions(d)
        else:
            parts = d.partitions()
        return factor(
            self.arg.at(d)
            - self._psi_red(d)
            - sum(
                prod((self._psi_red(e) + self.at(e)) ** m * Rational(1, factorial(m)) for e, m in p.items())
                for p in parts
                if p != {d: 1}
            )
        )

    def _psi_red(self, d: DimensionVector) -> FractionalMotive:
        result = self._psi_cache.get(d)
        if result is None:
            n = d[0] if len(d) == 1 else gcd(*d)
            result = factor(sum(self.at(d / k).subs(R, -((-R) ** k)) * Rational(1, k) for k in divisors(n) if k != 1))
            self._psi_cache[d] = result
        return result
