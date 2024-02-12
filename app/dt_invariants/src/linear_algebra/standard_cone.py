from typing import Optional

from .cone import Cone
from .dimension_vector import DimensionVector
from collections.abc import Iterator


class StandardCone(Cone):
    """This class represents the standard cone.

    The standard cone of a given rank contains all dimension vectors with
    non-negative coordinates and of length given by the rank. Note that any
    summand ``e`` of a dimension vector ``d`` in the standard cone satisfies
    ``e <= d`` with resprect to the lexicographic order.


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

    Raises
    ------
        AssertionError
            If the rank is not positive.

    Examples
    --------

    >>> cone = StandardCone(rank=2)
    >>> assert DimensionVector(1,1) in cone
    >>> assert DimensionVector(-1,1) not in cone
    >>> print(cone)
    StandardCone(rank=2)

    """

    def __init__(self, rank: int, name: Optional[str] = None) -> None:
        assert rank > 0, "The rank must be positive!"
        self.rank = rank
        self.name = name if name else f"StandardCone(rank={rank})"

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

    def _summands(self, d: DimensionVector, below: DimensionVector) -> Iterator[DimensionVector]:
        """A method to iterate through special summands of a cone member.

        A summand is returned if and only if it is less than ``below`` in the
        lexicographic order.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector whose summands we want to return.
        below : DimensionVector
            The upper exclusive bound of all summands.

        Yields
        ------
        Iterator[DimensionVector]
            An iterator looping through all summands of d less than below
            including d and the zero dimension vector if they are less than
            ``below``. We don't require a specific order.

        Examples
        --------

        >>> cone = StandardCone(rank=2)
        >>> for summand in cone._summands(DimensionVector(1,2), below=DimensionVector(1,1)):
        >>>     print(summand)
        (1,0)
        (0,2)
        (0,1)
        (0,0)

        """
        if below.is_zero:
            return
        e = below
        while True:
            e = self._pred_of(e, upper_bound=d)
            yield e
            if e.is_zero:
                return

    def _pred_of(self, d: DimensionVector, upper_bound: DimensionVector) -> Optional[DimensionVector]:
        """Returns the biggest summand of 'upper_bound' less than 'd'.

        This method returns the biggest summand of 'upper_bound' less than
        'd' with respect to the lexicographic order. Note that being a summand
        defines a partial order on the cone. Thus, this method returns the biggest
        dimension vector less than 'd' with respect to the lexicographic order
        which is also bounded above by 'upper_bound' with respect to the partial
        order.

        Note
        ----
        For performance reason, this method does not check if 'd' and
        'upper_bound' are in the cone. This should be ensured by the caller.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector whose predecessor is requested.
        upper_bound : DimensionVector
            A predecessor must be a summand of the upper_bound.

        Returns
        -------
        DimensionVector
            The predecessor as explained above.


        Example
        -------

        >>> cone = StandardCone(rank=2)
        >>> cone._pred_of(d=DimensionVector(2,3), upper_bound=DimensionVector(1,2))
        (1,2)


        """
        candidate: list = list(d)
        for idx in range(self.rank):
            if upper_bound[idx] < d[idx]:
                # turning the candidate into a summand less than d
                candidate[idx:] = upper_bound[idx:]
                return DimensionVector(candidate)
        # at this point we have returned or d=candidate is a summand of upper_bound
        for idx in reversed(range(self.rank)):
            if d[idx] > 0:
                candidate[idx] -= 1
                return DimensionVector(candidate)
            else:
                candidate[idx] = upper_bound[idx]
