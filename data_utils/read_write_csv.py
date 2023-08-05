import pandas as pd

#reads csv file and returns a list of tuples, where each tuple represents an edge relationship in the graph.
def read_data(filename):
    df = pd.read_csv(filename, dtype={'Node1': int, 'Node2': int, 'Weight': float})
    return [tuple(row) for row in df.itertuples(index=False)]

#writes data to csv file
def write_data(filename, data):
    df = pd.DataFrame(data, columns=['Node1', 'Node2', 'Weight'])
    #casts columns
    df['Node1'] = df['Node1'].astype(int)
    df['Node2'] = df['Node2'].astype(int)
    df['Weight'] = df['Weight'].astype(float)
    df.to_csv(filename, index=False)

