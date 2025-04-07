import os

def get_col_files(path):
    return [f for f in os.listdir(path) if f.endswith('.col')]

def read_col_file(file_path):
    edges = []
    dimension = 0

    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("p "):
                parts = line.split()
                dimension = int(parts[2])
            elif line.startswith("e "):
                n1, n2 = map(int, line.split()[1:])
                edges.append((n1-1, n2-1))  # Convert to 0-based index

    return edges, dimension
