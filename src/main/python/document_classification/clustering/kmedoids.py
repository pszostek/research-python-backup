"""K-medoids clustering."""
import sys
sys.path.append(r'../') 
import data_io
from data_io import matrix_io
from tools import matlab_wrapper

TMP_INPATH = "/tmp/kmedoids_simmatrix.txt"
TMP_OUTPATH = "/tmp/kmedoids_assignment.txt"

def kmedoids_clustering(similarity_matrix, k, maxits = 1000000):
    """Takes symmetric similarity matrix (list of lists) and returns list: assignment to clusters."""
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
    
    