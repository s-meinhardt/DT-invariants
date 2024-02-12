from .cone import Cone
from .dimension_vector import DimensionVector

from typing import Callable
from collections.abc import Iterator


class Subcone(Cone):
    """A class representing a subcone.

    Given a :class:`Cone`, and a suitable condition, this class
    generates the subcone of all dimension vectors of the given
    cone satisfying the condition. A condition is suitable if

    - the zero dimension vector satisfies the condition and
    - the sum of two dimension vectors satisfies the condition if
      each summand does.

    Being a child class of :class:`Cone`, a :class:`Subcone` inherits
    :meth:`dt_invariants.Cone.partitions`.

    Parameters
    ----------
    cone : Cone
        The cone of which we take the subcone of.

    condition: Callable[[DimensionVector], bool]
        Should a given dimension vector be part of the subcone?

    Examples
    --------

    >>> cone = StandardCone(rank=2)
    >>> # the second coordinate needs to be zero
    >>> condition = lambda d: d[1] == 0
    >>> subcone = Subcone(cone=cone, condition=condition)
    >>> assert DimensionVector(1,1) not in subcone
    >>> assert DimensionVector(1,0) in subcone

    """

    def __init__(self, cone: Cone, condition: Callable[[DimensionVector], bool]) -> None:
        self.rank = cone.rank
        self.name = f"Subcone({cone.name})"
        self._cone = cone
        self._condition = condition

    def __contains__(self, d: DimensionVector) -> bool:
        """Is the dimension vector contained in the subcone?

        To be contained in the subcone, the dimension vector has
        to be in the cone and has to satisfy the condition.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector to test.

        Returns
        -------
        bool
            Is the dimension vector in the subcone?

        Example
        -------

        >>> cone = StandardCone(rank=2)
        >>> subcone = Subcone(cone, condition=lambda d: d[1] == 0)
        >>> d = DimensionVector(1,1)
        >>> assert d in cone
        >>> d in subcone
        False

        """
        return (d in self._cone) and self._condition(d)

    def _summands(self, d: DimensionVector, below: DimensionVector) -> Iterator[DimensionVector]:
        """A method to return special summands of a dimension vector.

        This method returns all summands of the dimension vector 'd'
        which are smaller than 'below' in the lexicographic order.

        Parameters
        ----------
        d : DimensionVector
            The dimension vectors whose summands we want to return.
        below : DimensionVector
            Every returned summand must be smaller than 'below'.

        Yields
        ------
        Iterator[DimensionVector]
            An iterator looping through all summands.

        Example
        -------

        >>> cone = StandardCone(rank=2)
        >>> subcone = Subcone(cone, condition=lambda d: d[1] == 0)
        >>> for summand in subcone.summands(DimensionVector(1,1)):
        ...     print(summand)
        (1, 0)
        (0, 0)

        """
        return (s for s in self._cone._summands(d, below) if self._condition(s))
