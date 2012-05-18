"""Performs DBSCAN clustering."""
import numpy as np
from scipy.spatial import distance
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs

def dbscan_clustering(similarity_matrix, dbeps=0.95, dbmin_samples=3):
    """Takes symmetric similarity matrix (list of lists) and returns list: assignment to clusters."""
    S = np.array(similarity_matrix)
    db = DBSCAN().fit(S, eps=dbeps, min_samples=dbmin_samples, metric='precomputed')
    print db
    return list(int(c) for c in db.labels_)

if __name__=="__main__":
    from test import simple_data
    X,similarity_matrix = simple_data.get_3clust_data()
        
    Xpos = list(int(round(x/100.0))+1 for x in X)
    assignment = dbscan_clustering(similarity_matrix, dbeps=0.5, dbmin_samples=1)
            
    print np.array([Xpos, assignment])
            