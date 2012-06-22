"""Converters and other tools connected with different formats of clusters/trees description.

Two formats of trees are maintained:
1) list of lists of lists e.g. [[['l1','l2'],['l3']],[['l4'],['l5','l6','l7']]]
2) dictionary{leave: list of (top->down) clusters' number} e.g. {'l1':[0,1], 'l3':[0,2], 'l4':[1,2], ...} (cluster names at every level must be unique!)
"""

from Bio import Phylo
import Bio
from Bio import Cluster
import numpy  

import Image, ImageDraw, ImageFont, ImageOps
import io
from Bio import Phylo
import Bio
import sys


def write_biotree(tree, outTreePath):
    """Writes phylogenetic tree to all known formats."""
    Phylo.NewickIO.write([tree], open(outTreePath+"_plain.newick", "w"), plain=True)
    Phylo.NewickIO.write([tree], open(outTreePath+".newick", "w"), plain=False)
    Phylo.NexusIO.write([tree], open(outTreePath+".nexus", "w"))
    Phylo.PhyloXMLIO.write([tree], open(outTreePath+"_indent.xml", "w"), indent=True)
    Phylo.PhyloXMLIO.write([tree], open(outTreePath+".xml", "w"), indent=False)


def tree2biotree_converter(tree):
    """Takes tree represented as list of list and returns Bio.Python tree."""    
    def build_tree(children):
        #print "Entering children=",str(children)
        if not type(children) == list:
            return Bio.Phylo.BaseTree.Clade(name=str(children), clades=[])        
        children_clades = list( build_tree(child) for child in children )        
        return Bio.Phylo.BaseTree.Clade(name="", clades=children_clades)
    return Bio.Phylo.BaseTree.Tree(root=build_tree(tree), rooted=True) 


def msctree2biotree_converter(tree):
    """Takes tree represented as list of list and returns Bio.Python tree."""    
    def build_tree(children):
        #print "Entering children=",str(children)
        if not type(children) == list:
            return Bio.Phylo.BaseTree.Clade(name=str(children), clades=[])        
        children_clades = list( build_tree(child) for child in children )        
        return Bio.Phylo.BaseTree.Clade(name="", clades=children_clades)
    return Bio.Phylo.BaseTree.Tree(root=build_tree(tree), rooted=True) 



def assignment2clustdesc_converter(assignment, elementno2elementname = None):
    """Takes list of cluster-assignments and returns dictionary{assigned-cluster: list-of-elements-ixs-that-have-this-cluster-assigned}."""
    if elementno2elementname is None: #naive translation of names of elements
        elementno2elementname = dict((ix,ix) for ix,clust in enumerate(assignment))
    
    clustdesc = {}
    for element_no, cluster_name in enumerate(assignment):
        clustdesc[cluster_name] = clustdesc.get(cluster_name, []) + [ elementno2elementname[element_no] ]
    return clustdesc


def _extract_clustdesc_(mscleaves, msc2ix, cname_pos_start, cname_pos_end):
    """Takes list of msc-codes and returns dictionary{assigned-cluster: list-of-elements-ixs-that-have-this-cluster-assigned}.
    
    
    msc2ix - dictionary{msc-code:index}
    assigned-cluster = msc-code-name[cname_pos_start: cname_pos_end] //extract cluster name from MSC code
    """
    clustdesc = {}
    for msc in mscleaves:
        cluster_name = msc[cname_pos_start: cname_pos_end]        
        clustdesc[cluster_name] = clustdesc.get(cluster_name, []) + [msc2ix[msc]]
    return clustdesc

def gen_msc2ix(mscleaves):
    """Takes list of msc-codes and returns dictionary{msc-code: index}."""    
    return dict( (code,i) for i,code in enumerate(sorted(mscleaves)) )

    
    


if __name__=="__main__":
      
    import doctest
    doctest.testmod()  
    