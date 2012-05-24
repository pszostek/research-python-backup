"""Functions connected with representation of clusters as trees.

Two formats of trees are maintained:
1) list of lists of lists e.g. [[['l1','l2'],['l3']],[['l4'],['l5','l6','l7']]]
2) dictionary{leave: list of (top->down) clusters' number} e.g. {'l1':[0,1], 'l3':[0,2], 'l4':[1,2], ...} (cluster names at every level must be unique!)
"""
import formats
import collections
import math
import random

def build_msctree(mscleaves, msc2ix):
    """Reconstructs tree (representent as a list of lists of lists of... ints) out of msc-leaves (list of names e.g. '12A12','31D22',...).
        
    msc2ix = dictionary{msc-code:index}
    
    Sample:
    >>> build_msctree(['12A55', '12A66', '12B77', '12A88', '13C99', '12B76'], {'12A55': 0, '12A66': 1, '12A88': 3, '12B76': 5, '12B77': 2, '13C99': 4})
    [[[4]], [[0, 1, 3], [2, 5]]]
    """        
    clustdesc3 = formats._extract_clustdesc_(mscleaves, msc2ix, 0, 3)
        
    clustdesc2 = {}
    for prefix3, assigned_mscixs in clustdesc3.iteritems():
        prefix2 = prefix3[:2]
        clustdesc2[prefix2] = clustdesc2.get(prefix2, []) + [assigned_mscixs]
        
    return clustdesc2.values()
        
def gen_random_assignment(leaves, minpow = 0.25, maxpow = 0.75):
    import random_tree
    return random_tree.gen_random_assignment(leaves, minpow, maxpow)
        
def build_3level_tree(assignment_l, assignment_m, elementno2elementname = None):
    """Takes two lists (assignments to clusters) and returns tree (list of list of lists of ... ints).
    
    assignment_l - assignment of tree leaves (e.g. [0,0,1,0,2,1] means leaf0->cluster0, leaf1->cluster0, leaf2->cluster1, ..., leaf4->cluster2,...)
    assignment_m - assignment at second level of clustering
    elementno2elementname - dictionary{element no on the list: element name}
    Sample use:
    >>> build_3level_tree([0,0,1,0,2,1],[0,0,1])
    [[[0, 1, 3], [2, 5]], [[4]]]
    """    
    clustdesc_l = formats.assignment2clustdesc_converter(assignment_l, elementno2elementname)
    clustdesc_m = formats.assignment2clustdesc_converter(assignment_m, elementno2elementname)
    
    tree = []        
    for mcluster,m_lclusters in clustdesc_m.iteritems():        
        tree.append( [clustdesc_l[lcluster] for lcluster in m_lclusters if lcluster in clustdesc_l] )
        
    return tree
            

def extract_tree_leaves(tree):
    """Takes tree (list of lists of lists of ... basic-value) and returns list of leaves (basic-values).
    
    
    >>> sorted( extract_tree_leaves([[[0, 1, 3], [2, 5]], [[4]]]) ) == [0, 1, 2, 3, 4, 5]     
    True
    >>> sorted( extract_tree_leaves([[['a', 'b', 'd'], ['c', 'f']], [['e']]]) ) == ['a', 'b', 'c', 'd', 'e', 'f']
    True
    """
    def _extract_leaves_(e, result):
        try: #middle node
            for e_prim in e:
                _extract_leaves_(e_prim, result)
        except: #leave            
            result.append(e)
    leaves = []
    _extract_leaves_(tree, leaves)
    return leaves



def map_tree_leaves(tree, leave2leave):
    """Takes tree (list of lists of lists of ... basic-value) and changes names of leaves using leave2leave mapper.
    """
    def _walk_tree_(node):        
        if isinstance(node, collections.Iterable): #middle node            
            return [ _walk_tree_(subnode) for subnode in node ]
        else: #leave            
            return leave2leave[node]             
    return _walk_tree_(tree)
   
   
