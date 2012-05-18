"""Reads information about clusters and generates new similarity matrix (cluster vs. cluster)."""

#Skrypt bierze informacje o podziale na klastry wyliczonym z wejsciowej macierzy podobienstwa
#i na tej podstawie generuje nowe macierze podobienstw juz dla calych klastrow (macierz klaster vs klaster).

import data.io, calc.processing, calc.maths
import sys, os

def gen_clusters_similarity_matrix(inmatrix, clustdesc, aggregation_function):
    """Takes element-vs-element similarity matrix and calculates new cluster-vs-cluster similariy matrix.
       Input:
            inmatrix - symmetric element-vs-element similarity matrix
            clustdesc - clustering information: list of pairs: (cluster etiquette, list of indexes of assigned elements)
            aggregation_function - function that takes list of similarties: every_element_in_cluster_1-vs-every_element_in_cluster_2"""
    #loop over clusters
    outmatrix = data.io.create_matrix(len(clustdesc), len(clustdesc), value = 0)
    for cluster1No in xrange(0, len(clustdesc)):
        for cluster2No in xrange(cluster1No, len(clustdesc)):
            ixs1 = clustdesc[cluster1No][1]
            ixs2 = clustdesc[cluster2No][1]        
            subm = data.io.sub_matrix(inmatrix, ixs1, ixs2)    
            subm = data.io.serialize_matrix(subm) #list of similarites: every element from cluster1 vs every element form cluster 2 
            #cluster vs cluster similarity: 
            similarity =  aggregation_function(subm)  #<PLACE TO CALCULATE SIMIALRITY IN NEW MATRIX>
            #storing in output matrix:
            outmatrix[cluster1No][cluster2No] = similarity
            outmatrix[cluster2No][cluster1No] = similarity
    return outmatrix


if __name__ == "__main__":

    args = sys.argv
    if len(sys.argv) != 4:
        print "[ERROR] Exactly three arguments are expected: input-matrix-path labels'-prefix-length output-matrix-path"
        exit(-1)
    inMatrixPath    = args[1]                                                                   #input matrix
    prefix_len      = int(args[2])                                                              #length of prefix used for clusters' etiquettes generating
    outMatrixPath   = args[3]                                                                   #output matrix

    name            = os.path.basename(inMatrixPath).split('.')[0]                             #file path base name
    inClustPath     = '/tmp/tr_' + name + '_clustdesc_' + str(prefix_len) + '.txt'              #file with aggregated information about clusters (etiquette + list of indexes)



    #reading:
    inmatrix        = data.io.fread_smatrix_data(inMatrixPath)   # source matrix
    clustdesc       = data.io.fread_clusters(inClustPath)        # clustering

    #cluster-vs-cluster similarity matrix
    outmatrix       = gen_clusters_similarity_matrix(inmatrix, clustdesc, aggregation_function = max)
    
    #stores data:
    etiquettes = [cluster[0] for cluster in clustdesc]
    data.io.fwrite_smatrix(outmatrix, etiquettes, etiquettes, outMatrixPath)


