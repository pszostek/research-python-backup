"""A set of auxiliary functions for tree distance calculating."""

import trees
import logging
import itertools
from itertools import izip
import logging
    
#####################################################################################
# Simple matrix operations:

def h(X):
    """Calculates upper half sum of squared matrix X.
    
    X - squared matrix (list of lists).
    
    >>> h([[1, 2, 3, 4],[2, 2, 2, 4],[3, 2, 2, 4],[4, 4, 4, 4]])
    19
    """
    total = 0
    for i in xrange(len(X)):
        for j in xrange(i+1, len(X)):
            total = total + X[i][j]
    return total
    
def complement(B):
    """Returns 1-B for matrix (list of lists) B.
    
    >>> complement([[0.3,0.2,0.5], [0.2,0.1,0.4], [0.5,0.4,0.5]]) ==  [[0.7, 0.8, 0.5], [0.8, 0.9, 0.6], [0.5, 0.6, 0.5]]
    True
    """
    cB = []
    for row in B:                 
        cB.append( list(1-e for e in row) )
    return cB
            
def pairwise_aggregation(A,B, tau = lambda a,b: a*b):
    """    
    Pairwise aggregation of elements of matrices (lists of lists) AxB.
    
    Returns matrix C=tau(A,B) where tau (e.g. multiplication) works on pairs of elements. 
    """
    C = []
    for rowA, rowB in izip(A,B): 
        C.append( list( tau(a,b) for a, b in izip(rowA,rowB) ) )
    return C              
    
#####################################################################################


def calc_common_levels(path1, path2):
    """Returns number of common levels in paths (lists of clusters)."""
    common_levels = 0
    for ancestor1,ancestor2 in izip(path1, path2):
        if ancestor1!=ancestor2: break 
        common_levels = common_levels + 1
    return common_levels 

#####################################################################################


def trees_prefiltering(leaf2clusters_1, leaf2clusters_2):
    """Returns tuple leaf2clusters_1, leaf2clusters_2, leaf2ix where trees are reduced to common leaves and leaf2ix = dictionary{leaf: index}"""
    #working on copy:
    leaf2clusters_1 = dict(leaf2clusters_1.iteritems())
    leaf2clusters_2 = dict(leaf2clusters_2.iteritems())
    #"intersection":
    trees.trim_common_leaves(leaf2clusters_1, leaf2clusters_2)
    #leaf2ix:
    leaves = leaf2clusters_1.keys()
    leaf2ix = dict( (leaf,i) for i,leaf in enumerate(sorted(leaves)) )    
    return leaf2clusters_1, leaf2clusters_2, leaf2ix 

#####################################################################################

if __name__=="__main__":
      
    import doctest
    doctest.testmod()
    