"""Reads information about clusters from many sources and aggregates it to single output."""

#Skrypt bierze informacje o podziale na klastry 
#i na tej podstawie generuje plik zawierajacy zagregowana informacje o klastrach.

import Image, ImageDraw, ImageFont, ImageOps
import operator, math
import data.io, calc.processing, calc.maths
import sys, os
from munkres import Munkres
from time import strftime

#############################################################################
########### GENERATE COSTS MATRIX FOR LABEL ASSIGNMENT TO CLUSTERS ##########
#############################################################################

def calc_assignment_cost(labels_in_cluster, clust_label):
    """Returns cost (no of bad labels) of assigning label clust_label to cluster where elements have labels.

    Sample use:
    >>> calc_assignment_cost(['abc', 'bad', 'abe', 'baf', 'xxz'], 'ab')
    3
    """
    prefix_len = len(clust_label)    
    return sum(1 for l in labels_in_cluster if not l[0:prefix_len] == clust_label)

    
def calc_assignment_cost_vector(labels_in_cluster, clusts_labels):
    """Returns vector of costs (no of bad labels) of assigning labels from clust_labels to cluster where elements have labels.
    
    Sample use:
    >>> calc_assignment_cost_vector(['abc', 'bad', 'abe', 'baf', 'xxz'], ['ab', 'ba', 'xx'])
    [3, 3, 4]
    """    
    return [calc_assignment_cost(labels_in_cluster, clust_label) for clust_label in clusts_labels]


def gen_assignment_cost_matrix(assignment, labels, clusters, clusts_labels):
    """Generates matrix of costs for different assignment of labels from clusts_labels to clusters (described by assignment vector).

    Sample use:
    >>> gen_assignment_cost_matrix([0, 100, 100, 0, 22], ['abc', 'bad', 'abe', 'baf', 'xxz'], [0, 100, 22], ['ab', 'ba', 'xx'])
    [[1, 1, 2], [1, 1, 2], [1, 1, 0]]
    """
    m = []
    for cluster_no in clusters: #row = cluster
        ixs                 = calc.processing.find_ixs_of_val(assignment, cluster_no)
        labels_in_cluster   = calc.processing.get_elements_of_ixs(labels, ixs)
        cost_row            = calc_assignment_cost_vector(labels_in_cluster, clusts_labels)
        m.append(cost_row)
    return m    




#############################################################################
########### GENERATE CLUSTERS' DESCRIPTOR STRUCTURE #########################
#############################################################################

def __assign_labels_to_clusters__(assignment, labels, clusters, clusts_labels):
    cost_matrix             = gen_assignment_cost_matrix(assignment, labels, clusters, clusts_labels)
    munkres                 = Munkres()
    assignment_list = munkres.compute(cost_matrix);
    #assignment_list = [(i,i) for i in xrange(len(clusters))] #for debugging
    assigned_clusts_labels  = dict(assignment_list) #dictionary {cluster_no: assigned_label_no}
    return assigned_clusts_labels

def __gen_clust_desc_hungarian__(assignment, labels, prefix_len):
    print "Labels assigning method: hungarian"
    clusters                = list(set(assignment))
    clusts_labels           = list(calc.processing.get_prefixes(labels, prefix_len)) #all possible labels of clusters = prefixes of elements' labels
    assigned_clusts_labels  = __assign_labels_to_clusters__(assignment, labels, clusters, clusts_labels)

    clustdesc           = [] 
    for cluster_ix in xrange(len(clusters)):
        cluster_ixs     = calc.processing.find_ixs_of_val(assignment, clusters[cluster_ix]) #ixs of elements in the cluster
        cluster_label   = clusts_labels[assigned_clusts_labels[cluster_ix]] #cluster's name
        clustdesc.append( (cluster_label, cluster_ixs) )        

    return clustdesc


def __gen_clust_desc_majority__(assignment, labels, prefix_len):
    print "Labels assigning method: majority"
    clusters                = list(set(assignment))
    clustdesc           = [] 
    for cluster_ix in xrange(len(clusters)):
        cluster_ixs     = calc.processing.find_ixs_of_val(assignment, clusters[cluster_ix]) #ixs of elements in the cluster
        lbls            = calc.processing.get_elements_of_ixs(labels, cluster_ixs) #labels of selected indexes
        count           = calc.processing.count_unique_prefixes(lbls, prefix_len) #count prefixes in labels
        max_lbl         = max(count.iteritems(), key=operator.itemgetter(1)) #touple: (most popular label, its count)
        cluster_label   = max_lbl[0]
        clustdesc.append( (cluster_label, cluster_ixs) )        

    return clustdesc


def gen_clust_desc(assignment, labels, prefix_len, method = 'hungarian'):
    """On input: assignment of elements to clusters, labels of clusters' elements, what size prefixes should be used to label clusters. """
    """Output clusters information: list of pairs: (cluster label, list of indexes of assigned elements)"""
    if method == 'hungarian':
        return __gen_clust_desc_hungarian__(assignment, labels, prefix_len)
    else:
        return __gen_clust_desc_majority__(assignment, labels, prefix_len)


#############################################################################
# EXECUTE SCRIPT: READ ASSIGNMENT AND LABELS AND STORE IN SINGLE FILE########
#############################################################################

if __name__ == "__main__":

    import doctest
    doctest.testmod()

    args = sys.argv
    if len(sys.argv) != 3:
        print "[ERROR] Exactly two arguments are expected: input-matrix-path labels'-prefix-length"
        exit(-1)
    simMatrixPath   = args[1] 
    prefix_len      = int(args[2])                                                              #length of prefix used for clusters' etiquettes generating

    name            = os.path.basename(simMatrixPath).split('.')[0]                             #file path base name
    assignmentPath  = '/tmp/tr_' + name + '_assignment_' + str(prefix_len) + '.vector'          #assignment of elements to clusters
    labelsPath      = '/tmp/tr_' + name + '_labels_' + str(prefix_len) + '.svector'             #etiguettes of elements

    outClustPath    = '/tmp/tr_' + name + '_clustdesc_' + str(prefix_len) + '.txt'              #file to put aggregated information about clusters (etiquette + list of indexes)
                         
    labeling_method =  'majority'#'hungarian'


    #reading:
    assignment      = data.io.fread_ivector(assignmentPath) 
    labels          = data.io.fread_svector(labelsPath)
    print "Read assignment of", len(assignment), "elements (",len(labels),"labels ) to", len(set(assignment)),"clusters..."

    #generate cluster information
    clustdesc = gen_clust_desc(assignment, labels, prefix_len, labeling_method)

    #saving results to file:
    print "Writing clusters' descriptor to", outClustPath
    data.io.fwrite_clusters(clustdesc, outClustPath)
