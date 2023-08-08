import graphblas as gb
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, Vector
from graphblas import  unary, binary, monoid, semiring, indexunary



def health_state_dynamics(W: Matrix, h: Vector, s: Vector, test_for : int) -> Vector:
    """
    Tests the dynamics of the health (h) and state (s) vectors.
    
    Given the Exposure Matrix (W), equity vector (h), and state vector (s), this function computes the updated health 
    and state vectors after one iteration. Depending on the value of `test_for`, it returns either the updated health 
    or state vector.

    Parameters:
        - W: Exposure Matrix representing the Asset Liability Network.
        - h: Equity vector representing the health of each institution.
        - s: State vector indicating the distress state of each institution.
        - test_for: Integer to decide whether to return the health (1) or state vector.
    
    Returns:
        - Updated health or state vector after one iteration, based on the value of `test_for`.
    """
    potential_impact = Vector(float, h.size)
    h_new = Vector(float, h.size)
    s_new = Vector(int, s.size)
    
    #begin iteration 
    potential_impact << W.mxv(h, semiring.plus_times)
    h_new << h.ewise_mult(potential_impact, binary.plus).apply(binary.min, right=1)


    condition1 = h.apply(lambda x: 1 if x > 0 else 0)
    condition2 = s.apply(lambda x: 2 if x == 1 else 0)
    temp = condition1.ewise_add(condition2, binary.max)
    s_new << temp.ewise_add(s, binary.max)
    
    if test_for == 1:
        return h_new
        
    return s_new

def test_one_distress():
    W = Matrix.from_coo([0, 1, 1, 2], [1, 0, 2, 1], [0.5, 0.2, 1.0, 0.25])
    s = Vector.from_coo([0,1,2], [0, 1, 0])
    h = Vector.from_coo([0,1,2], [0.0, 0.5, 0.0])
    result_health = health_state_dynamics(W, h, s, 1)
    new_health = Vector.from_coo([0,1,2], [0.25, 0.5, 0.125])
    result_state = health_state_dynamics(W, h, s, 2)
    new_state = Vector.from_coo([0,1,2], [0, 2, 0])
    
    assert(result_health.isclose(new_health)) 
    assert(result_state.isclose(new_state))


def test_multiple_distress():
    W = Matrix.from_coo([0, 0, 1, 1, 2], [1, 2, 0, 2, 1 ], [0.5, 0.3, 0.2, 1.0, 0.25])
    h = Vector.from_coo([0,1,2], [0, 0.5, 0.4])
    s = Vector.from_coo([0,1,2], [0, 1, 1])
    result_health= health_state_dynamics(W, h, s, 1)
    new_health = Vector.from_coo([0,1,2], [0.37, 0.9, 0.525])
    result_state = health_state_dynamics(W, h, s, 2)
    new_state = Vector.from_coo([0,1,2], [0,2,2])

    assert(result_state.isclose(new_state))
    assert(result_health.isclose(new_health))