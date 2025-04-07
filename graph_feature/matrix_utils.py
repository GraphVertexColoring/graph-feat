import numpy as np

def build_matrices(edges, dimension):
    # generate the adjacency matrix
    adjacency = np.zeros((dimension, dimension), dtype = float)        
    # generate the laplacian matrix
    laplacian = np.zeros((dimension,dimension), dtype = float)
    for edge in edges:
        n1, n2 = edge
        adjacency[n1][n2] = adjacency[n2][n1] = 1

        laplacian[n1][n1] = laplacian[n1][n1] + 1
        laplacian[n2][n2] = laplacian[n2][n2] + 1
        if n1 != n2:
            laplacian[n1][n2] = laplacian[n2][n1] = -1
    return adjacency, laplacian
