'''
Created on Jan 18, 2012

@author: mlukasik
'''
from __future__ import division

import sys
sys.path.append(r'../')
#TODO: poradzic sobie z ponizszym, aby algorytm byl od tego niezalezny:
from data_io.zbl_record_generators import gen_record_filteredbyprefix
from tools.zbl_record_generators import map_frecords, extract_curr_level_labels

from tools.tree_dfs_builder import tree_dfs_builder
from tools.tree_dfs_explorer import tree_dfs_explorer

def PRINTER(x):
    #import logging
    #logging.info(x)
    print x
    #pass

class MlHierarchical(object):
    '''
    A hierarchical classifier, which is a tree of multi-label classifiers. 
    
    Since the classifiers are multi-label, the classifiers are in the parental nodes, indicating which child
    shall be traversed next (as opposed to the solution, where a binary classifier occupies each child node,
    indicating wether to traverse a node or not).
    
    '''

    def __init__(self, frecords, classifier, label_mappings, record_mappings, get_labels_of_record):
        '''
        Constructor.
        
        frecords - generator returning records.
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific frecords parameter
            
        classifier - constructor of a multi-label classifier, parametrized by frecords only.
        
        label_mappings - a list equal to depth of a classification tree that is to be constructed. consecutive elements are functions that
            map label into sub-label that is important in the current node-level
        
        record_mappings - a list equal to depth of a classification tree that is to be constructed. consecutive elements are functions that
            map record into sub-record (in terms of labels) that is important in the current node-level; mapping should be specified with child_id for
            additional filtering
            IMPORTANT: SHOULD NOT MODIFY RECORD INTERNALLY, BUT RETURN A NEW RECORD!
        '''
        #derivable fields:
        self.max_depth = len(label_mappings)-1
        self.get_labels_of_record = get_labels_of_record
        #Build the classification tree.
        PRINTER("[MlHierarchical: init]: start of training...")
        self.mltree = tree_dfs_builder(frecords, 
                                       lambda records, curr_depth, child_id: self.node_builder(records, curr_depth, child_id, classifier, record_mappings), 
                                       lambda records, curr_depth, child_id: self.children_splitter(records, curr_depth, child_id, label_mappings), self.max_depth, 0, '')#we start at depth 0
    
    #----------------------------CLASSIFYING----------------------------
    def classify(self, sample):
        '''
        Classify using the classification tree. Return list of labels.
        
        Note: the order of the resulting list is not significant.
        
        '''
        return tree_dfs_explorer(sample, self.mltree, self.max_depth, 0, self.stop_condition,
                      self.process_node, self.iterate_through_children, self.postprocess_result_data)
        #return reduce(lambda a, b: a+b, result)
    
    #----------------FOR TRAINING---------------#
    #----------------Functions needed to call tree_dfs_builder---------------#
    def node_builder(self, records, curr_depth, child_id, classifier, record_mappings):
        '''
        How to build a node on a given tree depth.
        
        Signature as required by tree_dfs_builder.
        
        '''
        PRINTER("[MlHierarchical:node_builder]: creating a root node on curr_depth: "+str(curr_depth)+" and child_id: "+str(child_id))
        curr_level_frecords = lambda: map_frecords(lambda: gen_record_filteredbyprefix(records, child_id), lambda rec: record_mappings[curr_depth](rec))
        return classifier(curr_level_frecords)
    
    def children_splitter(self, records, curr_depth, child_id, label_mappings):
        '''
        Split elements from records into buckets representing different labels.
        
        Signature as required by tree_dfs_builder.
        
        '''
        from collections import defaultdict
        children = defaultdict(lambda: [])
        for child in records():
            inserted_codes = set()#so that we do not inserted this record twice to the same bucket
            for code in map(label_mappings[curr_depth], self.get_labels_of_record(child)):#for each code of this record:
                if code.startswith(child_id) and code not in inserted_codes:
                    children[code].append(child)
                    inserted_codes.add(code)
        return dict(children)
    #----------------End of Functions needed to call tree_dfs_builder---------------#
    
    #----------------FOR CLASSIFYING---------------#
    #----------------Functions needed to call tree_dfs_explorer---------------#
    def stop_condition(self, result_data, input_data, curr_depth, max_depth):
        if not result_data or curr_depth == max_depth:
            PRINTER("[MlHierarchical: stop_condition]: either curr_labels is empty or curr_depth reached max:"+", "+str(curr_depth))
            return True
    def process_node(self, node, input_data, curr_depth):
        PRINTER("[MlHierarchical: process_node]: classifying on level: "+str(curr_depth))
        return node.content.classify(input_data)
    
    def iterate_through_children(self, node, result_data):
        for label in result_data:
            PRINTER("[MlHierarchical: iterate_through_children]: looking for classification as: "+str(label)+".")
            yield node.children[label]
    
    def postprocess_result_data(self, result):
        return reduce(lambda a, b: a+b, result)
    #----------------End of Functions needed to call tree_dfs_explorer---------------#