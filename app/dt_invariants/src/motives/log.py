from math import factorial, gcd, prod

from sympy import Integer, Rational, divisors, factor

from ..linear_algebra.dimension_vector import DimensionVector
from .motivic_series import MotivicSeries
from .symbols import R
from .types import FractionalMotive


class Log(MotivicSeries):
    def __init__(self, arg: MotivicSeries) -> None:
        super().__init__(cone=arg.cone, name=f"Log({arg.name})")
        self.arg = arg
        self._psi_cache: dict[DimensionVector, FractionalMotive] = {}
        self._validate()

    def _validate(self) -> None:
        assert (
            self.arg.at(DimensionVector.zero(num_vertices=self.rank)) == 1
        ), "coeff of argument at zero dimension vector must be 1"

    def _at(self, d: DimensionVector) -> FractionalMotive:
        if d.is_zero():
            return Integer(0)
        return factor(
            self.arg(d)
            - self._psi_red(d)
            - sum(
                prod((self._psi_red(e) + self(e)) ** m * Rational(1, factorial(m)) for e, m in p.items())
                for p in self.cone.partitions(d)
                if p != {d: 1}
            )
        )

    def _psi_red(self, d: DimensionVector) -> FractionalMotive:
        try:
            return self._psi_cache[d]
        except KeyError:
            n: int = d[0] if len(d) == 1 else gcd(*d)
            self._psi_cache[d] = factor(
                sum(self(d / k).subs(R, -((-R) ** k)) * Rational(1, k) for k in divisors(n) if k != 1)
            )
            return self._psi_cache[d]
