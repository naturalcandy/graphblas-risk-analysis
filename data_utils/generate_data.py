import random

#generates raw synthetic data
def generate_synthetic_data(N, E):
    # Generate nodes
    nodes = list(range(1, N+1))
    # Generate edges
    edges = [(random.choice(nodes), random.choice(nodes)) for _ in range(E)]
    # Generate weights
    weights = [random.random() for _ in range(E)]
    # Combine nodes, edges and weights into a list of records
    records = [(edge[0], edge[1], weight) for edge, weight in zip(edges, weights)]
    
    return records 