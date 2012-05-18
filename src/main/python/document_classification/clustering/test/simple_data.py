"""Generates simple data for testing purposes."""

import random
import numpy as np

def get_3clust_data():
    """Returns sample of 30 elements in 3 clusters."""
    X1 = list( -100+random.random() for i in xrange(10) )
    X2 = list( 0+random.random() for i in xrange(10) )
    X3 = list( 100+random.random() for i in xrange(10) )
    X = X1 + X2 + X3
    random.shuffle(X)
    
    distance_matrix = []
    for x in X:
        row = []
        for x2 in X:
            row.append( ((x-x2)*(x-x2)) )
        distance_matrix.append(row)
        
    max_d = max(max(distance_matrix))
    similarity_matrix = []
    for row in distance_matrix:
        srow = []
        for d in row:
            srow.append(1.0 - d/max_d)
        similarity_matrix.append(srow)
        
    return X,similarity_matrix