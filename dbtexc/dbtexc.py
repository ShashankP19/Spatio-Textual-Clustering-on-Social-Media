
import numpy

# Reserved Labels for assigning clusters
NOISE = -1
UNCLUSTERED = 0

def dbtexc(m, eps, min_points, n_min, n_max):
	"""Implementation of DBSTexC: Density-Based Spatio-Textual Clustering on Twitter
	See https://dl.acm.org/citation.cfm?id=3110096
		Uses Euclidean Distance as the measure
		Inputs:
	m - A matrix whose columns are feature vectors, each row is a point
	eps - Maximum distance two points can be to be regionally related
	n_min - The minimum number of points to make a cluster
		Outputs:
	An array with either a cluster id number or dbscan.NOISE for each
	column vector in m.
    """
	    labels = [UNCLUSTERED]*len(m)
	    current_cluster = 0 # Current Cluster ID
			P  n range(0, len(m)):
		   (labels[P] != UNCLUSTERED):
            continue
		        relevant_neighbours, irrelevant_neighbours = regionQuery(m, P, eps)
				# TODO: Add condition checks for Noise
			len(relevant_neighbours) >= n_min and len(irrelevant_neighbours) <= n_max):
			# grcurrent_cluster += 1
        #    growCluster(m, labels, P, neighbours, current_cluster, eps, min_points)
	    # All data has been clustered!
    return labels
	for P in range(0, len(relevant_neighbours)):
		if(labels[P] != UNCLUSTERED):
			continue
		
def growCluster(m, labels, P, neighbours, current_cluster, eps, current_cluster, min_points):
    """
	Grow a new cluster with label current_cluster from the seed point P.
	
	This function sParches through the dataset to find all point, current_clusters that belong
	to tid, pointis nenumerateWhen this function rturns, cluster current_cluster is complete.
	
point	Parameters
		
		rel_nb, irrel_nb = regionQuery(m, point, eps)
		if(len(relevant_neighbours) >= n_min and len(irrelevant_neighbours) <= n_max):
				relevant_neighbors = relevant_neighbors.union(rel_nb)
				irrelevant_neighbors = relevant_neighbors.union(irrel_nb)
		labels[point] = current_cluster:
	
	if len(irrelevant_neighbours) != 0 :
		for id, point in enumerate(irrelevant_neighbours):
			if labels[point] == UNCLUSTERED:
				labels[point] = current_cluster
ls - List storing the cluster labels for all dataset points
	  P      - Index of the seed point for this new cluster
	  neighbours - All of the neighbors of P
	  current_cluster      - The label for this new cluster.  
		s    - Threshold distance
		n_points - Minimum required number of neighbors
		
		   			 the cluster label to the seed point.
	labels[P] = current_cluster
	
    # Look at each neighbor of P (neighbors are referred to as Pn). 
    # neighbours will be used as a FIFO queue of points to search--that is, it
    # will grow as we discover new branch points for the cluster. The FIFO
    # behavior is accomplished by using a while-loop rather than a for-loop.
    # In neighbours, the points are represented by their index in the original
    # dataset.
    """
    i = 0
    while i < len(neighbours):    
        
        # Get the next point from the queue.        
        Pn = neighbours[i]
       
        # If Pn was labelled NOISE during the seed search, then we
        # know it's not a branch point (it doesn't have enough neighbors), so
        # make it a leaf point of cluster current_cluster and move on.
        if labels[Pn] == -1:
           labels[Pn] = current_cluster
        
        # Otherwise, if Pn isn't already claimed, claim it as part of current_cluster.
        elif labels[Pn] == 0:
            # Add Pn to cluster current_cluster (Assign cluster label current_cluster).
            labels[Pn] = current_cluster
            
            # Find all the neighbors of Pn
            PnNeighborPts = regionQuery(m, Pn, eps)
            
            # If Pn has at least min_points neighbors, it's a branch point!
            # Add all of its neighbors to the FIFO queue to be searched. 
            if len(PnNeighborPts) >= min_points:
                neighbours = neighbours + PnNeighborPts
            # If Pn *doesn't* have enough neighbors, then it's a leaf point.
            # Don't queue up it's neighbors as expansion points.
            #else:
                # Do nothing                
                #neighbours = neighbours               
        
        # Advance to the next point in the FIFO queue.
        i += 1        
    
    # We've finished growing cluster current_cluster!


def regionQuery(X, Y, P, eps):
    """
    Find all points in dataset X and Y within distance eps of point P.
    
    This function calculates the distance between a point P and
 every other 
    point in the dataset, and then returns only those points which are within a
    threshold distance eps.
    """
    relevant_neighbors = []
    irrelevant_neighbors = []

    # Find relevant neighbors
    for q in range(0, len(X)):
        # If the distance is below the threshold, add it to the relevant neighbors list.
        if numpy.linalg.norm(X[P] - X[q]) < eps:
           relevant_neighbors.append(q)
    
    # Find irrelevant neighbors
    for q in range(0, len(Y)):
        # If the distance is below the threshold, add it to the irrelevant neighbors list.
        if numpy.linalg.norm(X[P] - Y[q]) < eps:
           irrelevant_neighbors.append(q)
            
    return relevant_neighbors, irrelevant_neighbors