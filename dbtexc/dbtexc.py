
import numpy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# Reserved Labels for assigning clusters
NOISE = -1
UNCLUSTERED = 0

# Labels for marking the points once it is visited
VISITED = True
UNVISITED = False


def dbtexc(X, Y, eps, n_min, n_max, tweet_similarity_threshold):
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

        eps_X, eps_Y = regionQuery(X, Y, point, eps, tweet_similarity_threshold)

        if(len(eps_X) >= n_min and len(eps_Y) <= n_max):
            current_cluster += 1
            clusters.append([])
            clusters = expandCluster(point, eps_X, eps_Y, visited_X, visited_Y,
                                     labels_X, labels_Y, X, Y, current_cluster, eps, n_min, n_max, clusters, tweet_similarity_threshold)

    return clusters, labels_X, labels_Y


def expandCluster(central_point, eps_X, eps_Y, visited_X, visited_Y, labels_X, labels_Y, X, Y, current_cluster, eps, n_min, n_max, clusters, tweet_similarity_threshold):
    labels_X[central_point] = current_cluster
    clusters[-1].append(X[central_point])

    index = 0
    while index < len(eps_X):
        point = eps_X[index]
        index += 1

        if visited_X[point] == VISITED:
            continue
        visited_X[point] = VISITED

        rel, irrel = regionQuery(X, Y, point, eps, tweet_similarity_threshold)
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


def regionQuery(X, Y, P, eps, tweet_similarity_threshold):
    """
    Find all points in dataset X and Y within distance eps of point P.

    This function calculates the distance between a point P and every other 
    point in the dataset, and then returns only those points which are within a
    threshold distance eps.
    """

    return findNeighbours(X, X, P, eps, tweet_similarity_threshold), findNeighbours(X, Y, P, eps, tweet_similarity_threshold)


def findNeighbours(rel_points, points, central_point, eps, tweet_similarity_threshold):
    neighbours = []

    # print(rel_points[central_point])

    for q in range(0, len(points)):
        # If the distance is below the threshold, add it to the neighbors list
        # print(central_point, q)
        # print(numpy.linalg.norm(rel_points[central_point] - points[q]))
        # print(rel_points[central_point][-1])
        # print(points[q][-1])
        if numpy.linalg.norm(rel_points[central_point][0:2] - points[q][0:2]) < eps:
            if tweet_similarity_threshold == 0 or similarity(rel_points[central_point][-1], points[q][-1]) >= tweet_similarity_threshold :
                neighbours.append(q)

    return neighbours


def similarity(a, b):
    # tokenization
    X_list = word_tokenize(a)
    Y_list = word_tokenize(b)

    # sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 = []
    l2 = []

    # remove stop words from string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)

    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine
