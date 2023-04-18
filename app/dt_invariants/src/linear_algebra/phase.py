from __future__ import annotations

from cmath import phase
from math import pi


from .immutable import Immutable


class Phase(Immutable):
    """A class representing a real number.

    Representing a real number by the built-in data type `float`
    can cause errors when comparing or computing with real numbers.
    In our situation, these real numbers are typically of a special type.
    More specifically, they arrise as (normalized) phases of non-zero
    complex numbers with **integer** valued real and imaginary parts.
    For phases of this type, one can perform comparison and computations
    without running into errors by using the underlying (non-unique)
    presentation by complex numbers.
    An object of class :class:`Phase` remembers its origin but does not
    expose its origin via attributes as the defining complex number is not
    an intrinsic property of the phase. Two different complex numbers can
    have the same phase.

    Note that a phase of a complex number is within :math:`[0,2\\pi)`.
    Our phases are normalized by dividing it through :math:`\\pi` resulting
    in a real number in :math:`[0,2)`. To allow for higher or lower values,
    we can also choose a specific **branch** of the universal cover of the
    complex plane without zero. The default branch is 0 but a phase on
    branch 3 would be in :math:`[6, 8)`.

    Note
    ----
    A phase

    >>> phi = Phase.of(z=(a,b), branch=c)

    satisfies :math:`phi \\in [2*c, 2*c+2)` and

    .. math::
        a + b\\sqrt{-1} = \\sqrt{a^2 + b^2}\\exp(phi\\sqrt{-1}\\pi)

    Important
    ---------
    Phases are immutable objects. Thus, you cannot change any of its
    attributes after initialization, but you can use phases as keys
    in a dictionary.


    Parameters
    ----------
    value: int, default 0
        The value of the phase. We only allow initialization from
        integers as arbitrary floats might not have a presentation
        as the phase of a complex number with integer real and imaginary
        parts.

    Attributes
    ----------

    value: float
        The **float** representation of the phase.

    branch: int
        The integer part of ``value / 2``, in other words ``value // 2``.
        For a phase represented by a complex number, this is the branch
        of the logarithm of the (normalized to length one) complex number.
        Note that the branch along with the ``is_in_upper_half_plane``
        attribute completely determines the integer part of the phase.

    slope: float
        The negative cotangent of the fractional part of the phase
        (multiplied with pi). If the fractional part is zero, it is
        defined as :math:`\\inf`. For a phase represented by a complex
        number, this represents the slope of the line through 0 and
        the complex number (up to rotation by 90 degree).
        Note that the negative cotangent is a strictly monotone increasing
        function. In particular, the fractional part is completely
        determined by the slope.

    is_in_upper_half_plane: bool
        Is the integer part of the phase even? For a phase represented
        by a complex number, this returns if the complex number is in
        the upper half plane.
        Note that this boolean along with the ``branch``
        attribute completely determines the integer part of the phase.

    Examples
    --------

    Initializing a Phase with an integer

    >>> Phase(5)
    Phase(5.0)

    is no problem but a float will return an AssertionError

    >>> Phase(2.3)
    ...
    AssertionError: Only integer values are allowed

    Returning the Phase of a complex number

    >>> phi = Phase.of(z=(2,3))
    >>> phi
    Phase(0.3128329581890012)

    uses the default ``branch`` of 0, but one can also set a branch

    >>> phi2 = Phase.of((1,-1), branch=4)
    >>> phi2
    Phase(9.75)

    >>> phi2.branch
    4

    >>> phi2.is_in_upper_half_plane
    False

    >>> phi2.slope
    1.0

    The slope of an integer valued phase is :math:`\\inf`.

    >>> Phase(1).slope
    inf


    You can cast phases into other simple data types, in particular
    its **float** presentation.

    >>> float(phi)
    0.3128329581890012

    >>> int(phi)
    0

    >>> bool(phi)
    True

    You can also get the **float** presentation through the
    ``value`` attribute.

    >>> phi2.value
    9.75


    Phases can be added or subtracted

    >>> phi + phi2
    Phase(10.062832958189)

    >>> phi - phi2
    Phase(-9.437167041810998)

    You can also add/subtract an integer to a phase. The integer will
    be interpreted as the unique phase with the given value.

    >>> phi + 6
    Phase(6.312832958189001)

    The negative of a phase is

    >>> -phi
    Phase(-0.3128329581890012)

    The multiplication/division of phases is not defined even though
    these operations are possible for the underlying real numbers.
    The reason is that products or quotients might not be constructible
    from complex numbers with **integer** valued real and imaginary
    part.

    Phases can also be compared

    >>> phi < phi2
    True

    >>> phi == phi2
    False

    Recall that the real and the imaginary part are only
    determined by the value of a phase up to a positive multiple.

    >>> phi == Phase.of(z=(4,6))
    True
    """

    __slots__ = ["_real", "_imag", "branch"]

    def __init__(self, value: int = 0) -> None:
        assert isinstance(value, int), "Only integer values are allowed"

        branch, remainder = divmod(value, 2)
        object.__setattr__(self, "_real", (-1) ** remainder)
        object.__setattr__(self, "_imag", 0)
        object.__setattr__(self, "branch", branch)

        super().__init__()

    @classmethod
    def of(cls, z: tuple[int, int], branch: int = 0) -> Phase:
        """Create a phase from a given complex number.

        This method returns the phase of the complex number
        :math:`z[0] + \\sqrt{-1}z[1]` where the branch of the
        logarithm can be specified (default: 0).


        Parameters
        ----------
        z : tuple[int, int]
            The complex number whose phase we want to return.
        branch : int, default 0
            The branch of the logarithm.

        Returns
        -------
        Phase
            The phase of the complex number.

        Examples
        --------

        >>> Phase.of(z=(1,1))
        Phase(0.25)

        You can choose another branch of the logarithm
        moving the phase by ``2 * branch``.

        >>> Phase.of(z=(1,1), branch=3)
        Phase(6.25)

        """
        phase = cls()
        object.__setattr__(phase, "_real", z[0])
        object.__setattr__(phase, "_imag", z[1])
        object.__setattr__(phase, "branch", branch)
        return phase

    def covers(self, z: tuple[int, int]) -> bool:
        """Checks if ``z`` has the given phase ignoring the branch.

        For a non-zero complex number :math:`z[0] + z[1]\\sqrt{-1}` represented
        by the tuple ``z`` of integer valued real and imaginary parts, this method
        checks if the normalized phase of that number coinsides with the given
        phase modulo the branch cut, i.e. modulo 2.

        Attention
        ---------
        The method always returns True for the complex number 0.

        Parameters
        ----------
        z: tuple[int, int]
            A pair representing the real and imaginary part of a complex number.

        Returns
        -------
        bool
            Has the complex number :math:`z[0] + z[1]\\sqrt{-1}` the given phase modulo 2?

        Examples
        --------
        Every phase covers the complex number zero.

        >>> Phase.of(z=(2,3)).covers(z=(0,0))
        True

        Otherwise it just checks the phases modulo 2.

        >>> Phase.of(z=(2,3), branch=1).covers(z=(4,6))
        True

        >>> Phase.of(z=(2,3), branch=1).covers(z=(4,5))
        False
        """
        return self == Phase.of(z, branch=self.branch)

    @property
    def slope(self) -> float:
        """A method returning the slope of a phase.
        :noindex:
        The slope of a phase is defined as negative cotangent of the
        fractional part of the phase (multiplied with pi). If the fractional
        part is zero, it is defined as :math:`+\\inf`.

        Returns
        -------
        float
            The negative cotangent of the fractional part of the phase.

        Example
        -------

        >>> Phase.of(z=(3,2)).slope
        -1.5

        """
        if self._imag:
            return -self._real / self._imag
        else:
            return float("inf")

    @property
    def is_in_upper_half_plane(self) -> bool:
        """Is the integer part of the phase even?.

        For a phase represented by a complex number,
        this returns if the complex number is in
        the upper half plane.

        Note: For this method, the upper half plane also contains the positive real axis.

        Returns
        -------
        bool
            Is the defining complex number in the upper half plane?

        Examples
        --------
        Some obvious examples

        >>> Phase.of(z=(2,1)).is_in_upper_half_plane
        True

        >>> Phase.of(z=(2,-1)).is_in_upper_half_plane
        False

        and some less obvious examples.

        >>> Phase.of(z=(2,0)).is_in_upper_half_plane
        True

        >>> Phase.of(z=(-2,0)).is_in_upper_half_plane
        False
        """
        return self._imag > 0 or self._imag == 0 and self._real > 0

    @property
    def value(self) -> float:
        return float(self)

    def __repr__(self) -> str:
        return f"Phase({float(self)})"

    def __str__(self) -> str:
        return repr(self)

    def __hash__(self) -> int:
        return hash((self._real, self._imag, self.branch))

    def __eq__(self, other: Phase) -> bool:  # type: ignore[override]
        """Checks if the given phase has the same `value` as the `other` phase.

        Note
        ----
        The value of a phase only depends on the real and the imaginary part
        up to a positive factor.

        Parameters
        ----------
        other : Phase
            The other phase to compare with.

        Returns
        -------
        bool
            Is the value of the given phase the same as the value of the other phase?
        """
        return (
            int(self) == int(other) and self._real * other._imag == other._real * self._imag  # both have the same slope
        )

    def __lt__(self, other: Phase) -> bool:
        """Checks if the given phase is smaller than the `other` phase.

        Parameters
        ----------
        other : Phase
            The other phase to compare with.

        Returns
        -------
        bool
            Is the given phase smaller than the other phase?
        """
        if int(self) < int(other):
            return True
        elif int(self) > int(other):
            return False
        elif self._imag * other._real - self._real * other._imag < 0:
            return True
        else:
            return False

    def __le__(self, other: Phase) -> bool:
        """Checks if the given phase is less or equal the `other` phase.

        Parameters
        ----------
        other : Phase
            The other phase to compare with.

        Returns
        -------
        bool
            Is the given phase less or equal the other phase?
        """
        return self < other or self == other

    def __float__(self) -> float:
        """A method returning the **float** presentation of the phase.

        Returns
        -------
        float
            The float presentation of the phase.

        Example
        -------

        >>> float(Phase.of((1,1), branch=1))
        2.25

        """
        return 2 * (self.branch + (self._imag < 0)) + phase(complex(self._real, self._imag)) / pi

    def __int__(self) -> int:
        """A method returning the **int** presentation of the phase.

        Returns
        -------
        int
            The int presentation of the phase.

        Example
        -------

        >>> int(Phase.of(z=(0,-1), branch=3))
        7

        """
        if self.is_in_upper_half_plane:
            return 2 * self.branch
        else:
            return 2 * self.branch + 1

    def __bool__(self) -> bool:
        """A method returning the **bool** presentation of the phase.

        Returns
        -------
        bool
            Is the phase different from zero?

        Example
        -------

        >>> bool(Phase.of(z=(1,0)))
        False

        """
        return self.branch != 0 or self._imag != 0 or self._real != 0

    def __add__(self, other: int | Phase) -> Phase:
        """A method to add phases.

        Parameters
        ----------
        other : int | Phase
            The second summand.

        Returns
        -------
        Phase
            The result of adding the second summand to the given phase.
        """

        if isinstance(other, int):
            other = Phase(other)
        if not isinstance(other, Phase):
            ValueError("The second summand must be a Phase or an integer!")

        real = self._real * other._real - self._imag * other._imag
        imag = self._imag * other._real + self._real * other._imag
        sum_is_in_upper_half_plane = imag > 0 or imag == 0 and real > 0
        if self.is_in_upper_half_plane and other.is_in_upper_half_plane:
            branch: int = self.branch + other.branch
        elif self.is_in_upper_half_plane and not sum_is_in_upper_half_plane:
            branch = self.branch + other.branch
        elif other.is_in_upper_half_plane and not sum_is_in_upper_half_plane:
            branch = self.branch + other.branch
        else:
            branch = self.branch + other.branch + 1
        return Phase.of(z=(real, imag), branch=branch)

    def __radd__(self, other: int) -> Phase:
        return self + other

    def __neg__(self) -> Phase:
        """A method to return the negative of a phase.

        Returns
        -------
        Phase
            The negative of the given phase.
        """
        return Phase.of(z=(self._real, -self._imag), branch=-self.branch - 1)

    def __sub__(self, other: int | Phase) -> Phase:
        """A method to subtract phases.

        Parameters
        ----------
        other : int | Phase
            The subtrahend.

        Returns
        -------
        Phase
            The result of subtracting the subtrahend from the given phase.
        """
        return self + -other

    def __rsub__(self, other: int) -> Phase:
        return -self + other
