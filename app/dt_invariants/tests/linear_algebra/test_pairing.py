import pytest
from pytest import fixture
from pytest import mark as m

from app.dt_invariants import DimensionVector, Pairing


@fixture(autouse=True)
def pairing() -> Pairing:
  return Pairing(rank=3, coeff_matrix={(0, 0): 2})


@m.describe("Pairing Initialization")
def describe_initialize():
  @m.context("with correct attributes")
  def context_correct_attributes():
    @m.it("initializes the Pairing with correct attributes")
    def test_correct_attributes(pairing):
      assert pairing.rank == 3, "wrong number of vertices"
      assert isinstance(pairing.coeff_matrix, dict), "wrong type of coeff matrix"
      assert pairing.coeff_matrix.get((0, 0)) == 2, "wrong element at (0,0)"

  @m.context("with missing coefficient matrix")
  def context_missing_coeff_matrix():
    @m.it("uses a default matrix")
    def test_default_matrix():
      pairing = Pairing(rank=3)
      assert isinstance(pairing.coeff_matrix, dict), "default matrix is missing"

  @m.context("with incorrect attributes")
  def context_incorrect_attributes():
    @m.it("returns an error when rank is not a positive integer")
    def test_incorrect_rank():
      with pytest.raises(ValueError) as err:
        Pairing(rank=-3, coeff_matrix={(0, 0): 2})

      assert str(err.value) == "The rank must be a positive integer."

    @m.it("returns an error when the coeff_matrix is not a dictionary")
    def test_incorrect_coeff_matrix_type():
      with pytest.raises(ValueError) as err:
        Pairing(rank=3, coeff_matrix=[2, 3])

      assert (
        str(err.value) == "The coeff_matrix must be of type dict[tuple[int, int], int]."
      )

    @m.it("returns an error when the coeff_matrix has incorrect keys")
    def test_incorrect_coeff_matrix_keys():
      with pytest.raises(ValueError) as err:
        Pairing(rank=3, coeff_matrix={(0,): 2})

      assert (
        str(err.value)
        == "The keys of the coeff_matrix must be a tuple of two integers."
      )

    @m.it("returns an error when the indices are out of range")
    def test_incorrect_coeff_matrix_vertices():
      with pytest.raises(ValueError) as err:
        Pairing(rank=3, coeff_matrix={(3, 3): 2})

      assert str(err.value) == "The indices of the coeff_matrix be called 0,...,2."

    @m.it("returns an error when the coeff_matrix has incorrect elements")
    def test_incorrect_coeff_matrix_values():
      with pytest.raises(ValueError) as err:
        Pairing(rank=3, coeff_matrix={(0, 0): 1.4})

      assert str(err.value) == "The elements of the coeff_matrix must be integers."


@m.describe("Computation of pairing")
def describe_computation():
  @m.it("returns the correct values")
  def test_correct_values(pairing):
    d = DimensionVector(2, 1, 1)
    e = DimensionVector(2, 1, 0)
    assert pairing(d, d) == 8
    assert pairing(d, e) == 8

  @m.context("with no coeff matrix")
  def context_with_unit_matrix():
    @m.it("uses the unit matrix")
    def test_unit_matrix():
      pairing = Pairing(rank=3)
      d = DimensionVector(2, 1, 1)
      assert pairing(d, d) == 6
