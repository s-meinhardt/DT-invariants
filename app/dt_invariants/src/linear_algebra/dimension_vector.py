from __future__ import annotations

from collections.abc import Iterable, Sequence


from .immutable import Immutable


class DimensionVector(Immutable, Sequence):
    """A class representing a tuple of integers.

    A dimension vector is basically a tuple of integers.
    The built-in Python tuple, however, does not behave
    like a vector. Adding two such tuples concatenates
    them rather than adding the coordinates.
    This class represents a tuple but behaves like a vector.
    Moreover, some useful extra properties and methods are
    provided.
    As the coordinates often represent dimensions, this class
    is called 'dimension vector'.

    Important
    ---------
    Dimension vectors are immutable objects. Thus, you cannot
    change any of its coordinates after initialization, but
    you can use dimension vectors as keys in a dictionary.

    Parameters
    ----------
    args : Iterable[int]
        The coordinates of the vector.

    Attributes
    ----------
    is_zero: bool
        Are all coordinates zero?

    successor: DimensionVector
        The following dimension vector in lexicographic order

    Examples
    --------

    You can initialize a dimension vector with a list of coordinates

    >>> DimensionVector(1,2)
    (1,2)

    or by providing any iterable of integers such as a generator

    >>> DimensionVector(x for x in range(3))
    (0,1,2)

    or a list.

    >>> DimensionVector([1,4])
    (1,4)

    Is my dimension vector zero?

    >>> DimensionVector(2,3,6).is_zero
    False

    If you need the zero dimension vector of a given length, use

    >>> d = DimensionVector.zero(length=3)
    >>> assert d.is_zero
    >>> d
    (0,0,0)

    Use the copy method to create another copy of a dimension vector.

    >>> d = DimensionVector(1,2)
    >>> e = d.copy()
    >>> d == e
    True

    >>> d is e
    False

    You can add or subtract dimension vectors as usual

    >>> d + e
    (2,4)

    >>> d - e
    (0,0)

    or multiply them by integers.

    >>> assert 3 * d == d * 3
    >>> 3 * d
    (3,6)

    You can also divide a dimension vector by an integer. Fractional
    quotients of coordinates will be rounded down.

    >>> d // 2
    (0,1)

    When comparing dimension vectors, we use the lexicographic order
    according to which we compare a specific coordinate starting from
    the left and only move to the right neighbour in case of a tie.

    >>> d = DimensionVector(1,4)
    >>> e = DimensionVector(1,7)
    >>> f = DimensionVector(2,1)
    >>> assert d <= e
    >>> assert d <= f

    Note that this is a total order, i.e. any two dimension vectors
    can be compared.
    To get the following dimension vector obtained by increasing the
    last coordinate, simply use

    >>> d.successor
    (1,5)

    """

    # __slots__ = ["_coord"]

    def __init__(self, *args) -> None:
        if isinstance(args[0], Iterable):
            object.__setattr__(self, "_coord", tuple(args[0]))
        else:
            object.__setattr__(self, "_coord", tuple(args))
        assert all(
            map(lambda x: isinstance(x, int), self._coord)
        ), "Coordinates must be integers!"
        super().__init__()

    @classmethod
    def zero(cls, length: int) -> DimensionVector:
        """A method generating the zero dimension vector of a given length.

        Parameters
        ----------
        length : int
            The length of the requested dimension vector.

        Returns
        -------
        DimensionVector
            The requested zero dimension vector.

        Example
        -------

        >>> DimensionVector.zero(length=3)
        (0,0,0)

        """
        return DimensionVector(0 for _ in range(length))

    @property
    def is_zero(self) -> bool:
        """Is this dimension vector zero?

        Returns
        -------
        bool
            Are all coordinates zero?
        """
        return all(map(lambda x: x == 0, self))

    @property
    def successor(self):
        """The following dimension vector in lexicographic order.

        Returns
        -------
        DimensionVector
            The dimension vector obtained by increasing the last
            coordinate by 1.
        """
        return self + DimensionVector((len(self) - 1) * [0] + [1])

    def copy(self) -> DimensionVector:
        """A method to create a different copy of a dimension vector.

        Returns
        -------
        DimensionVector
            Another copy of the dimension vector.

        Example
        -------

        >>> d = DimensionVector(1,2)
        >>> e = d.copy()
        >>> d == e
        True

        >>> d is e
        False

        """
        return DimensionVector(x for x in self)

    def __hash__(self) -> int:
        return hash(tuple(self))

    def __len__(self) -> int:
        return len(self._coord)

    def __getitem__(self, position: int) -> int:
        return self._coord[position]

    def __add__(self, other: DimensionVector) -> DimensionVector:
        assert len(self) == len(
            other
        ), "Both dimension vectors must have the same length!"
        """A method to add dimension vectors.

        Parameters
        ----------
        other : DimensionVector
            The second summand.

        Returns
        -------
        DimensionVector
            The dimension vector containing the pairwise sums of the coordinates.
        """
        assert len(self) == len(
            other
        ), "Both dimension vectors must have the same length!"
        return DimensionVector(map(lambda x: x[0] + x[1], zip(self, other)))

    def __iadd__(self, other: DimensionVector) -> DimensionVector:
        return self + other

    def __neg__(self) -> DimensionVector:
        """A method returning the negative of a dimension vector.

        Returns
        -------
        DimensionVector
            The dimension vector with the signs of the coordinates swapped.
        """
        return DimensionVector(-x for x in self)

    def __sub__(self, other: DimensionVector) -> DimensionVector:
        return self + -other

    def __isub__(self, other: DimensionVector) -> DimensionVector:
        return self - other

    def __mul__(self, factor: int) -> DimensionVector:
        """A method to multiply a dimension vector with an integer.

        Parameters
        ----------
        factor : int
            The second factor.

        Returns
        -------
        DimensionVector
            The dimension vector with all coordinates scaled by 'factor'.
        """
        return DimensionVector(map(lambda x: factor * x, self))

    def __rmul__(self, factor: int) -> DimensionVector:
        return self * factor

    def __imul__(self, factor: int) -> DimensionVector:
        return self * factor

    def __floordiv__(self, divisor: int) -> DimensionVector:
        """A method to divide a dimension vector by an integer.

        Parameters
        ----------
        divisor : int
            The divisor.

        Returns
        -------
        DimensionVector
            The dimension vector obtained by performing a floor division
            of all coordinates by the divisor.
        """
        return DimensionVector(map(lambda x: x // divisor, self))

    # def __floordiv__(self, other: DimensionVector) -> int:
    #     assert len(self) == len(other), "Both dimension vectors must have the same length!"
    #     assert not other.is_zero, "Cannot divide by zero vector!"
    #     eligible_pairs = filter(lambda x: x[1] != 0, zip(self, other))
    #     quotients = map(lambda x: x[0] // x[1], eligible_pairs)
    #     return min(quotients)

    def __mod__(self, other: int) -> DimensionVector:
        return self - other * (self // other)

    def __divmod__(self, other: int) -> tuple[DimensionVector, DimensionVector]:
        """
        returns the pair (self // other, self % other)
        """
        quotient = self // other
        return quotient, self - quotient * other

    def __repr__(self) -> str:
        return repr(tuple(self))

    def __lshift__(self, other: DimensionVector) -> bool:
        """
        implements the partial order relation << meaning that all coordinates
        are <= and both vectors do not coincide

        Note: d << e implies d < e
        """
        assert len(self) == len(
            other
        ), "Both dimension vectors must have the same length!"
        return all(map(lambda x: x[0] <= x[1], zip(self, other))) and self != other

    def __rshift__(self, other: DimensionVector) -> bool:
        """
        implements the partial order relation >> meaning that all coordinates
        are >= and both vectors do not coincide

        Note: d >> e implies d > e
        """
        assert len(self) == len(
            other
        ), "Both dimension vectors must have the same length!"
        return all(map(lambda x: x[0] >= x[1], zip(self, other))) and self != other

    def __eq__(self, other: DimensionVector) -> bool:
        assert len(self) == len(
            other
        ), "Both dimension vectors must have the same length!"
        return all(map(lambda x: x[0] == x[1], zip(self, other)))

    def __lt__(self, other: DimensionVector) -> bool:
        assert len(self) == len(
            other
        ), "Both dimension vectors must have the same length!"
        for x, y in zip(self, other):
            if x == y:
                continue
            return x < y

    def __le__(self, other: DimensionVector) -> bool:
        return self < other or self == other
