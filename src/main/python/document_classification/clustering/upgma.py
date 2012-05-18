"""UPGMA clustering."""

import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')

from cStringIO import StringIO
from numpy import array
from Bio import Phylo
import Bio
from Bio import Cluster
import numpy  


def upgma(dmatrix, k, agreggation_method = 'a'):
    """Retruns k binary biopython trees built using hierarchical clustering (Bio.Cluster.treecluster mode: agreggation_method)."""
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
        if len(toplevel_nodes) <= k: break             
        #dodaj wezel ukryty zlozony z dwoch juz istniejacych
        hidden_node_ix = hidden_node_ix - 1 
        left_node   = pnodes[node.left]
        right_node  = pnodes[node.right]
        #zaktualizuj zestaw wezlow na szczycie
        toplevel_nodes.remove(left_node.name)
        toplevel_nodes.remove(right_node.name)
        toplevel_nodes.update([hidden_node_ix])
        #ustaw dlugosci galezi
        left_node.branch_length     = node.distance/2 - pheight[node.left] 
        right_node.branch_length    = node.distance/2 - pheight[node.right]
        #dodaj informacje o danym wezle        
        pnodes[hidden_node_ix] = Bio.Phylo.BaseTree.Clade(name=hidden_node_ix, clades=[left_node, right_node])
        pheight[hidden_node_ix] = node.distance/2
        
    return [Bio.Phylo.BaseTree.Tree(root=pnodes[node_id], rooted=True) for node_id in toplevel_nodes]


def extract_leaves(biotree):
    """Returns list of names of leaves of biopython tree."""
    leaves = []
    def update_leaves_list(clade):
        if len(clade.clades) == 0: 
            leaves.append(clade.name)
        else:            
            for c in clade.clades:
                update_leaves_list(c)
    update_leaves_list(biotree.root)
    return leaves
        

def upgma_clustering(similarity_matrix, k, agreggation_method = 'a'):    
    dmatrix = [[1.0-sim for sim in row] for row in similarity_matrix]    
    clusters = upgma(dmatrix, k, agreggation_method)
    assignment = range(len(similarity_matrix))
    for clustno,clusttree in enumerate(clusters): 
        for leave in extract_leaves(clusttree):
            assignment[leave] = clustno 
    return assignment
    
    

if __name__=="__main__":
    from test import simple_data
    X,similarity_matrix = simple_data.get_3clust_data()        
        
    Xpos = list(int(round(x/100.0))+1 for x in X)
    assignment = upgma_clustering(similarity_matrix, k=3, agreggation_method='s')
            
    import numpy as np            
    print np.array([Xpos, assignment])
