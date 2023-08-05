import pandas as pd


#Reads csv file and uses columns to construct tuple of lists used in creating sparse matrix.
def csv_to_sparse(filename):
    df = pd.read_csv(filename)
    first_nodes = df.loc[:, "Node1"]
    second_nodes = df.loc[:, "Node2"]
    weights = df.loc[:, "Weight"]
    size = max(first_nodes.max(), second_nodes.max()) + 1
    return (first_nodes.tolist(), second_nodes.tolist(), weights.tolist(), size)