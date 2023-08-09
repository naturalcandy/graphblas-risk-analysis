import networkx as nx
import csv
import random

def generate_financial_network(n, m, weight_range=(1, 100)):
    """
    Generate a synthetic financial network using the Barabási-Albert model.
    
    Parameters:
    - n: Number of nodes
    - m: Number of edges to attach from a new node to existing nodes
    - weight_range: Tuple indicating the range of edge weights
    
    Returns:
    - List of edges in the format (edge1, edge2, weight, buffer)
    """
    G = nx.barabasi_albert_graph(n, m)
    
    edges = []
    for u, v in G.edges():
        # Assign weight based on the degree of the nodes
        weight = random.randint(weight_range[0], weight_range[1]) * (G.degree(u) + G.degree(v))
        edges.append((u, v, weight))
    
    # Generate buffer (capital) for each node based on its degree
    buffers = {node: G.degree(node) * random.randint(weight_range[0], weight_range[1]) for node in G.nodes()}
    
    return edges, buffers

def save_to_csv(edges, buffers, filename="data/raw/synthetic_data.csv"):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Node1", "Node2", "Exposure", "Capital"])  
        for edge in edges:
            writer.writerow([edge[0], edge[1], edge[2], buffers[edge[1]]])

# Parameters
n = 1000  # Number of nodes
m = 5    # Number of edges to attach from a new node to existing nodes

edges, buffers = generate_financial_network(n, m)
save_to_csv(edges, buffers)
