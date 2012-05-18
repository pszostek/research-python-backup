"""Reads two-level clustering results and generates phylogenetic trees."""

import Image, ImageDraw, ImageFont, ImageOps
import io
from Bio import Phylo
import Bio
import sys


def write_tree(tree, outTreePath):
    """Writes phylogenetic tree to all known formats."""
    Phylo.NewickIO.write([tree], open(outTreePath+"_plain.newick", "w"), plain=True)
    Phylo.NewickIO.write([tree], open(outTreePath+".newick", "w"), plain=False)
    Phylo.NexusIO.write([tree], open(outTreePath+".nexus", "w"))
    Phylo.PhyloXMLIO.write([tree], open(outTreePath+"_indent.xml", "w"), indent=True)
    Phylo.PhyloXMLIO.write([tree], open(outTreePath+".xml", "w"), indent=False)

def build_phylo_tree(labels, clustdesc1, clustdesc2, root_name):
    """Builds phylogenetic tree.        
       Input: 
            labels - names of leaves
            clustdesc1 - first-level clustering: dictionary {cluster's label: assigned indexes}
            clustdesc2 - second-level clustering: dictionary {cluster's label: assigned indexes}
            root_name - how to call root node"""
    root = Bio.Phylo.BaseTree.Clade(name = root_name)
    for cluster2 in clustdesc2: 
        node2 = Bio.Phylo.BaseTree.Clade(name = cluster2[0]) #name in format XX
        for cluster1Ix in cluster2[1]: #for every classified as a part of XX
            cluster1 = clustdesc1[cluster1Ix]
            node1 = Bio.Phylo.BaseTree.Clade(name = cluster1[0]) #name in format XXY
            for cluster0Ix in cluster1[1]: #for every classified as a part of XXY
                node0 = Bio.Phylo.BaseTree.Clade(name = labels[cluster0Ix]) #name in format XXYZZ
                node1.clades.append(node0)
            node2.clades.append(node1)
        root.clades.append(node2)
    tree = Bio.Phylo.BaseTree.Tree(root, rooted=True)
    return tree

def build_phylo_tree_leaves_merged(labels, clustdesc1, clustdesc2, root_name):
    """Builds phylogenetic tree but leaves are merged into single node. Further information in help for build_phylo_tree function."""
    root = Bio.Phylo.BaseTree.Clade(name = root_name)
    for cluster2 in clustdesc2: 
        node2 = Bio.Phylo.BaseTree.Clade(name = cluster2[0]) #name in format XX
        for cluster1Ix in cluster2[1]: #for every classified as a part of XX
            cluster1 = clustdesc1[cluster1Ix]
            node1 = Bio.Phylo.BaseTree.Clade(name = cluster1[0]) #name in format XXY
            node0str = ""
            for cluster0Ix in cluster1[1]: #for every classified as a part of XXY
                node0str = node0str + " " + labels[cluster0Ix] #name in format XXYZZ
            node0 = Bio.Phylo.BaseTree.Clade(name = node0str) #name in format (XXYZZ, XXYZZ, ..., XXYZZ)
            node1.clades.append(node0)
            node2.clades.append(node1)
        root.clades.append(node2)
    tree2 = Bio.Phylo.BaseTree.Tree(root, rooted=True)
    return tree2


if __name__ == "__main__":

    args = sys.argv
    if len(sys.argv) != 5:
        print "[ERROR] Exactly four arguments are expected: labels-path clusters-level1-description-path clusters-level2-description-path output-tree-path" 
        print "[ERROR] sample args: rand_cof/tr_rand_cof_labels_3.svector rand_cof/tr_rand_cof_clustdesc_3.txt rand_cof/tr_rand_cof_2_clustdesc_2.txt rand_cof/trees/tree_rand_cof_"
        exit(-1)

    labelsPath      = args[1]       #etiguettes of elements (0 level)
    clust1Path      = args[2]       #file to put aggregated information about clusters (etiquette + list of indexes) (1st level)
    clust2Path      = args[3]       #file to put aggregated information about clusters (etiquette + list of indexes) (2nd level)
    outTreePath     = args[4]       #prefix of output path

    labels          = io.fread_svector(labelsPath)  # labels of the lowest level
    clustdesc1      = io.fread_clusters(clust1Path) # clustering
    clustdesc2      = io.fread_clusters(clust2Path) # clustering

    tree = build_phylo_tree(labels, clustdesc1, clustdesc2, root_name = "MSC")
    tree2 =  build_phylo_tree_leaves_merged(labels, clustdesc1, clustdesc2, root_name = "MSC")


    write_tree(tree, outTreePath);
    write_tree(tree2, outTreePath+"_merged")