def bottomup2topdown_tree_converter(tree):
    """Takes tree described as list of lists of lists of ... of basic-values and returns dictionary{leaf: list-of-clusters-assigned-at-each-level}.
    
    Levels are listed from the highest to the lowest (H-M-L order).
    Indexes of clusters at every level are unique.
    Sample use:
    >>> bottomup2topdown_tree_converter([ [[0, 1, 3], [2, 5]], [[4]] ])
    {0: [0, 0], 1: [0, 0], 2: [0, 1], 3: [0, 0], 4: [1, 2], 5: [0, 1]}
    >>> bottomup2topdown_tree_converter([ [[0, 1, 3], [2, 5]], [4] ])
    {0: [0, 0], 1: [0, 0], 2: [0, 1], 3: [0, 0], 4: [1, 2], 5: [0, 1]}
    >>> bottomup2topdown_tree_converter([ [[[0, 1], 3], [2, 5]], [4] ])
    {0: [0, 0, 0], 1: [0, 0, 0], 2: [0, 1], 3: [0, 0], 4: [1], 5: [0, 1]}
    >>> sorted(list(bottomup2topdown_tree_converter([ [[['a','b'], ['c']] , [['d','e','f'],['g','h']]], [[['x']],[['y']]] ]).iteritems()))
    [('a', [0, 0, 0]), ('b', [0, 0, 0]), ('c', [0, 0, 1]), ('d', [0, 1, 2]), ('e', [0, 1, 2]), ('f', [0, 1, 2]), ('g', [0, 1, 3]), ('h', [0, 1, 3]), ('x', [1, 2, 4]), ('y', [1, 3, 5])]
    """
    level2clustercount = {}
    leaf2clusters = {}
    def _extract_levels_(e, levels_list):
        #print "levels_list=",levels_list," e=",e             
        if type(e) == list:
            level = len(levels_list)
            for e_prim in e:
                cluster_ix = level2clustercount.get(level,0) #ustal numer nowego klastra jako kolejny numer na tym poziomie
                level2clustercount[level] = level2clustercount.get(level, 0) + 1 #zlicz kolejny klaster na danym zaglebieniu
                _extract_levels_(e_prim, levels_list+[cluster_ix]) 
        else:
            leaf2clusters[e] = levels_list[0:len(levels_list)-1]
    _extract_levels_(tree, [])
    return leaf2clusters
    
        
def common_leaves(leaf2clusters_1, leaf2clusters_2):
    """Returns set of leaves common for both trees.
    
    Trees are given as dictionaries{leaf: list-of-descending-clusters}.    
    """        
    return set(leaf2clusters_1.keys()).intersection(set(leaf2clusters_2.keys()))

def trim(leaf2clusters, leaves):
    """Removes from tree branches with unknown leaves.
    
    Tree should be given as dictionary{leaf: list-of-descending-clusters}.
    leaves is a set of leaves' identifiers.
    
    Sample use:
    >>> leaf2clusters = {'a':[0],'b':[0],'c':[1],'c2':[1],'d':[1], 'e':[]}
    >>> leaves = ['a','b','c','d','e']
    >>> sorted(list(trim(leaf2clusters, leaves).iteritems()))
    [('a', [0]), ('b', [0]), ('c', [1]), ('d', [1]), ('e', [])]
    """
    leaves = set(leaves)
    for leaf in list(leaf2clusters):
        if not leaf in leaves:
            leaf2clusters.pop(leaf)
    return leaf2clusters 
    
            
def trim_common_leaves(leaf2clusters_1, leaf2clusters_2):            
    """Removes from trees branches with leaves that are not present in other tree.
    
    >>> leaf2clusters_1 = {'a':[0],'b':[0],'c':[1],'c2':[1],'d':[1], 'e':[]}
    >>> leaf2clusters_2 = {'a':[0],'b':[0], 'b2':[0], 'c':[1],'d':[1], 'e':[2]}
    >>> (l1,l2) = trim_common_leaves(leaf2clusters_1, leaf2clusters_2); sorted(list(l1.iteritems())),sorted(list(l2.iteritems()))
    ([('a', [0]), ('b', [0]), ('c', [1]), ('d', [1]), ('e', [])], [('a', [0]), ('b', [0]), ('c', [1]), ('d', [1]), ('e', [2])])
    """
    commonleaves = common_leaves(leaf2clusters_1, leaf2clusters_2)
    trim(leaf2clusters_1, commonleaves)
    trim(leaf2clusters_2, commonleaves)
    return (leaf2clusters_1, leaf2clusters_2)
    


def build_msctree_leaf2clusters(mscleaves, msc2ix):
    """Does the same as build_msctree but result is converted."""
    msc_tree = build_msctree(mscleaves, msc2ix)
    msc_leaf2clusters = bottomup2topdown_tree_converter(msc_tree)
    return msc_leaf2clusters,msc_tree 

def tree_depth(leaf2clusters):
    """Returns length of the longest path from root to leaves."""
    return max(len(c) for l,c in leaf2clusters.iteritems())+1

    
if __name__=="__main__":      
    import doctest
    doctest.testmod()      
    