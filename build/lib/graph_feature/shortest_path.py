import numpy as np

def shortest_path(adj, dimension):
    INF = float('inf')

    dist = np.zeros((dimension, dimension), dtype = float)
    dist[dist == 0] = INF

    temp = np.copy(adj)
    n = 1
    k = 0
    while(n<=dimension):
        if k >= dimension**2:               # We know that the distance matrix got at most dimension squared values to modify
            break                           # Once all values are updated break, since no more updates will happen.

        temp[temp > 0] = 1
        temp = np.matmul(temp,adj)
        n += 1
        for x in range(dimension):
            for y in range(dimension):
                if temp[x][y] > 0:
                    if dist[x][y] == INF:   # Only updates if dist isnt updated yet
                        dist[x][y] = n
                        k += 1              # Counts updates
        
    np.fill_diagonal(dist, 0)
    return dist   