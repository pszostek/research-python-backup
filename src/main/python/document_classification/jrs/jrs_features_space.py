
import numpy
import random
from numpy import matrix
from scipy.spatial import distance
import logging
import time
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def empty_data(numrows, numcols, value):
    """Return list of lists structure filled in with value."""
    data = []
    for i in xrange(numrows):
        row = []
        for j in xrange(numcols):
            row.append(value)
        data.append(row)
    return data;
            

def dist(data, distance_calculator = distance.euclidean):
    """Returns symmetric matrix (observation x observation) -> distance between observations.
    
    data - list of lists (observations in rows, features in columns)
    distance_calculator(x,y) - returns distance between x and y
                               can be: distance.euclidean, distance.cosine,... 
    """
    distances = empty_data(len(data), len(data), 0.0)    
    for i in xrange(len(data)):
        row_start = time.clock()
        for j in xrange(i+1, len(data)):
            d = distance_calculator(data[i],data[j])
            distances[i][j] = d
            distances[j][i] = d 
        logging.info("next row="+str(i)+" processed in"+str(time.clock()-row_start))  
    return distances
                        

def covariance_matrix(data):
    """Returns covariance numpy.matrix for data (numpy.matrix) (observations in rows, feature in columns)"""
    return numpy.cov(data.transpose())

def uniform_sample_rows(data, samplesize):  
    """Selects by random samplesize rows from data. 
    
    data - list of lists (observations in rows, features in columns)
    """  
    ixs = range(len(data))
    random.shuffle(ixs)
    ixs = set(ixs[:samplesize])
    return [row for i,row in enumerate(data) if i in ixs]
    
    