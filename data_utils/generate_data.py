import csv
import numpy as np

EDGE_FILENAME = "data/raw/synthetic_edges.csv"
NODE_FILENAME = "data/raw/synthetic_nodes.csv"
N = 500

def generate_financial_network(n, min_capital=1, max_capital=100, connection_factor=0.2, exposure_factor=0.6):
    """
    Generates a synthetic financial network with realistic capital and exposure ratios.
    """
    # Generate capital for each node following a power-law distribution
    capitals = np.random.pareto(2, n) * (max_capital - min_capital) + min_capital
    
    edges = []
    for i in range(n):
        # Determine number of connections for node i based on its capital
        num_connections = min(n-1, int(capitals[i] * connection_factor))
        connections = np.random.choice(n, num_connections, replace=False)
        
        for j in connections:
            if i != j:  # avoid self loans
                exposure = min(capitals[i], capitals[j]) * exposure_factor
                edges.append((i, j, exposure))
    
    return capitals, edges

def save_to_csv(edges, capitals, edge_filename, node_filename):
    # Save node (capital) data
    with open(node_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["NodeID", "Capital"])  
        for i, capital in enumerate(capitals):
            writer.writerow([i, capital])

    # Save edges
    with open(edge_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Node1", "Node2", "Exposure"])  
        writer.writerows(edges)

if __name__ == '__main__':
    capitals, edges = generate_financial_network(N)
    save_to_csv(edges, capitals, EDGE_FILENAME, NODE_FILENAME)
