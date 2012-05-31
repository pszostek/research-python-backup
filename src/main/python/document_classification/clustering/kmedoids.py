"""K-medoids clustering."""
import sys
sys.path.append(r'../') 
import data_io
from data_io import matrix_io
from tools import matlab_wrapper
import logging

TMP_INPATH = "/tmp/kmedoids_simmatrix.txt"
TMP_OUTPATH = "/tmp/kmedoids_assignment.txt"

def kmedoids_clustering(similarity_matrix, k, maxits = 1000000):
    """Takes symmetric similarity matrix (list of lists) and returns list: assignment to clusters."""
    logging.info("[kmedoids_clustering] clustering objects="+str(len(similarity_matrix))+" k="+str(k))
    if len(similarity_matrix) <= k:        
        logging.warn("[kmedoids_clustering] objects="+str(len(similarity_matrix))+" is no more than clusters="+str(k)+"!")
        return range(0, len(similarity_matrix))
    
    labels = list( i for i in xrange(len(similarity_matrix)) )    
    matrix_io.fwrite_smatrix(similarity_matrix, labels, labels, TMP_INPATH)
    if matlab_wrapper.run_matlab("../clustering/kmedoids_matlab/kmedoids.m", [TMP_INPATH, (k), (maxits), TMP_OUTPATH]) != 0:
        raise Exception("[kmedoids_clustering] Matlab failure!")
    assignment = matrix_io.fread_ivector(TMP_OUTPATH)
    
    clusters = set(assignment) #przenumerowanie klastrow:
    clust2clust = dict( (old_no, new_no) for (new_no,old_no) in enumerate(clusters) ) 
    assignment = list(clust2clust[c] for c in assignment)
    return assignment


if __name__=="__main__":
    from test import simple_data
    X,similarity_matrix = simple_data.get_3clust_data()
        
    Xpos = list(int(round(x/100.0))+1 for x in X)
    assignment = kmedoids_clustering(similarity_matrix, k=3)
            
    import numpy as np            
    print np.array([Xpos, assignment])
    
    