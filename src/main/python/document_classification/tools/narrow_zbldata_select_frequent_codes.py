'''
Created on Jan 2, 2012

@author: mlukasik

Script allowing to create a smaller dataset out of a large SPRINGER data.
It does the task by leaving only the codes that are frequent in the dataset 
(at least as many occurences as specified by user).
'''
from __future__ import division
import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import gen_record, gen_record_prefixed, gen_lmc, gen_record_fromshifts, gen_record_filteredbylabels
from tools.msc_processing import get_labels_counts, get_labelperdocuments_counts
from data_io.zbl_io import write_zbl_records

def PRINTER(x):
    print '[narrow_zbldata_select_frequent_codes]: ', x

def filter_rare_labels(labels_tree, min_occurences, levels_wanted):
    '''
    Filter out rare codes (those that have less children than min_occurences).
    '''
    #PRINTER('[filter_by_divisability] level: '+str(levels_wanted)+" labels_tree: "+str(labels_tree))
    to_del = []
    for label in labels_tree.iterkeys():
        if levels_wanted>0:
            filter_rare_labels(labels_tree[label], min_occurences, levels_wanted-1)
            if len(labels_tree[label]) < min_occurences:
                #PRINTER('[filter_by_divisability] adding to del: '+label+" "+str(len(labels_tree[label]))
                #        +" "+str(min_occurences))
                to_del.append(label)
    
    #PRINTER('[filter_by_divisability] to_del: '+str(to_del))
    for label in to_del:
        labels_tree.pop(label)

def get_tree_leaves(labels_tree, levels_wanted):
    '''
    Moves down the tree to return the list of leaves eventually.
    '''  
    if levels_wanted==0:
        return list(labels_tree.iterkeys())
    result = []
    for subtree in labels_tree.itervalues():
        result = result+get_tree_leaves(subtree, levels_wanted-1)
    return result
        
def build_label_tree(labels, label_mappings):
    '''
    Build a label tree.
    '''
    labels_tree = {}
    curr_node = labels_tree
    for label in labels:
        for label_mapping in label_mappings:
            if label_mapping(label) not in curr_node:
                curr_node[label_mapping(label)] = {}
            curr_node = curr_node[label_mapping(label)]
        if label not in curr_node:
            curr_node[label] = {}
        curr_node = labels_tree
    return labels_tree
        
def filter_by_divisability(labels, min_occurences, levels_wanted):
    '''
    Returns a list of labels, filtering out codes that have less min_occurences children.
    
    This is performed by:
    1 - building a tree of codes
    2- recursively going down this tree, and when coming back, deleting nodes that have less than 2 children
        (performed by filter_rare_labels which is a recursive function)
    3 - going back to the list by joining the leaves of a tree that haven't been deleted 
        (performed by get_tree_leaves, which is a recursive function)
    '''
    label_mappings = [lambda x: x[:2], lambda x: x[:3]][:levels_wanted]
    
    #build a label tree
    labels_tree = build_label_tree(labels, label_mappings)
    #PRINTER('[filter_by_divisability] labels_tree: '+str(labels_tree))
    
    #filter a tree:
    filter_rare_labels(labels_tree, min_occurences, levels_wanted)
    PRINTER('[filter_by_divisability] labels_tree: '+str(labels_tree))
    
    #make a list from the tree-leaves:
    return get_tree_leaves(labels_tree, levels_wanted)

if __name__ == '__main__':
    fname = sys.argv[1]
    savefname = sys.argv[2]
    levels_wanted = int(sys.argv[3])
    mincodeoccurences = int(sys.argv[4])
    biggest_labels_cnt = int(sys.argv[5])
    filtered_by = sys.argv[6:]
    
    PRINTER("Input arguments:")
    PRINTER("fname: "+str(fname))
    PRINTER("savefname: "+str(savefname))
    PRINTER("levels_wanted: "+str(levels_wanted))
    PRINTER("mincodeoccurences"+str(mincodeoccurences))
    PRINTER("biggest_labels_cnt"+str(biggest_labels_cnt))
    PRINTER("filtered_by:"+str(filtered_by))
    
    codeprefixlen = 5
    if levels_wanted==2:
        codeprefixlen = 3
    elif levels_wanted==1:
        codeprefixlen = 2
    
    #prepare generators
    rec_generator = lambda: gen_record(fname, filtered_by)
    
    prefixed_rec_generator = lambda: gen_record_prefixed(rec_generator, codeprefixlen)
    prefix_code_generator = lambda: gen_lmc(prefixed_rec_generator)
    
    #generate labels
    PRINTER("Generating labels...")
    labels_counts = get_labels_counts(prefix_code_generator, mincodeoccurences)
    #PRINTER("labels generated."
    #PRINTER(sorted(labels_counts, key = lambda x: x[1], reverse = True)
    biggest_labels = map(lambda x: x[0], sorted(labels_counts, key = lambda x: x[1], 
                                                reverse = True))
    
    biggest_labels = filter_by_divisability(biggest_labels, 2, levels_wanted-1)
    
    PRINTER("Labels after filtering by divisability: "+str(biggest_labels))
    PRINTER("Number of labels: "+str(len(biggest_labels)))
    
    biggest_labels = biggest_labels[:biggest_labels_cnt]
    
    PRINTER("Labels after cutting only frequent labels: "+str(biggest_labels))
    PRINTER("Number of labels: "+str(len(biggest_labels)))
    
    labelsset = set(biggest_labels)
    PRINTER(biggest_labels)
    
    #gen filtered records:
    prefix_code_generator = lambda: gen_record_filteredbylabels(prefixed_rec_generator, labelsset)
    PRINTER("counting elements...")
    elements_count = len(list(prefix_code_generator()))
    PRINTER("number of elements:"+str(elements_count))
    
    
    codes_generator = lambda: gen_lmc(prefix_code_generator)
    labelperdocuments_counts = get_labelperdocuments_counts(codes_generator)
    PRINTER("labels per document statistics:"+str(labelperdocuments_counts))
    
    l = list(labelperdocuments_counts.iteritems())
    PRINTER("average number of labels per document:"+str(sum(le[0]*le[1] for le in l)/sum(le[1] for le in l)))
    
    PRINTER("saving...")
    write_zbl_records(open(savefname, 'w'), prefix_code_generator())