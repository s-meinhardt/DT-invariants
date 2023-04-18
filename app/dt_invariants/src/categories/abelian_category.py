from __future__ import annotations

from typing import Optional, cast

from ..linear_algebra.pairing import Pairing
from ..motives.motivic_series import MotivicSeries
from ..motives.symbols import R


class AbelianCategory:
    """A class representing an abelian category.

    This class represents an abelian category embedded into a
    triangulated category, typically in form of a t-structure.

    Moreover, a free abelian group has been chosen along with a
    'dimension vector' map assigning to each object an element in
    that group. This group can be a free abelian quotient of the
    Grothendieck group of the triangulated category.

    Attributes
    ----------
    name: str
        The name of the abelian category. If not provided at initialization,
        a generic name will be created by passing the category to 'repr()'.

    rank: int
        The rank of the free abelian group.

    euler_pairing: Pairing
        A :class:`Pairing` on the free abelian group which, when evaluated
        on the dimension vectors of two objects, should return the alternating
        sum of the (shifted) Hom groups.

    motive_of_objects: MotivicSeries
        A :class:`MotivicSeries` wrapping the motives of objects of the
        abelian category. For each dimension vector it returns an element
        in the (extended) Grothendieck group of varieties.

    normalized_motive_of_objects: MotivicSeries
        A :class:`MotivicSeries` wrapping the normalized motive of objects
        of the abelian category. For each dimension vector, the motive of
        objects will be normalized by dividing through
        :math:`\U0001D543^{vdim/2}`
        where *vdim* is the virtual dimension of the (derived) stack of objects
        of the given dimension vector and computed by the euler pairing.

    Raises
    ------
    AssertionError
        If the `motive_of_objects` and the `euler_pairing` have different ranks.
    """

    def __init__(self, motive_of_objects: MotivicSeries, euler_pairing: Pairing, name: Optional[str] = None) -> None:
        assert (
            euler_pairing.rank == motive_of_objects.rank
        ), "The motivic series and the euler pairing must have the same rank"

        self.rank = euler_pairing.rank
        self.euler_pairing = euler_pairing
        self.motive_of_objects = motive_of_objects
        self.name: str = name if name else repr(self)
        self._normalized_motive_of_objects: Optional[MotivicSeries] = None

    def __getitem__(self, shift: int) -> AbelianCategory:
        """A method to shift the abelian category.

        This method (mis)uses the standard *access key* notation to represent
        the shift of the abelian category within its triangulated category.

        Example
        --------
        For a given abelian catgory `ab_cat=AbelianCatgory(...)`
        the object `ab_cat[3]` represents the abelian category shifted 3 times.

        Parameters
        ---------
        shift: int
            The number of shifts to perform

        Returns
        -------
            AbelianCategory
                An :class:`AbelianCategory` wrapping the shifted abelian category
        """
        return AbelianCategory(
            motive_of_objects=self.motive_of_objects[shift],
            euler_pairing=self.euler_pairing,
            name=f"{self.name}[{shift}]",
        )

    @property
    def normalized_motive_of_objects(self) -> MotivicSeries:
        if self._normalized_motive_of_objects:
            return self._normalized_motive_of_objects
        else:
            self.set_normalized_motive_of_objects()
            return cast(MotivicSeries, self._normalized_motive_of_objects)

    def set_normalized_motive_of_objects(self) -> None:
        self._normalized_motive_of_objects = MotivicSeries(
            cone=self.motive_of_objects.cone,
            at_dv=lambda d: R ** self.euler_pairing(d, d) * self.motive_of_objects(d),
            name=f"{self.motive_of_objects.name}_vir",
        )
