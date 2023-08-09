import csv
import graphblas as gb
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, Vector

def read_financial_data(filename="data/raw/synthetic_data.csv"):
    """
    Reads financial data from a CSV file and returns a GraphBLAS matrix and vector.
    
    The CSV file is expected to have the following columns:
    - Node1: The ID of the first node (institution) in an edge.
    - Node2: The ID of the second node (institution) in an edge.
    - Exposure: The exposure value between Node1 and Node2.
    - Capital: The capital value of Node1.
    
    The function returns:
    - A GraphBLAS matrix L where each entry L_{ij} represents the exposure from institution i to institution j.
    - A GraphBLAS vector C where each entry C_i represents the capital of institution i.
    
    Parameters:
    - filename (str): The path to the CSV file containing the financial data. 
                      Default is "data/raw/synthetic_data.csv".
    
    Returns:
    - L (grblas.Matrix): A GraphBLAS matrix representing exposures between institutions.
    - C (grblas.Vector): A GraphBLAS vector representing the capital of each institution.
    """
    edges = []    
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        for row in reader:
            node1, node2, exposure, capital = int(row[0]), int(row[1]), float(row[2]), float(row[3])
            # we assume that the capital of a node k is located in the kth row of the data
            edges.append((node1, node2, exposure, capital))
    
    row_indices = [edge[0] for edge in edges]
    col_indices = [edge[1] for edge in edges]
    values = [edge[2] for edge in edges]
    capital_values = [edge[3] for edge in edges]
    
    L = Matrix.from_coo(row_indices, col_indices, values, dtype=float)
    
    capital_indices = list(range(len(capital_values)))
    C = Vector.from_coo(capital_indices, capital_values)
    
    return L, C


L, C = read_financial_data()
print(L)
print(C)
