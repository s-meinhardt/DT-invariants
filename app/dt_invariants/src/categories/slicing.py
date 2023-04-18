from typing import Optional, cast

from ..linear_algebra.phase import Phase
from ..linear_algebra.pairing import Pairing
from ..motives.dt_invariant import DTInvariant
from ..motives.motivic_series import MotivicSeries
from ..motives.sliced_motive import SlicedMotive
from .abelian_category import AbelianCategory


class Slicing:
    """A class representing a slicing of a triangulated category.

    This class represents a slicing of a triangulated category, i.e.
    a function which assigns to each :class:`Phase` an abelian
    subcategory satisfying certain properties. Objects in any of
    those subcategories are often called *semistable* as slicings
    typically appear in the context of stability conditions. In general,
    however, *semistable* objects do not need to be semistable with
    respect to any stability condition.

    Moreover, a free abelian group has been chosen along with a
    'dimension vector' map assigning to each object an element in
    that group. This group can be a free abelian quotient of the
    Grothendieck group of the triangulated category.

    Attributes
    ----------
    name: str
        The name of the slicing. If not provided at initialization,
        a generic name will be created by passing the slicing to 'repr()'.

    rank: int
        The rank of the free abelian group.

    euler_pairing: Pairing
        A :class:`Pairing` on the free abelian group which, when evaluated
        on the dimension vectors of two objects, should return the alternating
        sum of the (shifted) Hom groups.

    motive_of_objects: SlicedMotive
        A :class:`SlicedMotive` wrapping the motives of objects of the
        triangulated category. For each dimension vector it returns an element
        in the (extended) Grothendieck group of varieties. For each phase it
        returns a :class:`MotivicSeries`.

    dt_invariants: SlicedMotive
        A :class:`SlicedMotive` wrapping the motives of *abstract*
        Donaldson-Thomas invariants basically defined as the plethystic
        logarithm of the normalized motive of *semistable* objects
        (of a given :class:`Phase`).

    Raises
    ------
    AssertionError
        If the `motive_of_objects` and the `euler_pairing` have different ranks.
    """

    def __init__(self, euler_pairing: Pairing, motive_of_objects: SlicedMotive, name: Optional[str] = None) -> None:
        assert (
            euler_pairing.rank == motive_of_objects.rank
        ), "euler pairing and motive of objects must have the same rank"
        self.rank = euler_pairing.rank
        self.euler_pairing = euler_pairing
        self.motive_of_objects = motive_of_objects
        self.name: str = name if name else repr(self)
        self._cache: dict[Phase, AbelianCategory] = {}
        self._dt_invariants: Optional[SlicedMotive] = None

    def __call__(self, phi: Phase) -> AbelianCategory:
        """A method to return *semistable* objects.

        Calling a slicing with a given :class:`Phase` will return the
        abelian subcategory of *semistable* objects of that :class:`Phase`.

        Example
        --------
        For a given slicing `slicing=Slicing(...)` and phase `phi=Phase(...)`
        the object `slicing(phi)` represents the abelian category of semistable
        objects of Phase `phi`.

        Parameters
        ----------
        phi : Phase
            The phase of *semistable* objects we are interested in.

        Returns
        -------
        AbelianCategory
            The abelian subcategory of *semistable* objects.
        """
        result = self._cache.get(phi)
        if result is None:
            result = AbelianCategory(
                motive_of_objects=cast(MotivicSeries, self.motive_of_objects(phi)),
                euler_pairing=self.euler_pairing,
                name=f"{self.name}({float(phi)})",
            )
            self._cache[phi] = result
        return result

    @property
    def dt_invariants(self) -> SlicedMotive:
        if self._dt_invariants:
            return self._dt_invariants
        else:
            self.set_dt_invariants()
            return cast(SlicedMotive, self._dt_invariants)

    def set_dt_invariants(self) -> None:
        self._dt_invariants = DTInvariant(slicing=self)
