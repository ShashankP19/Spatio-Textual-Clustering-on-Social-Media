
import numpy

# Reserved Labels for assigning clusters
NOISE = -1
UNCLUSTERED = 0

# Labels for marking the points once it is visited
VISITED = True
UNVISITED = False


def dbtexc(X, Y, eps, n_min, n_max):
    """
    Implementation of DBSTexC: Density-Based Spatio-Textual Clustering on Twitter
    See https://dl.acm.org/citation.cfm?id=3110096

    Uses Euclidean Distance as the measure

    Inputs:
    X - A matrix whose columns are feature vectors, each row is a relevant point
    Y - A matrix whose columns are feature vectors, each row is a ir    relevant point
    eps - Maximum distance two points can be to be regionally related
    n_min - The minimum number of points to make a cluster

    Outputs:
    An array with either a cluster id number or dbscan.NOISE for each
    column vector in m.
    """

    # Initialization
    n = len(X)
    m = len(Y)
    current_cluster = 0
    clusters = []

    labels_X = [UNCLUSTERED]*n
    visited_X = [UNVISITED]*n

    labels_Y = [UNCLUSTERED]*m
    visited_Y = [UNVISITED]*m

    for point in range(0, n):
        if visited_X[point] == VISITED:
            continue

        visited_X[point] = VISITED

        eps_X, eps_Y = regionQuery(X, Y, point, eps)

        if(len(eps_X) >= n_min and len(eps_Y) <= n_max):
            current_cluster += 1
            clusters.append([])
            clusters = expandCluster(point, eps_X, eps_Y, visited_X, visited_Y,
                          labels_X, labels_Y, X, Y, current_cluster, eps, n_min, n_max, clusters)

    return clusters


def expandCluster(central_point, eps_X, eps_Y, visited_X, visited_Y, labels_X, labels_Y, X, Y, current_cluster, eps, n_min, n_max, clusters):
    labels_X[central_point] = current_cluster

    index = 0
    while index < len(eps_X):
        point = eps_X[index]
        index += 1

        if visited_X[point] == VISITED:
            continue
        visited_X[point] = VISITED

        rel, irrel = regionQuery(X, Y, point, eps)
        if(len(rel) >= n_min and len(irrel) <= n_max):
            eps_X += rel
            eps_Y += irrel
        if labels_X[point] == UNCLUSTERED:
            labels_X[point] = current_cluster
            clusters[-1].append(X[point])

    if len(eps_Y) != 0:
        for point in eps_Y:
            if visited_Y[point] == UNVISITED:
                visited_Y[point] = VISITED
                if labels_Y[point] == UNCLUSTERED:
                    labels_Y[point] = current_cluster
                    clusters[-1].append(Y[point])

    return clusters


def regionQuery(X, Y, P, eps):
    """
    Find all points in dataset X and Y within distance eps of point P.

    This function calculates the distance between a point P and every other 
    point in the dataset, and then returns only those points which are within a
    threshold distance eps.
    """

    return findNeighbours(X, X, P, eps), findNeighbours(X, Y, P, eps)


def findNeighbours(rel_points, points, central_point, eps):
    neighbours = []

    # print(rel_points[central_point])

    for q in range(0, len(points)):
        # If the distance is below the threshold, add it to the neighbors list
        # print(central_point, q)
        if numpy.linalg.norm(rel_points[central_point] - points[q]) < eps:
            neighbours.append(q)

    return neighbours
