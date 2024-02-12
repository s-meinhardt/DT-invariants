from __future__ import annotations

from typing import Protocol
from collections.abc import Iterator
from abc import abstractmethod
from itertools import chain

from .dimension_vector import DimensionVector


class Cone(Protocol):
    """A base class for cones.

    A cone is a subset of the lattice of dimension vectors, which
    contains the zero dimension vector and is closed under forming
    sums of dimension vectors. Although not checked by this class
    or any of its subclasses, we require that each dimension vector
    d in a cone has only finitely many summands, i.e. finitely many
    decompositions d = e + f with e and f also in the cone. This
    requirement ensures that motivic series which are supported on
    cones can be multiplied.

    One can iterate through the summands of a cone by using the
    :meth:`dt_invariants.Cone.summands` method. Note that this
    method needs to raise an StopIteration error after finitely
    many steps.

    A generalization of a sum decomposition is a partition, i.e. a
    sum decomposition with multiple summands up to order. A partition
    is represented by a dictionary with the keys being the distinct
    summands and the values being the multiplicities. Due to our
    requirement, each dimension vector in a cone has only finitely
    many partitions which can be accessed via the
    :meth:`dt_invariants.Cone.partitions` method provided by this
    base class.

    As cones are basically containers of dimension vectors, every child
    class must implement the :meth:`dt_invariants.Cone.__contains__`
    method allowing expressions like ``d in cone``.

    Note
    ----
    This class should not be used to build cones. The user should use
    any of its subclasses other cone producing methods.

    Attributes
    ----------
    rank : int
        The rank of the underlying lattice of dimension vectors, i.e.
        the required length of dimension vectors.

    name : str
        The name of the cone. If not provided by the user, it is the
        string representation of the cone object.

    """

    rank: int
    name: str

    def __repr__(self) -> str:
        """A method returning the representation of the cone.

        Returns
        -------
        str
            The name of the cone.
        """
        return self.name

    @abstractmethod
    def __contains__(self, d: DimensionVector) -> bool:
        """Abstract method to implement containment.

        Every child class must implement this method allowing
        boolean expressions like ``d in cone`` for any dimension
        vector d.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector to test.

        Returns
        -------
        bool
            Is the dimension vector contained in the cone?
        """
        ...

    @abstractmethod
    def _summands(self, d: DimensionVector, below: DimensionVector) -> Iterator[DimensionVector]:
        """Abstract method to iterate through special summands of a cone member.

        A summand is returned if and only if it is less than ``below`` in the
        lexicographic order.

        Note
        ----
        For performance reason, this method should not check if 'd' and
        'below' are in the cone. This will be ensured by the caller.

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

        """
        ...

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
        return chain([d], self._summands(d, below=d))

    def partitions(self, d: DimensionVector) -> Iterator[dict[DimensionVector, int]]:
        """A method to return all partions of a dimension vector.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector whose partitions we want to return.

        Yields
        ------
        Iterator[dict[DimensionVector, int]]
            An iterator looping through all partitions represented as
            dictionaries with keys being the distinct summands and values
            being the multiplicities.

        Raises
        ------
        AssertionError
            If the length of the dimension vector is not the
            rank of the cone.

        Example
        -------

        >>> cone = StandardCone(rank=2)
        >>> for partition in cone.partitions(DimensionVector(1,2))
        >>>     print(partition)
        {(1, 2): 1}
        {(1, 1): 1, (0, 1): 1}
        {(1, 0): 1, (0, 2): 1}
        {(1, 0): 1, (0, 1): 2}

        """
        assert self.rank == len(d), f"The dimension vector must have length {self.rank}!"
        return chain([{d: 1}], self._partitions(d, below=d))

    def _partitions(self, d: DimensionVector, below: DimensionVector) -> Iterator[dict[DimensionVector, int]]:
        """A method to return specific partitions of a dimension vector.

        A partition is returned if and only if all summands are less than
        ``below`` in the lexicographic order.

        Parameters
        ----------
        d : DimensionVector
            The dimension vector whose partitions we want to return.
        below : DimensionVector
            The upper (exclusive) bound for all summands in
            the partion.

        Yields
        ------
        Iterator[dict[DimensionVector, int]]
            An iterator looping through all partitions represented as
            dictionaries with keys being the distinct summands and values
            being the multiplicities.
        """
        for e in self._summands(d, below=below):
            if e.is_zero:
                continue
            q = 1
            r = d - e
            while r in self:
                if r.is_zero:
                    yield {e: q}
                else:
                    for partition in self._partitions(r, below=e):
                        yield {e: q, **partition}
                q += 1
                r -= e

    def __neg__(self) -> Cone:
        """A method to form the negative of a cone.

        The negative of a cone is obtained by forming the negative
        of all dimension vectors in the cone.

        Returns
        -------
        Cone
            The cone whose negative we want to build.

        >>> cone = StandardCone(rank=2)
        >>> neg_cone = -cone
        >>> DimensionVector(-2,-3) in neg_cone
        True

        """
        cone = Cone(rank=self.rank, name=f"-{self.name}")

        def _contains(instance, d: DimensionVector) -> bool:
            return -d in self

        def _summands(instance, d: DimensionVector) -> Iterator[DimensionVector]:
            for summand in self.summands(-d):
                yield -summand

        cone.__contains__ = _contains
        cone.summands = _summands

        return cone

    # def __getitem__(self, shift: int) -> Cone:
    #     name = f"{self.name}[{shift}]"
    #     if shift % 2 == 0:
    #         return Cone(rank=self.rank, is_contained=self.is_contained, pred_of=self.pred_of, name=name)
    #     else:
    #         return Cone(
    #             rank=self.rank,
    #             is_contained=lambda d: self.contains(-d),
    #             pred_of=lambda d, upper_bound: -self.pred_of(-d, -upper_bound),
    #             name=name,
    #         )
