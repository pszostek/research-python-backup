"""Functions that operates on similarity/distance matrices."""

import sys
sys.path.append(r'../') 
from data_io.matrix_io import *
from formats import *
from data_io import matrix_io
import logging

MIN_SIMILARITY_VALUE = 0.0
MAX_SIMILARITY_VALUE = 1.0

def aggregate_similarity_matrix(inmatrix, clustdesc, aggregation_function, diagonal_value = None):
    """Takes element-vs-element similarity matrix and calculates new cluster-vs-cluster similariy matrix.
       Input:
            inmatrix - symmetric element-vs-element similarity matrix
            clustdesc - clustering information: dictionary{assigned-cluster: list-of-elements-ixs-that-have-this-cluster-assigned}
            aggregation_function - function that takes list of similarties: every_element_in_cluster_1-vs-every_element_in_cluster_2
            diagonal_value - if != None then will be set on a diagonal of a matrix     
    """            
    logging.info("[aggregate_similarity_matrix] clustdesc = "+str(clustdesc)[:100])
    outmatrix = matrix_io.create_matrix(len(clustdesc), len(clustdesc), value = 0.0)
    cluster_names = clustdesc.keys()
    
    for cluster1No in xrange(0, len(cluster_names)):
        for cluster2No in xrange(cluster1No, len(cluster_names)):
            cn1,cn2 = cluster_names[cluster1No],cluster_names[cluster2No]             
            ixs1,ixs2 = clustdesc[cn1],clustdesc[cn2]
                         
            subm = sub_matrix(inmatrix, ixs1, ixs2)                             
            similarity =  aggregation_function(subm)  #cluster vs cluster similarity: #<PLACE TO CALCULATE SIMIALRITY IN NEW MATRIX>
            #logging.info("[aggregate_similarity_matrix] "+str(cn1)+" vs "+str(cn2)+ " -> " + str(subm[:5][:5])+"->"+str(similarity))
            #storing in output matrix:
            outmatrix[cluster1No][cluster2No] = outmatrix[cluster2No][cluster1No] = similarity
                        
    if not diagonal_value is None:
        set_diagonal(outmatrix, diagonal_value)
        
    return outmatrix

def set_diagonal(matrix, value):
    """Sets at every position of a matrix diagonal the value."""
    for i in xrange(len(matrix)):
        matrix[i][i] = value

def validate_similarity_matrix(simmatrix,minval=MIN_SIMILARITY_VALUE,maxval=MAX_SIMILARITY_VALUE):
    """Returns [(row1,col1,val11),...,(rowN,colN,valNN)] of cells where simmatrix value is incorrect."""
    errors = []
    for rowno, row in enumerate(simmatrix):
        for colno, element in enumerate(row):
            if element<minval or element>maxval:
                errors.append( (rowno, colno, element) )
    return errors       

def aggregate_similarity_matrix_a(inmatrix, assignment, aggregation_function, diagonal_value = None):
    """Does the same as aggregate_similarity_matrix but second parameter (assignment) is a list of elements' assignments to clusters."""    
    return  aggregate_similarity_matrix(inmatrix, assignment2clustdesc_converter(assignment), aggregation_function, diagonal_value)
    
def build_similiarity_matrix(elements, similarity_calculator):
    """Returns symmetric matrix of size len(elements) x len(elements) with values similiarty_calculator(element1, element2)."""
    dim = len(elements)
    matrix = create_matrix(dim, dim, value = 0.0)
    for r in xrange(dim):
        for c in xrange(r+1, dim):            
            matrix[r][c] = matrix[c][r] = similiarty_calculator(elements[r], elements[c])               
    return matrix


def build_sparse_similiarity_matrix(elements, selected_pairs, similarity_calculator):
    """Returns dictionary {(ix1,ix2): similarity} where (ix1,ix2) are taken from selected_pairs and similarity = similarity_calculator(elements[ix1],elements[ix2])."""
    return dict( ((ix1,ix2),similarity_calculator(elements[ix1],elements[ix2])) for ix1,ix2 in selected_pairs )