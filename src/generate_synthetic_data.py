#Generates synthetic data to simulate financial relationships between institutions.

from data_utils import generate_synthetic_data, write_data


if __name__ == "__main__":
    N = 100  # Number of nodes
    E = 500  # Number of edges
    data = generate_synthetic_data(N, E)
    write_data("data/raw/synthetic_data.csv", data)