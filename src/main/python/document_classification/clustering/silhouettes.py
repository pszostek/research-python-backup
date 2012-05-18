"""Calculating number of clusters using silhouettes."""

import sys
sys.path.append(r'../') 
sys.path.append(r'../../') 
from trees import formats
import logging 
from itertools import izip
import upgma

def _c_as_(simmatrix, element_i, cluster_elements):
    """Calculates avg similarity for cluster.
    
    >>> simmatrix = [[0.9,0.4,0.3,0.2,0.1],[0.4,0.81,0.4,0.2,0.0],[0.3,0.4,0.85,0.7,0.6],[0.2,0.2,0.7,0.93,0.3],[0.1,0.0,0.6,0.3,0.8]]
    >>> round( _c_as_(simmatrix, 2, set([0,1,4]) ) * 1000 )
    433.0
    >>> round( _c_as_(simmatrix, 2, set([0,1,2,4]) ) * 1000 )
    433.0
    >>> round( _c_as_(simmatrix, 2, set([2]) ) * 1000 )
    850.0
    """    
    tot_sim = sum(simmatrix[max(element_i,element_j)][min(element_i,element_j)] for element_j in cluster_elements)                    
    if element_i in cluster_elements:                 
        if len(cluster_elements)==1:
            return simmatrix[element_i][element_i]
        else:
            return float(tot_sim-simmatrix[element_i][element_i]) / (len(cluster_elements)-1)
    return float(tot_sim) / len(cluster_elements)

def ab(cluster2elements, simmatrix, element_i, element_i_cluster):
    """Returns (a,b) for element_i in given clustering.
    
    cluster2elements - clustering {cluster-ix:container-of-elements-ixs}
    simmatrix - similarity matrix  
    element_i - index of considered element 
    element_i_cluster - cluster number for considered element
    
    >>> simmatrix = [[0.9,0.4,0.3,0.2,0.1],[0.4,0.81,0.4,0.2,0.0],[0.3,0.4,0.85,0.7,0.6],[0.2,0.2,0.7,0.93,0.3],[0.1,0.0,0.6,0.3,0.8]]
    >>> cluster2elements={0: [0], 1: [1,2,3], 2: [3,4]}
    >>> (a,b) = ab(cluster2elements, simmatrix, 2, 1)
    >>> round(a*1000), round(b*1000)
    (550.0, 650.0)
    """
    #c - cluster index, c_elements - list of elements in cluster c
    cluster2avgsim = dict( (c, _c_as_(simmatrix, element_i, c_elements)) for c,c_elements in cluster2elements.iteritems() )
     
    a = cluster2avgsim[element_i_cluster]
    cluster2avgsim.pop(element_i_cluster)
    b = max(cluster2avgsim.values())
    return (a,b)

def sil_i(a_i, b_i):
    """Returns sil_i for given a_i and b_i."""
    return float(a_i-b_i) / max(a_i,b_i)

def avg_sil(simmatrix, assignment):
    """For given assignment to clusters calculates average silhouette.
    
    simmatrix - similarity matrix (list of lists of values in [0,1])
    assignment - list of clusters numbers that are assigned to elements (i-th index on the list means i-th element) 
    """    
    cluster2elements    = formats.assignment2clustdesc_converter(assignment)
    cluster2elements    = dict( (cluster,set(elements)) for cluster,elements in cluster2elements.iteritems() )
    
    number_of_elements  = len(assignment)
    total_sil           = 0.0    
    for element_i, element_i_cluster in izip( xrange(number_of_elements), assignment):         
        a_i, b_i = ab(cluster2elements, simmatrix, element_i, element_i_cluster)
        logging.info("[avg_sil] element_i="+str(element_i)+" element_i_cluster="+str(element_i_cluster)+" a_i, b_i="+str( (a_i, b_i) ))
        total_sil = total_sil + sil_i(a_i, b_i)
    return float(total_sil) / number_of_elements


def silhouettes(simmatrix, possible_k, clustering_method):
    """
    Returns {k-value: average-silhouette(k)}.
    
    simmatrix - similarity matrix (given as list of lists)
    possible_k - list of k-values to be considered
    clustering_method(simmatrix, k) - returns assignment to clusters
    """    
    k2avgsil = {}
    for k in possible_k:        
        assignment          = clustering_method(simmatrix, k)    
        k2avgsil[k]         = avg_sil(simmatrix, assignment)
        logging.info("[silhouettes] considering k="+str(k)+" -> "+str(k2avgsil[k]))
    logging.info("[silhouettes] k2avgsil="+str(k2avgsil))
    return k2avgsil

def number_of_clusters(simmatrix, possible_k, clustering_method = upgma.upgma_clustering):
    """Calculates number of clusters using silhouettes."""
    k2avgsil = silhouettes(simmatrix, possible_k, clustering_method)
    return max( (v,k) for k,v in k2avgsil.iteritems() )[1]     
    
if __name__=="__main__":
      
    import doctest
    doctest.testmod()  

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    try:
        simmatrix_path = sys.argv[1]
    except:
        print "Argument expected: similarity matrix path"
        sys.exit(-1)
    print simmatrix_path
    
    from data_io import matrix_io
    (rows, cols, simmatrix) = matrix_io.fread_smatrix(simmatrix_path) #, datareader=matrix_io.__read_ftabs__, maxrows=1000
    print "matrix size=",len(simmatrix),"x",len(simmatrix[0])
    print simmatrix[0][:10]
    print simmatrix[1][:10]
    print simmatrix[2][:10]
    print simmatrix[3][:10]
    print simmatrix[4][:10]
    print "Selected k=",number_of_clusters(simmatrix, xrange(2, len(simmatrix)) ) 

