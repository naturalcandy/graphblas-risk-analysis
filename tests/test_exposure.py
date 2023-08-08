import graphblas as gb
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, Vector
from graphblas import binary
import pytest

def calculate_exposure_network(L: Matrix, c: Vector):
    """
    Calculates the exposure network based on the Asset Liability Network, L and 
    capital vector c.
    
    Parameters:
    - L: A sparse matrix where edges represent loans from one institution to another.
    - c: A vector representing the capital of each entity.
    
    Returns:
    - Matrix: A matrix where each entry represents the fraction of possible loss 
      institution 'i' might incur due to its loan exposure to institution 'j', 
      relative to 'j's capital.
    """
    W = L.dup()
    for j in range(L.nrows):
        W[:, j] << W[:, j].apply(binary.truediv, right=c[j]).apply(lambda x: min(1, x))
    return W


def test_basic():
    L = Matrix.from_coo([0, 0, 1, 2], [1, 2, 0, 1], [20.0, 30.0, 40.0, 80.0])
    c = Vector.from_coo([0,1,2], [100.0, 200.0, 300.0])
    exposure_network = calculate_exposure_network(L, c)
    expected = Matrix.from_coo([0,0,1,2], [1,2,0,1], [0.1,0.1,0.4,0.4])
    assert(exposure_network.isclose(expected))


def test_min_operator():
    L = Matrix.from_coo([0, 1, 2, 0], [0, 0, 0, 2], [40.0, 60.0, 80.0, 120.0])
    c = Vector.from_coo([0,1,2], [30.0, 10.0, 240.0])
    exposure_network = calculate_exposure_network(L, c)
    expected = Matrix.from_coo([0,1,2,0], [0,0,0,2], [1,1,1,0.5])
    assert(exposure_network.isclose(expected))

def test_zero_loan():
    L = Matrix.from_coo([0,0,1,1], [0,1,0,1], [0.0, 0.0, 0.0, 0.0])
    c = Vector.from_coo([0,1], [2,3])
    exposure_network = calculate_exposure_network(L, c)
    expected = Matrix.from_coo([0,0,1,1], [0,1,0,1], [0.0, 0.0, 0.0, 0.0])
    assert(exposure_network.isclose(expected))

