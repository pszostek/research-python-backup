
import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')

from tools import msc_processing
from tools import randomized
from data_io import zbl_io
from trees import *
from tree_distance import *
import tree_distance

import random
import logging
import trees
import math
import time
import trees

def gen_random_assignment(leaves, minpow = 0.25, maxpow = 0.75):
    """Returns random assignment for leaves."""
    min_clusters = round(math.pow(len(leaves), minpow))
    max_clusters = round(math.pow(len(leaves), maxpow))
    num_clusters = random.randint(min_clusters, max_clusters)
    #print "[trees.gen_random_assignment] num_clusters:",num_clusters
    assignment = [ random.randint(0, num_clusters-1) for l in leaves ]
    return assignment   

 
def get_random_tree2(leaves, minpow = 0.25, maxpow = 0.75):
    """Returns random 3-level tree (list of lists of lists...) + num_l,num_m (number of nodes at L/M level of the tree).
    
    Number of clusters at every level is using minpow,maxpow -> for details see: gen_random_assignment. 
    """
    assignment_l = gen_random_assignment(leaves, minpow, maxpow)
    num_l = len(set(assignment_l))
    #print "",num_l," clusters at M level"
    assignment_m = gen_random_assignment(xrange(num_l), minpow, maxpow)
    num_m = len(set(assignment_m))
    #print "",num_m," clusters at H level"
    
    rand_tree = build_3level_tree(assignment_l, assignment_m)
    #print str(trees.map_tree_leaves(rand_tree, ix2msc))[:400]      

    return rand_tree,num_l,num_m 

def get_random_tree(leaves, minpow = 0.25, maxpow = 0.75):
    """Returns random 3-level tree (list of lists of lists...).
    
    Number of clusters at every level is using minpow,maxpow -> for details see: gen_random_assignment.
    """
    return get_random_tree2(leaves, minpow, maxpow)[0]

def compare_to_random_tree(msc_leaf2clusters, \
                           bonding_calc, membership_calc, membership_bonding,\
                           only_fast_calculations = False):
    leaves = list( msc_leaf2clusters )     
    rand_tree,num_l,num_m = get_random_tree2(leaves)
    
    rand_leaf2clusters = trees.bottomup2topdown_tree_converter(rand_tree)
    indexes_dict = tree_distance.get_indexes_dict(msc_leaf2clusters, rand_leaf2clusters, \
                                                  bonding_calc, membership_calc, membership_bonding,\
                                                  only_fast_calculations)
    #print indexes_dict
     
    return (num_l, num_m, indexes_dict)


def get_random_tree_leaf2clusters(leaves, minpow = 0.25, maxpow = 0.75):
    """See: get_random_tree."""
    rand_tree = get_random_tree(leaves, minpow, maxpow)    
    rand_leaf2clusters = trees.bottomup2topdown_tree_converter(rand_tree)
    return rand_leaf2clusters,rand_tree
