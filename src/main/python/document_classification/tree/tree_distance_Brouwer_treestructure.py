"""Brouwer 2009 methods based on common paths."""
import trees
import logging
import itertools
from itertools import izip
import logging

from tree_distance_common import *
    
#####################################################################################

def _path_fraction_bonding_(common_levels, tree_depth):
    return float(common_levels) / tree_depth

#####################################################################################
        
def B_using_tree_l2c(leaf2clusters, bonding_calc = lambda common_levels: common_levels):
    """Generates bonding matrix for given tree.
    
    leaf2clusters - tree given as a dictionary {leaf: descending-list-of-clusters} 
    bonding_calc(common_levels) - should return membership-value under assumption that considered element has no common_levels of common levels with considered cluster
        common_level==0 -> only root is common
        common_level==1 -> single node (at top of a tree) is common
        common_level==depth -> every nodes are common (->leaf is inside the considered cluster)
    Order of rows and columns is the same as for sorted leaves.
    """        
    B = []             
    for lix,leaf in enumerate(sorted(leaf2clusters)):
        leaf_path = leaf2clusters[leaf]+[lix] #append leaf_no to path
        bv = [] #bonding vector
        for lix2,leaf2 in enumerate(sorted(leaf2clusters)):
            leaf2_path = leaf2clusters[leaf2]+[lix2] #append leaf_no to path            
            common_levels = calc_common_levels(leaf_path, leaf2_path)
            bv.append(bonding_calc(common_levels))
            #print "leaf_path, leaf2_path =",leaf_path, leaf2_path,"->",bonding_calc(common_levels)
        B.append(bv)
    return B

def B_using_tree(tree, bonding_calc = lambda common_levels: common_levels):
    """Generates bonding matrix for given tree.
    
    tree - description of a tree (given as a list of lists of lists...)
    For additional documentation see: B_using_tree_l2c.
    Sample use:
    >>> B_using_tree([ [[['a','b'], ['c']] , [['d','e','f'],['g','h']]], [[['x']],[['y']]] ]) == [[4, 3, 2, 1, 1, 1, 1, 1, 0, 0], [3, 4, 2, 1, 1, 1, 1, 1, 0, 0], [2, 2, 4, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 4, 3, 3, 2, 2, 0, 0], [1, 1, 1, 3, 4, 3, 2, 2, 0, 0], [1, 1, 1, 3, 3, 4, 2, 2, 0, 0], [1, 1, 1, 2, 2, 2, 4, 3, 0, 0], [1, 1, 1, 2, 2, 2, 3, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 4]]
    True
    """
    leaf2clusters = trees.bottomup2topdown_tree_converter(tree)
    return B_using_tree_l2c(leaf2clusters, bonding_calc)
    
#####################################################################################

            
def Brouwer_treestructure_B1B2(leaf2clusters_1, leaf2clusters_2, \
                 bonding_calc = lambda common_levels: common_levels):
    """Returns tuple B1,B2,leaf2ix where: B1,B2 - bonding matrices for two trees, leaf2ix - dictionary{leaf: index}.
     
    Bondings are calculated straightforward from structures of trees. 
    Trees are given as a dictionary {leaf: descending-list-of-clusters}.
    For details of:
     bonding_calc - see: B_using_tree_l2c 
    """    
    leaf2clusters_1, leaf2clusters_2, leaf2ix  = trees_prefiltering(leaf2clusters_1, leaf2clusters_2)
    logging.info("[Brouwer_treestructure_B1B2] leaf2ix = "+str(leaf2ix))
        
    B1 = B_using_tree_l2c(leaf2clusters_1, bonding_calc)
    logging.info("[Brouwer_treestructure_B1B2] B1 = "+str(B1)[:200])
    B2 = B_using_tree_l2c(leaf2clusters_2, bonding_calc)
    logging.info("[Brouwer_treestructure_B1B2] B2 = "+str(B2)[:200])
    return B1,B2, leaf2ix

#####################################################################################


if __name__=="__main__":
      
    import doctest
    doctest.testmod()