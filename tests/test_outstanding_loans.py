import graphblas as gb
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, Vector
from graphblas import monoid
import pytest


def calculate_outstanding_loans(L : Matrix):
    """
    Calculates the fraction of total outstanding loans for each institution.
    
    Parameters:
    - L: A matrix where each entry L_{ij} represents the amount of money 
         that institution i owes to institution j.
         
    Returns:
    - A vector where each entry v_i represents the fraction of the total 
      outstanding loans in the system that are owed by institution i.
    """
    L_i = L.reduce_columnwise(monoid.plus)
    total_outstanding = L_i.reduce(monoid.plus).value
    v = Vector(float, L.ncols)
    v << L_i.apply(lambda x: x / total_outstanding)
    return v


def test_basic():
    L = Matrix.from_coo([0, 0, 1, 2], [1, 2, 0, 1], [20.0, 30.0, 40.0, 80.0])
    fraction_of_outstanding = calculate_outstanding_loans(L)
    expected = Vector.from_coo([0, 1, 2], [0.2352, 0.5882, 0.1764])
    assert(fraction_of_outstanding.isclose(expected, abs_tol=1e-4))
    

def test_owe_equal():
    L = Matrix.from_coo([0, 0, 1, 1, 2, 2], [1, 2, 0, 2, 0, 1], [20.0, 20.0, 20.0, 20.0, 20.0, 20.0])
    fraction_of_outstanding = calculate_outstanding_loans(L)
    expected = Vector.from_coo([0, 1, 2], [0.3333, 0.3333, 0.3333])
    assert(fraction_of_outstanding.isclose(expected, abs_tol=1e-4))