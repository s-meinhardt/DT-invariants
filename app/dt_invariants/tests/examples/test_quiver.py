import pytest
from pytest import fixture
from pytest import mark as m

from app.dt_invariants import AbelianCategory, DimensionVector, Pairing, Quiver


@m.describe("Quiver Initialization")
def describe_initialize():
  @m.context("with correct attributes")
  def context_correct_attributes():
    @fixture(autouse=True)
    def quiver() -> Quiver:
      return Quiver(num_vertices=3, arrow_matrix={(0, 0): 2}, name="test")

    @m.it("initializes the quiver with correct attributes")
    def test_correct_attributes(quiver):
      assert quiver.num_vertices == 3, "wrong number of vertices"
      assert isinstance(quiver.arrow_matrix, dict), "wrong type of arrow matrix"
      assert quiver.arrow_matrix.get((0, 0)) == 2, "wrong number of arrows"
      assert quiver.name == "test"
      assert isinstance(quiver.vertices, range), "wrong type of vertices"
      assert len(quiver.vertices) == 3, "wrong number of vertices"

    @m.it("initializes the hom, ext and euler pairing")
    def test_pairing_initialization(quiver):
      assert isinstance(quiver.hom, Pairing)
      assert isinstance(quiver.ext, Pairing)
      assert isinstance(quiver.euler_pairing, Pairing)

      d = DimensionVector(2, 1, 1)
      e = DimensionVector(2, 1, 0)
      assert quiver.hom(d, d) == 6
      assert quiver.hom(d, e) == 5
      assert quiver.ext(d, d) == 8
      assert quiver.ext(d, e) == 8
      assert quiver.euler_pairing(d, d) == -2
      assert quiver.euler_pairing(d, e) == -3

  @m.context("with missing quiver name")
  def context_missing_name():
    @m.it("uses a default name")
    def test_default_name():
      quiver = Quiver(num_vertices=3, arrow_matrix={(0, 0): 2})
      assert quiver.name == repr(quiver)

  @m.context("with incorrect attributes")
  def context_incorrect_attributes():
    @m.it("returns an error when num_vertices is not a positive integer")
    def test_incorrect_num_vertices():
      with pytest.raises(ValueError) as err:
        Quiver(num_vertices=-3, arrow_matrix={(0, 0): 2})

      assert str(err.value) == "The number over vertices must be a positive integer."

    @m.it("returns an error when the arrow_matrix is not a dictionary")
    def test_incorrect_arrow_matrix_type():
      with pytest.raises(ValueError) as err:
        Quiver(num_vertices=3, arrow_matrix=[2, 3])

      assert (
        str(err.value) == "The arrow_matrix must be of type dict[tuple[int, int], int]."
      )

    @m.it("returns an error when the arrow_matrix has incorrect keys")
    def test_incorrect_arrow_matrix_keys():
      with pytest.raises(ValueError) as err:
        Quiver(num_vertices=3, arrow_matrix={(0,): 2})

      assert (
        str(err.value)
        == "The keys of the arrow_matrix must be a tuple of two integers."
      )

    @m.it("returns an error when the vertices are out of range")
    def test_incorrect_arrow_matrix_vertices():
      with pytest.raises(ValueError) as err:
        Quiver(num_vertices=3, arrow_matrix={(3, 3): 2})

      assert str(err.value) == "The vertices of the quiver must be called 0,...,2."

    @m.it("returns an error when the arrow_matrix has incorrect values")
    def test_incorrect_arrow_matrix_values():
      with pytest.raises(ValueError) as err:
        Quiver(num_vertices=3, arrow_matrix={(0, 0): -2})

      assert (
        str(err.value)
        == "The number of arrows between two vertices must be non-negative integer."
      )

    @m.it("returns an error when the name of the quiver is not a string")
    def test_incorrect_name():
      with pytest.raises(ValueError) as err:
        Quiver(num_vertices=3, arrow_matrix={(0, 0): 2}, name=2)

      assert str(err.value) == "The name of the quiver must be a string."


@m.describe("Quiver Representations")
def describe_representations():
  @fixture(autouse=True)
  def quiver() -> Quiver:
    return Quiver(num_vertices=1, arrow_matrix={(0, 0): 1})

  @m.it("has an abelian category of representations")
  def test_has_representations(quiver):
    assert isinstance(quiver.reps, AbelianCategory)

  @m.it("skips the computation if already present")
  def test_single_computation(quiver):
    quiver._reps = "hello"
    assert quiver.reps == "hello"
