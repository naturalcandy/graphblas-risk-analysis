import graphblas as gb
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, Vector
from graphblas import  unary, binary, monoid, semiring, select

#Rows represent the debtor (the one who owes money).
#Columns represent the creditor (the one who has given out the loan or to whom the money is owed).

def register_special_op(beta: float):
    #define custom operations         
    unary.register_new("health_update", lambda x: 1 if x > 1 else x)
    binary.register_new("scaled_addition", lambda x, y: x + y * beta)
    semiring.register_new("impact_semiring", monoid.times, binary.scaled_addition)

    #used for conditional checks regarding node state.
    select.register_new("greater_than_zero", lambda x, i, j, k: x > 0)
    select.register_new("not_equal_two", lambda x, i, j, k: x != 2)
      


def debt_rank_graphBLAS(L: Matrix, c: Vector, d: Vector,
                        h: Vector, s: Vector, 
                        beta: float, max_iter: int = 100) -> (Vector, float):
    
        #Calculate the exposure network W
        W = L.dup()
        W << W.ewise_mult(c, op="truediv")
        W << W.apply(lambda x: min(1, x))

        #Calculate the fraction of total outstanding loans v
        L_total = L.reduce_rowwise(monoid.plus)
        L_total_sum = L_total.reduce(monoid.plus)
        v = L_total / L_total_sum

        #add all special operations used in the simulation to graphBLAS namespace
        register_special_op(beta)

        #incorporate initial shock
        h << h.ewise_mult(d, binary.minus)

        #begin simulation
        for t in range(max_iter):

            mask = Vector(bool, s.size)
            mask << s.select("==", 1) #number for mask should map to what we want to represent as our distressed state
            indirect_impact = Vector(float, W.nrows)
            indirect_impact(mask) << W.mxv(h, semiring.impact_semiring)

            # Use the custom unary operation for health update
            h_new = Vector(float, h.size)
            h_new << h.ewise_mult(indirect_impact, binary.plus)            
            h_new = h.apply(unary.health_update)

            #update state vector
            s_new = s.dup()
            mask_zero = Vector(bool, h_new.size)
            mask_zero << h_new.select('==', 0)
            s_new(mask_zero)[:] << 2

            #initialize masks
            mask_positive = h_new.select(select.greater_than_zero)
            mask_s_not_2 = s.select(select.not_equal_two)

            combined_mask = Vector(bool, h_new.size)
            combined_mask << mask_positive.ewise_mult(mask_s_not_2, binary.land) 

            #update state vector
            s_new(combined_mask)[:] << 1

            #check for convergence (read about euclidean norm and try to see if useful here)
            if h.isclose(h_new) and s.isclose(s_new):
                break
            
            #update to reflect new health and state vectors
            h, s = h_new, s_new
    
        #calculate debtrank
        R = (h_new.ewise_mult(v).reduce() - h.ewise_mult(v).reduce())
        return h_new, R.new()






