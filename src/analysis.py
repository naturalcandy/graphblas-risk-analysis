#main entry point for analysis.

import graphblas as gb
# Context initialization
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, binary

from data_utils import csv_to_sparse

def main():
    #data = read_data('data/processed/preprocessed_data.csv')
    #print(data)
    (row, col, weight, dim) = csv_to_sparse('data/processed/preprocessed_data.csv')
    #assuming our matrix is a square matrix
    M = Matrix.from_coo(row, col, weight, nrows=dim, ncols=dim, dup_op=binary.plus)
    #since data is randomly generated, we handle duplicate edges by the dup_op flag.
    print(M)


if __name__ == '__main__':
    main()


