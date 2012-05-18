
import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')

from cStringIO import StringIO
from numpy import array
from Bio import Phylo
import Bio
from Bio import Cluster
import numpy  

#from clustering.sim_matrix import *
#from clustering.sim_aggregation import *
#from clustering.kmedoids import  *
#from clustering import kmedoids
#def build_kmedoids_tree(similarity_matrix, kvec, similarity_aggregator=matrix_avg): 
    #similarity_matrix = [[0,3,2,4,5],[3,0,4,1,2],[2,4,0,5,1],[4,1,5,0,3],[5,2,1,3,0]]
        
#    leafs = range(len(similarity_matrix))
    
#    assignments = []
#    for k in kvec:
#        assignment = kmedoids_clustering(similarity_matrix, k, 10000)
#        assignments.append(assignment)
#        similarity_matrix = aggregate_similarity_matrix_a(similarity_matrix, assignment, similarity_aggregator)
        
#    leaf2clusters = {}
#    for leaf in leafs:
#        clusters = []
#        ix = leaf
#        for assignment in assignments:
#            clusters = clusters + [assignment[ix]]
#            ix = assignment[ix]
#        leaf2clusters[leaf] =  clusters
    
#    return leaf2clusters #dictionary {leaf-ix: list-of-clusters}

#########################################################################
#########################################################################
#########################################################################


def _dmatrix_to_list_of_pairs_(dmatrix):
    """zbudowanie slownika odleglosci [(v1,v2)->odleglosc] miedzy wierzcholkami na podstawie macierzy odleglosci"""
    rows = (dmatrix.shape)[0]
    dist = {}
    for r in range(0,rows):
        for c in range(0, r):
           dist[(r,c)] = dmatrix[r,c]
    return dist

def _build_u_(vertices, dist):
    """wylicza liste wartosci u na podstawie listy dostepnych wierzcholkow i slownika odleglosci miedzy wierzcholkami"""
    n = len(vertices)
    u = {}
    for v in vertices:
        u[v] = 0
        for d in dist.iterkeys():
            if (d[0]==v or d[1]==v):
                u[v] = u[v] + ( float(dist[d])/(n-2) )
    return u

def _choose_ij_(dist, u):
    """wybiera indeksy elementow do zlaczenia na podstawie slownika odleglosci i listy wartosci u"""
    for ij in dist.iterkeys(): break #zainicjuj para pierwsza z brzegu
    for km in dist.iterkeys():
        #print "_choose_ij_:", km, "->", dist[km] - u[km[0]] - u[km[1]]
        if ((dist[ij] - u[ij[0]] - u[ij[1]]) > (dist[km] - u[km[0]] - u[km[1]])):
            ij = km
    return ij

def _find_key_(dist, a,b):
    """znajduje i zwraca w slowniku dist indeksowanym parami klucz zawierajacy a i b"""
    for ab in dist.iterkeys():  
        if (ab[0]==a and ab[1]==b) or (ab[1]==a and ab[0]==b): break
    return ab

