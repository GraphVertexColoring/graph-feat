# graph_feature/feature_extractor.py
# Copyright (c) 2025 Frederik M. Dam
# This file is licensed under the GNU License.
# See the LICENSE file in the project root for full license text.
import numpy as np
import math
from .matrix_utils import build_matrices
from .shortest_path import shortest_path

def extract_features(file_name, edges, dimension):
    adjacency, laplacian = build_matrices(edges, dimension)
    features = {'source': file_name, 'num_vertices': dimension, 'num_edges': len(edges)}

    # Shortest Path Analysis
    dist_matrix = shortest_path(adjacency, dimension)

    # Replace infinities with NaN temporarily for stats
    dist_matrix_clean = np.where(dist_matrix == float('inf'), np.nan, dist_matrix)

    # Defensive handling
    if np.isnan(dist_matrix_clean).all():
        features['largest_dist'] = 0.0
        features['average_dist'] = 0.0
    else:
        features['largest_dist'] = float(np.nanmax(dist_matrix_clean))
        features['average_dist'] = float(np.nanmean(dist_matrix_clean))

    # Degree-based Metrics
    degrees = np.diag(laplacian)
    features['mean_degree'] = np.mean(degrees)
    features['std_deviation_degree'] = np.std(degrees)

    # Clustering Coefficient
    closed_triplets = np.trace(np.linalg.matrix_power(adjacency, 3)) / 6
    total_triplets = dimension * (dimension - 1) * (dimension - 2) / 6
    features['clustering_coef'] = closed_triplets / total_triplets if dimension >= 3 else 0

    # Adjacency eigenvalues
    eig_adj, _ = np.linalg.eig(adjacency)
    abs_eig_adj = np.abs(eig_adj)
    features['energy'] = np.mean(abs_eig_adj)

    mean_adj = np.mean(eig_adj)
    variance_adj = np.mean((eig_adj - mean_adj)**2)
    features['std_devi_eig_adj'] = math.sqrt(variance_adj)

    sorted_adj = sorted(eig_adj, key=lambda x: x.real)
    features['small_eig_adj'] = sorted_adj[0].real
    features['sec_small_eig_adj'] = sorted_adj[1].real
    features['large_eig_adj'] = sorted_adj[-1].real
    features['sec_large_eig_adj'] = sorted_adj[-2].real
    features['gap_eig_adj'] = abs(sorted_adj[-1] - sorted_adj[-2]).real

    # Laplacian eigenvalues
    eig_lap, _ = np.linalg.eig(laplacian)
    sorted_lap = sorted(eig_lap, key=lambda x: x.real)
    features['connectivity'] = sorted_lap[1].real

    non_zero_lap = [x for x in sorted_lap if not np.isclose(x, 0)]
    features['small_nonzero_eig_lap'] = non_zero_lap[0].real if len(non_zero_lap) > 0 else np.nan
    features['sec_small_nonzero_eig_lap'] = non_zero_lap[1].real if len(non_zero_lap) > 1 else np.nan

    features['large_eig_lap'] = sorted_lap[-1].real
    features['sec_large_eig_lap'] = sorted_lap[-2].real
    features['gap_eig_lap'] = abs(sorted_lap[-1] - non_zero_lap[0]).real if len(non_zero_lap) > 0 else np.nan

    return features
