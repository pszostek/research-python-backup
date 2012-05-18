"""Functions that calculates membership of leaves of trees."""

import trees
import logging
import itertools
from itertools import izip
import logging
from math import sqrt
from math import acos
from math import pi

from tree_distance_common import *


def M_dictionary_l2c(leaf2clusters, membership_calc = lambda common_levels: common_levels):
    """Generates membership dictionary{leaf:membership-vector} for given tree.
    
    leaf2clusters - tree given as a dictionary {leaf: descending-list-of-clusters} (clusters' numbers must be unique at every level)
    membership_calc(common_levels) - should return membership-value under assumption that considered element has no common_levels of common levels with considered cluster
        common_level==0 -> only root is common
        common_level==1 -> single node (at top of a tree) is common
        common_level==depth -> every nodes are common (->leaf is inside the considered cluster)
    """
    #{lower-level-cluster: descending-list-of-clusters}
    lowestcluster2path = dict( (clusters_path[-1], clusters_path) for clusters_path in leaf2clusters.values() )
    #{leaf:membership-vector}             
    M_dict = {}
    for leaf,leaf_path in leaf2clusters.iteritems():
        mv = [] #membership vector
        for cluster,cluster_path in lowestcluster2path.iteritems():
            common_levels = calc_common_levels(leaf_path, cluster_path)
            mv.append( membership_calc(common_levels) )
        M_dict[leaf] = mv                
    return M_dict
    
def M_dictionary(tree, membership_calc = lambda common_levels: common_levels):
    """Generates membership dictionary{leaf:membership-vector} for given tree.
    
    tree - description of a tree (given as a list of lists of lists...)
    For additional documentation see: M_dictionary_l2c.    
    Sample use:
    >>> sorted(list(M_dictionary([ [[['a','b'], ['c']] , [['d','e','f'],['g','h']]], [[['x']],[['y']]] ]).iteritems()))
    [('a', [3, 2, 1, 1, 0, 0]), ('b', [3, 2, 1, 1, 0, 0]), ('c', [2, 3, 1, 1, 0, 0]), ('d', [1, 1, 3, 2, 0, 0]), ('e', [1, 1, 3, 2, 0, 0]), ('f', [1, 1, 3, 2, 0, 0]), ('g', [1, 1, 2, 3, 0, 0]), ('h', [1, 1, 2, 3, 0, 0]), ('x', [0, 0, 0, 0, 3, 1]), ('y', [0, 0, 0, 0, 1, 3])]
    """
    #{leaf: descending-list-of-clusters}    
    leaf2clusters = trees.bottomup2topdown_tree_converter(tree)
    return M_dictionary_l2c(leaf2clusters, membership_calc)

def M_dictionary2matrix(M_dict, leaf2ix = None):    
    """Converts M_dictionary{leaf: membership-vector} to matrix (list of lists) where single row represents single element's membership."""
    if leaf2ix is None:
        leaf2ix = dict((leaf,leaf) for leaf in M_dict)
    maxix = max(leaf2ix.values())
    ix2leaf = dict( (ix,leaf) for leaf,ix in leaf2ix.iteritems() )
    M = [ M_dict[ ix2leaf[ix] ] for ix in xrange(maxix+1) ]
    return M


if __name__=="__main__":
      
    import doctest
    doctest.testmod()    