def nj(ids, dmatrix):    
    dmatrix = array(dmatrix)

    #slownik wezlow phylo tree
    pnodes = {} #inicjalizacja slownika wezlow lisciami
    for i in range(0, len(ids)):
        pnodes[i] = Bio.Phylo.BaseTree.Clade(name=ids[i], branch_length=1)

    #indeks wierzcholkow wewnetrznych
    hidden_node_id = 0

    #lista wierzcholkow uzywanych
    rows = (dmatrix.shape)[0]
    vertices = range(0,rows) 
    #print "vertices:", vertices

    #lisa kosztow
    dist = _dmatrix_to_list_of_pairs_(dmatrix)
    #print "dist:", dist 

    while len(vertices)>2 :
        #zbudowanie slownika u[wierzcholek] //krok1
        u = _build_u_(vertices, dist)
        #print "u:", u

        #wybranie i, j do zlaczenia:
        ij = _choose_ij_(dist, u)
        i = ij[0]
        j = ij[1]
        #print "ij:", ij

        #galezie:
        vi = 0.5*dist[ij] + 0.5*(u[i]-u[j])
        vj = 0.5*dist[ij] + 0.5*(u[j]-u[i])
        #print "vi=",vi," vj=", vj

        #aktualizacja odleglosci
        hidden_node_id = hidden_node_id - 1 #indeks kolejnego wezla ukrytego
        Dij = dist[ij]
        dist.pop(ij)        #usuniecie z kosztow
        vertices.remove(i)  #usuniecie z listy wierzcholkow
        vertices.remove(j)

        #dla kazdego z wierzcholkow uaktualnij odleglosci:
        for k in vertices:

            ik = _find_key_(dist, i, k) #wyszukaj Dik
            Dik = dist[ik]
            dist.pop(ik)
            
            jk = _find_key_(dist, j, k)   #wyszukaj Djk:
            Djk = dist[jk]
            dist.pop(jk)

            Dijk = (Dik + Djk - Dij)/2.0  #wylicz odleglosc od wierzcholka zlaczanego
            dist[(hidden_node_id, k)] = Dijk
        #print "dist':", dist

        #dodaj wierzcholek:
        vertices.append(hidden_node_id)
        pnodes[i].branch_length = vi
        pnodes[j].branch_length = vj
        #print "[i=",i,"]vi=", vi, " [j=",j,"]vj=", vj
        pnodes[hidden_node_id] = Bio.Phylo.BaseTree.Clade(branch_length=1, name="("+pnodes[i].name+","+pnodes[j].name+")", clades=[ pnodes[i], pnodes[j] ])
        #print "vertices':", vertices

    #zlacz ostatnie dwa wezly
    l = pnodes[vertices[0]]
    r = pnodes[vertices[1]]
    d = dist[_find_key_(dist, vertices[0], vertices[1])]
    l.branch_length = d/2.0
    r.branch_length = d/2.0
    root_clade = Bio.Phylo.BaseTree.Clade(branch_length=0, name="("+l.name+","+r.name+")", clades=[l, r])

    return Bio.Phylo.BaseTree.Tree(root=root_clade, rooted=True)

################################################################################################
################################################################################################
################################################################################################
################################################################################################


def upgma(ids, dmatrix, agreggation_method = 'a', anonclades = False):
    """Generuje drzewo typu Bio.Bhylo.BaseTree.Tree wykorzysujac Bio.Cluster.treecluster na podstawie listy identyfikatorow i macierzy odleglosci"""

    dmatrix = array(dmatrix)  
    tree = Bio.Cluster.treecluster(distancematrix = dmatrix, method = agreggation_method) #wyliczenie drzewa

    pnodes = {} #inicjalizacja slownika wezlow lisciami
    pheight = {} #slownik ktory dla danego nr wezla przechowuje jego wysokosc 
    for i in range(0, len(ids)):
        pnodes[i] = Bio.Phylo.BaseTree.Clade(name=ids[i])
        pheight[i] = 0

    hidden_node_ix = 0 #biezacy nr ukrytego wezla
    anonymous_node_counter = 0
    for node in tree:
        left_node = pnodes[node.left]
        right_node = pnodes[node.right]

        branch_distance = node.distance/2 #odleglosc od liscia lewego i prawego poddrzewa
        left_node.branch_length = branch_distance - pheight[node.left] #ustaw dlugosci galezi
        right_node.branch_length = branch_distance - pheight[node.right]

        hidden_node_ix = hidden_node_ix - 1 #dodaj wezel ukryty zlozony z dwoch juz istniejacych
        if anonclades:
            node_name = "a"+str(anonymous_node_counter) # ("("+left_node.name+","+right_node.name+")")
        else:
            node_name = ""
        anonymous_node_counter = anonymous_node_counter + 1
        pnodes[hidden_node_ix] = Bio.Phylo.BaseTree.Clade(name=node_name, clades=[left_node, right_node])
        pheight[hidden_node_ix] = branch_distance

    return Bio.Phylo.BaseTree.Tree(root=pnodes[hidden_node_ix], rooted=True)

################################################################################################
################################################################################################
################################################################################################
################################################################################################

