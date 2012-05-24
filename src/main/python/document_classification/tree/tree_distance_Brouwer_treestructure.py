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
        
def B_using_tree_l2c(leaf2clusters, bonding_calc = lambda common_path_fraction: common_path_fraction):
    """Generates bonding matrix for given tree.
    
    leaf2clusters - tree given as a dictionary {leaf: descending-list-of-clusters} 
    bonding_calc(common_path_fraction) - returns bonding value  
    """        
    B = []             
    max_levels = trees.tree_depth(leaf2clusters)
    logging.info("[B_using_tree_l2c] max_levels="+str(max_levels))    
    
    for lix,leaf in enumerate(sorted(leaf2clusters)):
        leaf_path = leaf2clusters[leaf]+[lix] #append leaf_no to path
        bv = [] #bonding vector
        for lix2,leaf2 in enumerate(sorted(leaf2clusters)):
            leaf2_path = leaf2clusters[leaf2]+[lix2] #append leaf_no to path
            
            common_levels           = calc_common_levels(leaf_path, leaf2_path)                        
            #common_path_fraction    = float(common_levels) / max_levels
            #common_path_fraction    = 0.5*(float(common_levels) / len(leaf_path) + float(common_levels) / len(leaf2_path)) 
            #common_path_fraction    = max(float(common_levels) / len(leaf_path) , float(common_levels) / len(leaf2_path))
            common_path_fraction    = min(float(common_levels) / len(leaf_path) , float(common_levels) / len(leaf2_path))
            bv.append(bonding_calc(common_path_fraction))
            #print "leaf_path, leaf2_path =",leaf_path, leaf2_path,"->",bonding_calc(common_path_fraction)
            
        B.append(bv)
    return B

def B_using_tree(tree, bonding_calc = lambda common_path_fraction: common_path_fraction):
    """Generates bonding matrix for given tree.
    
    tree - description of a tree (given as a list of lists of lists...)
    For additional documentation see: B_using_tree_l2c.
    Sample use:
    >>> B_using_tree([ [[['a','b'], ['c']] , [['d','e','f'],['g','h']]], [[['x']],[['y']]] ], bonding_calc = lambda common_path_fraction: common_path_fraction*4.0) == [[4, 3, 2, 1, 1, 1, 1, 1, 0, 0], [3, 4, 2, 1, 1, 1, 1, 1, 0, 0], [2, 2, 4, 1, 1, 1, 1, 1, 0, 0], [1, 1, 1, 4, 3, 3, 2, 2, 0, 0], [1, 1, 1, 3, 4, 3, 2, 2, 0, 0], [1, 1, 1, 3, 3, 4, 2, 2, 0, 0], [1, 1, 1, 2, 2, 2, 4, 3, 0, 0], [1, 1, 1, 2, 2, 2, 3, 4, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 4, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 4]] 
    True
    """
    leaf2clusters = trees.bottomup2topdown_tree_converter(tree)
    return B_using_tree_l2c(leaf2clusters, bonding_calc)
    
#####################################################################################

            
def Brouwer_treestructure_B1B2(leaf2clusters_1, leaf2clusters_2, \
                 bonding_calc = lambda common_path_fraction: common_path_fraction):
    """Returns tuple B1,B2,leaf2ix where: B1,B2 - bonding matrices for two trees, leaf2ix - dictionary{leaf: index}.
     
    Bondings are calculated straightforward from structures of trees. 
    Trees are given as a dictionary {leaf: descending-list-of-clusters}.
    For details of:
     bonding_calc - see: B_using_tree_l2c 
    """    
    leaf2clusters_1, leaf2clusters_2, leaf2ix  = trees_prefiltering(leaf2clusters_1, leaf2clusters_2)
    logging.info("[Brouwer_treestructure_B1B2] leaf2ix = "+str(leaf2ix)[:200])
        
    B1 = B_using_tree_l2c(leaf2clusters_1, bonding_calc)
    logging.info("[Brouwer_treestructure_B1B2] B1 = "+str(B1)[:200])
    B2 = B_using_tree_l2c(leaf2clusters_2, bonding_calc)
    logging.info("[Brouwer_treestructure_B1B2] B2 = "+str(B2)[:200])
    return B1,B2, leaf2ix

#####################################################################################


if __name__=="__main__":
      
    import doctest
    doctest.testmod()