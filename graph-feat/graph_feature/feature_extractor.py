import numpy as np
import math
from .matrix_utils import build_matrices
from .shortest_path import shortest_path

def extract_features(file_name, edges, dimension):
    adjacency, laplacian = build_matrices(edges, dimension)
    features = {'source': file_name, 'num_vertices': dimension, 'num_edges': len(edges)}

    # Shortest Path Analysis
    dist_matrix = shortest_path(adjacency, dimension)
    dist_matrix[dist_matrix == float('inf')] = 0
    features['largest_dist'] = float(np.max(dist_matrix))
    features['average_dist'] = float(np.nanmean(np.where(dist_matrix == np.inf, np.nan, dist_matrix)))

    # Degree-based Metrics
    degrees = np.diag(laplacian)
    features['mean_degree'] = np.mean(degrees)
    features['std_deviation_degree'] = np.std(degrees)

    # Clustering Coefficient
    closed_triplets = np.trace(np.linalg.matrix_power(adjacency, 3)) / 6
    total_triplets = dimension * (dimension - 1) * (dimension - 2) / 6
    features['clustering_coef'] = closed_triplets / total_triplets if dimension >= 3 else 0

    return features