def write_tree(tree, outTreePath):
    """Writes phylogenetic tree to all known formats."""
    #from Bio import Phylo
    #import Bio
    #Phylo.NewickIO.write([tree], open(outTreePath+"_plain.newick", "w"), plain=True)
    #Phylo.NewickIO.write([tree], open(outTreePath+".newick", "w"), plain=False)
    #Phylo.NexusIO.write([tree], open(outTreePath+".nexus", "w"))
    #Phylo.PhyloXMLIO.write([tree], open(outTreePath+"_indent.xml", "w"), indent=True)
    Phylo.PhyloXMLIO.write([tree], open(outTreePath+".xml", "w"), indent=False)

def phylotree2dicttree(phylotree):    
    def extract_subtree(clade, dict, anonymous_clade_counter):                             
        for subclade in clade.clades:
            key = subclade.name
            if len(key) <= 0:
                key = "x"+str(anonymous_clade_counter)
                anonymous_clade_counter = anonymous_clade_counter + 1
            dict[key] = {}
            extract_subtree(subclade, dict[key], anonymous_clade_counter)
    
    dicttree = {}
    anonymous_clade_counter = 0
    extract_subtree(phylotree.root, dicttree, anonymous_clade_counter)     
    return dicttree 

################################################################################################
################################################################################################
################################################################################################
################################################################################################


def build_sim_matrix_labels(distances, labels, label2ix_mapper = lambda label: label-1, defvalue = 1.0):
    #distances = [[0,3,2,4,5],[3,0,4,1,2],[2,4,0,5,1],[4,1,5,0,3],[5,2,1,3,0]]
    #labels = [[2,5],[3],[1,2],[3,4],[1,5]]
    #labels - list of lists
    #distances - distances matrix (list of lists)
    
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))    
    
    label2ix = dict( (label,label2ix_mapper(label)) for label in single_labels )
    ix2label = dict( (v,k) for k,v in label2ix.iteritems() )    
    
    single_ixs = list( label2ix.values() ) 
    num_ixs = max(single_ixs)+1
         
    label2sampleixs = {}
    for sampleix,ll in enumerate(labels):
        for l in ll:
          sampleixs = label2sampleixs.get(l,[])
          sampleixs.append(sampleix)
          label2sampleixs[l] = sampleixs
     
    labels_distances_matrix = [ [defvalue for col in xrange(num_ixs)] for rowix in xrange(num_ixs)]                     
    for ix1 in xrange(num_ixs):     
        try:   
            label1 = ix2label[ix1]
            sampleixs1 = label2sampleixs[label1]
            #print ix1,"->",sampleixs1
            for ix2 in xrange(num_ixs):
                try:
                    label2 = ix2label[ix2]
                    sampleixs2 = label2sampleixs[label2]
                                
                    total = 0.0
                    count = len(sampleixs1) * len(sampleixs2)
                    for sampleix1 in sampleixs1:
                        for sampleix2 in sampleixs2:
                            total = total +  distances[sampleix1][sampleix2]                                   
                    labels_distances_matrix[ix1][ix2] = float(total) / count
                except:
                    print "[build_sim_matrix_labels] skipping col:",ix2
        except:
            print "[build_sim_matrix_labels] skipping row:",ix1
            
    return labels_distances_matrix
            
            
def build_sim_matrix_labcount(pairlabel2dist, labels, default_dist = 10000, label2ix_mapper = lambda label: label-1):
    
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))    
    
    label2ix = dict( (label,label2ix_mapper(label)) for label in single_labels )
    ix2label = dict( (v,k) for k,v in label2ix.iteritems() )    
    
    single_ixs = list( label2ix.values() ) 
    num_ixs = max(single_ixs)+1
    
    labels_distances_matrix = [ [default_dist for col in xrange(num_ixs)] for rowix in xrange(num_ixs)]        
    for ix1 in xrange(num_ixs):    
        label1 = ix2label[ix1]    
        for ix2 in xrange(num_ixs):
            label2 = ix2label[ix2]            
            labels_distances_matrix[ix1][ix2] = pairlabel2dist.get((label1,label2), default_dist)                             
    return labels_distances_matrix
            
if __name__ == "__main__":
    dmatrix = [[0.0, 1.1, 2.3], [1.1, 0.0, 4.5], [2.3, 4.5, 0.0]]
    ids = ['a', 'b','c' ]
    print dmatrix
    phylo_tree = upgma(ids, dmatrix)
    print phylo_tree
    Phylo.draw_ascii(phylo_tree)
    write_tree(phylo_tree, "/tmp/tree")