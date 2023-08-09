import csv
import numpy as np

def generate_financial_network(n, min_capital=1, max_capital=100, connection_factor=0.2, exposure_factor=0.6):
    """
    Generate a synthetic financial network with realistic capital and exposure ratios.
    
    Parameters:
    - n: Number of nodes (institutions)
    - min_capital, max_capital: Range for institution capital
    - connection_factor: Factor to determine number of connections based on capital
    - exposure_factor: Factor to determine exposure based on capital
    
    Returns:
    - List of edges in the format (node1, node2, exposure, capital)
    """
    # Generate capital for each node following a power-law distribution
    capitals = np.random.pareto(2, n) * (max_capital - min_capital) + min_capital
    
    edges = []
    for i in range(n):
        # Determine number of connections for node i based on its capital
        num_connections = min(n-1, int(capitals[i] * connection_factor))
        connections = np.random.choice(n, num_connections, replace=False)
        
        for j in connections:
            if i != j:  # Avoid self-loops
                exposure = min(capitals[i], capitals[j]) * exposure_factor
                edges.append((i, j, exposure, capitals[i]))
    
    return edges

def save_to_csv(edges, filename="data/raw/synthetic_data.csv"):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Node1", "Node2", "Exposure", "Capital"])  
        writer.writerows(edges)

# Parameters
n = 500  # Number of nodes

edges = generate_financial_network(n)
save_to_csv(edges)
