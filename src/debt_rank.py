import graphblas as gb
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, Vector
from graphblas import  unary, binary, monoid, semiring

"""
    Calculates the DebtRank of nodes in a financial network using GraphBLAS.

    Parameters:
    - L (Matrix): The Asset Liability Matrix where each element L_{ij} represents the 
                  amount of money that institution j has loaned to institution i.
    - c (Vector): Vector representing the total capital of each institution.
    - h (Vector): Initial health or economic value of institutions. 
                  Values should be in the range [0,1].
    - s (Vector): Initial state of each institution where:
                  0: Undistressed
                  1: Distressed
                  2: Inactive
    - max_iter (int, optional): Maximum number of iterations for the simulation. 
                                Default is 100.

    Returns:
    - Vector: DebtRank vector where each entry represents the DebtRank of the 
              corresponding institution.
    - float: Total DebtRank value for the entire network.

    Overview:
    The function simulates the propagation of distress in a financial network. 
    It calculates the exposure network W from the Asset Liability Matrix and the 
    capital vector. The function then computes the fraction of total outstanding 
    loans for each institution. Using an iterative approach, the function updates 
    the health and state of each institution based on their interactions with other 
    institutions. The DebtRank is then calculated as the difference between the 
    final impact and the initial impact caused by the distressed set.

    Notes:
    - Convergence is checked at each iteration. The simulation stops if the health 
      and state vectors do not change between iterations or if the maximum number 
      of iterations is reached.
    - The final state of the h and s vectors represent the remaining equity and state of
      all institutions once the simulation has completed. 
    """
def debt_rank_graphBLAS(L: Matrix, 
                        c: Vector,
                        h: Vector, 
                        s: Vector, 
                        max_iter: int = 100) -> Vector:
        
        #Calculate the exposure network W
        W = L.dup()
        for j in range(L.nrows):
            W[:, j] << W[:, j].apply(binary.truediv, right=c[j]).apply(lambda x: max(1, x))

        #Calculate the fraction of total outstanding loans v
        L_i = L.reduce_columnwise(monoid.plus)
        total_outstanding = L_i.reduce(monoid.plus).value
        v = Vector(float, L.ncols)
        v << L_i.apply(lambda x: x / total_outstanding)

        #store initial impact caused by our distressed set
        initial_impact = h.dup()
        initial_impact << (initial_impact.reduce(monoid.plus) * v)

        #allocate new health and state vectors for next iteration
        #h_new = Vector(float, h.size)
        s_new = Vector(int, s.size)

        #use the identity value of the addition monoid to avoid extra calculations
        #done in computing the sparsity of our updated health vector. 
        h_new = Vector(float, h.size)
        h_new[:] << 0.0

        mask_zero = Vector(bool, h_new.size)
            

        #begin simulation
        for t in range(max_iter):
            
            #set mask using state vector
            mask_zero << s.select('==', 0)

            #update health
            h_new(accum=binary.plus, mask=mask_zero) << W.mxv(h, semiring.plus_times)
            h(accum=binary.plus) << h_new.apply(binary.min, right=1)


            #update state
            condition1 = h.apply(lambda x: 1 if x > 0 else 0)
            condition2 = s.apply(lambda x: 2 if x == 1 else 0)
            temp = condition1.ewise_add(condition2, binary.max)
            s_new << temp.ewise_add(s, binary.max)

            #check for convergence
            if h.isclose(h_new) and s.isclose(s_new):
                break
            
            # Use h_new to store the intermediate results for next iteration
            h = h_new
            h_new[:] << 0.0
            s = s_new
        
        total_impact = h.reduce(monoid.plus)
        
        #calculate DebtRank
        debt_rank = (total_impact * v) - initial_impact
        
        return debt_rank.new()





