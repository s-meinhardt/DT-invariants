from typing import Optional

from .cone import Cone
from .dimension_vector import DimensionVector
from collections.abc import Iterator


class StandardCone(Cone):
    """This class represents the standard cone.

    The standard cone of a given rank contains all dimension vectors with
    non-negative coordinates and of length given by the rank.


    Parameters
    ----------
    rank: int
        The rank of the lattice containing the standard cone.

    name: Optional[str]
        On optional name for the standard cone.

    Attributes
    ----------
    rank: int
        The rank of the lattice containing the standard cone.

    name: str
        On optional name for the standard cone which defaults to the
        presentation of the standard cone instance.
    """

    def __init__(self, rank: int, name: Optional[str] = None) -> None:
        self.rank = rank
        self.name = name if name else repr(self)

    def _pred_of(self, d: DimensionVector, upper_bound: DimensionVector) -> DimensionVector:
        """Returns the predecessor of a dimension vector in the standard cone.

        Given a dimension vector d in the standard cone, this method
        computes the maximum of the set of dimension vectors e smaller
        or equal the upper bound (with respect to the lexicographic order)
        satisfying :math:`0 <= e[i] <= d[i]` for all coordinates but e != d.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector whose predecessor is requested
        upper_bound : DimensionVector
            A predecessor must be smaller or equal this dimension vector.

        Returns
        -------
        DimensionVector
            The predecessor as explained above.

        Raises
        ------
        AssertionError
            If the dimension vector is zero or not in the cone.

        Example
        -------

        >>> cone = StandardCone(rank=2)
        >>> cone._pred_of(DimensionVector(2,3), upper_bound=DimensionVector(3,1))
        (2,1)

        """
        assert not d.is_zero, "Cannot make zero vector smaller"
        assert d in self, "The dimension vector must be conained in the cone!"
        predecessor: list = list(d)
        for idx, x in enumerate(d):
            if upper_bound[idx] < x:
                predecessor[idx:] = upper_bound[idx:]
                return DimensionVector(*predecessor)
        # at this point we have returned or self <<= upper_bound
        idx = -1
        while True:
            if d[idx] > 0:
                predecessor[idx] -= 1
                return DimensionVector(predecessor)
            else:
                predecessor[idx] = upper_bound[idx]
            idx -= 1

    def __contains__(self, d: DimensionVector) -> bool:
        """Returns if the dimension vector is contained in the given cone.

        To be contained in a standard cone, all coordinates of a
        dimension vector have to be non-negative.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector to test.

        Returns
        -------
        bool
            Is the dimension vector in the given cone.

        Raises
        ------
        AssertionError
            If the length of the dimension vector is not the
            rank of the cone.

        Example
        -------

        >>> cone = StandardCone(rank=2)
        >>> DimensionVector(2,3) in cone
        True

        >>> DimensionVector(-2,3) in cone
        False

        """
        assert self.rank == len(d), f"The dimension vector must have length {self.rank}!"
        return all(x >= 0 for x in d)

    def summands(self, d: DimensionVector) -> Iterator[DimensionVector]:
        """A method to generate all summands of a given dimension vector.

        A summand e of a dimension vector d is a dimension vector in the
        same cone such that d-e is also in the cone. The zero dimension
        vector and d itself are trivial examples.

        Parameters
        ----------
        d : DimensionVector
            The dimension vectors whose summands we want to compute.

        Yields
        ------
        Iterator[DimensionVector]
            An iterator looping through all summands of d.

        Raises
        ------
        AssertionError
            If the length of the dimension vector is not the rank of the cone
            or if the dimension vector is not in the cone.

        Example
        -------

        >>> cone = StandardCone(rank=2)
        >>> for summand in cone.summands(DimensionVector(1,1)):
        ...     print(summand)
        (1, 1)
        (1, 0)
        (0, 1)
        (0, 0)

        """
        assert self.rank == len(d), f"The dimension vector must have length {self.rank}!"
        assert d in self, "The dimension vector must be conained in the cone!"
        e = d.copy()
        while e in self:
            yield e
            if e.is_zero:
                return
            else:
                e = self._pred_of(e, upper_bound=d)
