import csv
import graphblas as gb
gb.init("suitesparse", blocking=True)
from graphblas import Matrix, Vector, binary

FILE_EDGES = "data/raw/synthetic_data.csv"
FILE_NODES = "data/raw/synthetic_nodes.csv"


def read_financial_data(file_edges : str, file_nodes : str) -> (Matrix, Vector):
    """
    Reads financial data from provided CSV files and returns a GraphBLAS matrix and vector.
    
    Parameters:
    - file_edges (str): The path to the CSV file containing the financial data. 
                      
    - file_nodes (str): The path to the CSV file containing the financial nodes.
    
    Returns:
    - L (gb.Matrix): A GraphBLAS matrix representing exposures between institutions.
    - c (gb.Vector): A GraphBLAS vector representing the capital of each institution.
    """
    #create our asset liability matrix
    edges = []    
    with open(file_edges, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            node1, node2, exposure = int(row[0]), int(row[1]), float(row[2])
            edges.append((node1, node2, exposure))
    
    row_indices = [edge[0] for edge in edges]
    col_indices = [edge[1] for edge in edges]
    values = [edge[2] for edge in edges]
    
    L = Matrix.from_coo(row_indices, col_indices, values, dtype=float)

    #create our capital vector
    nodes = []
    with open(file_nodes, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            node1, capital = int(row[0]), float(row[1])
            nodes.append((node1, capital))
        node_indices = [node[0] for node in nodes]
        capital_indices = [node[1] for node in nodes]

        c = Vector.from_coo(node_indices, capital_indices)
    
    return L, c


def generate_distress(num_institutions: int, distress_vector: Vector):
    """
    Simulates the initial financial distress.

    Parameters:
    - num_institutions (int): The number of institutions.
    - distress_vector (gb.Vector): A vector of floats representing the initial shock, 's'
                                   applied to each institution. 

    Returns:
    - h (gb.Vector): A vector represenitng the health of all insitiutions after the initial shock
    - s (gb.Vector): A vector representing the state of all institutions after the initial shock
    """
    #state vector is discrete whereas health can range from 0 - 1
    health_vector = Vector(float, num_institutions)
    state_vector = Vector(int, num_institutions)
    health_vector[:] << 0
    state_vector[:] << 0

    #apply initial distress
    health_vector << health_vector.ewise_mult(distress_vector, binary.plus)
    distressed_institutions = health_vector.apply(lambda x: 1 if x != 0 else 0).new()
    state_vector << state_vector.ewise_mult(distressed_institutions, binary.bor)   

    return health_vector, state_vector

