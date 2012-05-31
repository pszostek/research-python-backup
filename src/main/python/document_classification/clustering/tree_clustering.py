"""Subroutines that generates tree by clustering leaves."""

import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')
sys.path.append(r'../../../')

import logging
import numpy


import trees
import sim_matrix

from cStringIO import StringIO
from numpy import array
from Bio import Phylo
import Bio
from Bio import Cluster
import numpy  






def generate_3level_tree(sim_matrix_l, clustering_l, similarity_aggregator_m, clustering_m):
    """Returns 3level tree generated using similarity matrix=sim_matrix_l, given clustering methods and similarity matrix aggregation method."""            
    #logging.info("[generate_3level_tree] --------------------------------------------------------")
    logging.info("[generate_3level_tree] Clustering L-level (xxyzz) (method:"+str(clustering_l)+")...")
    assignment_l = clustering_l(sim_matrix_l)
    #sil =  silhouettes(sim_matrix_l, range(2,len(sim_matrix_l),1), upgma.upgma_clustering, f=avgmax)
    #sil2 = dict( (s,k) for k,s in sil.iteritems() )
    logging.info("[generate_3level_tree] assignment_l = "+str(assignment_l)[:200])        
    
    #logging.info("[generate_3level_tree] --------------------------------------------------------")
    logging.info("[generate_3level_tree] Aggregating similarity matrix on M-level (aggregator:"+str(similarity_aggregator_m)+")...")
    sim_matrix_m = sim_matrix.aggregate_similarity_matrix_a(sim_matrix_l, assignment_l, similarity_aggregator_m)
    logging.info("[generate_3level_tree]  sim_matrix_m of size "+str(len(sim_matrix_m))+"x"+str(len(sim_matrix_m[0])))
    logging.info("[generate_3level_tree] \n"+str(numpy.array(sim_matrix_m))[:500])

    #logging.info("[generate_3level_tree] --------------------------------------------------------")
    logging.info("[generate_3level_tree] Clustering M-level (xxy) (method:"+str(clustering_m)+")...")
    assignment_m = clustering_m(sim_matrix_m)
    logging.info("[generate_3level_tree] assignment_m = "+str(assignment_m)[:200])

    #logging.info("[generate_3level_tree] --------------------------------------------------------")
    logging.info("[generate_3level_tree] Building 3level tree with assignment_l and assignment_m")
    new_tree = trees.build_3level_tree(assignment_l, assignment_m)
    new_leaf2clusters = trees.bottomup2topdown_tree_converter(new_tree)
    
    return new_leaf2clusters,new_tree


def generate_upgma_tree(similarity_matrix, agreggation_method = 'a'):
    """Returns tree generated using give simialrity_matrix and aggregation_method (for details see: Bio.Cluster.treecluster)."""    
    logging.info("[generate_upgma_tree] clustering agreggation_method="+str(agreggation_method))
    #similarity -> distances
    dmatrix             = [[1.0-sim for sim in row] for row in similarity_matrix]
    if agreggation_method == 's': agreggation_method = 'm'
    elif agreggation_method == 'm': agreggation_method = 's'
         
    ids = range(len(dmatrix))    
    tree = Bio.Cluster.treecluster(distancematrix = array(dmatrix), method = agreggation_method) #wyliczenie drzewa

    pnodes = {} #inicjalizacja slownika wezlow lisciami
    pheight = {} #slownik ktory dla danego nr wezla przechowuje jego wysokosc 
    for i in range(0, len(ids)):
        pnodes[i] = Bio.Phylo.BaseTree.Clade(name=ids[i], clades=[])
        pheight[i] = 0

    hidden_node_ix = 0 #biezacy nr ukrytego wezla    
    toplevel_nodes = set(ids)
    for node in tree:                    
        #dodaj wezel ukryty zlozony z dwoch juz istniejacych
        hidden_node_ix = hidden_node_ix - 1 
        left_node   = pnodes[node.left]
        right_node  = pnodes[node.right]
        #ustaw dlugosci galezi
        left_node.branch_length     = node.distance/2 - pheight[node.left] 
        right_node.branch_length    = node.distance/2 - pheight[node.right]
        #dodaj informacje o danym wezle        
        pnodes[hidden_node_ix] = Bio.Phylo.BaseTree.Clade(name=[left_node.name, right_node.name], clades=[left_node, right_node])
        pheight[hidden_node_ix] = node.distance/2

    return pnodes[hidden_node_ix].name

