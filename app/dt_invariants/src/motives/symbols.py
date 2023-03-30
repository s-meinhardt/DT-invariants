from sympy import Rational, Symbol

from .types import Motive

L: Motive = Symbol("\U0001D543")
R: Motive = L ** Rational(1, 2)
