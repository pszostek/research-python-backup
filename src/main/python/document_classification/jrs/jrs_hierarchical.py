'''
Created on Jan 18, 2012

@author: mlukasik
'''
from __future__ import division

import sys
sys.path.append(r'../')
from tools.tree_dfs_builder import tree_dfs_builder
from tools.tree_dfs_explorer import tree_dfs_explorer

def PRINTER(x):
    #import logging
    #logging.info(x)
    #print x
    pass

class JrsMlHierarchical(object):
    '''
    A hierarchical classifier, which is a tree of multi-label classifiers. 
    
    Since the classifiers are multi-label, the classifiers are in the parental nodes, indicating which child
    shall be traversed next (as opposed to the solution, where a binary classifier occupies each child node,
    indicating wether to traverse a node or not).
    
    '''

    def __init__(self, records, train_labels, classifier, label_mappings, continue_deepening, is_leaf_node):
        '''
        Constructor.
        
        records -records list.
        
        train_labels - consecutive labels, for each record
        
        classifier - constructor of a multi-label classifier, parametrized by records, train_labels and list_of_all_labels.
        
        label_mappings - a list equal to depth of a classification tree that is to be constructed. consecutive elements are functions that
            map label into sub-label that is important in the current node-level
        
        continue_deepening - returns a boolean value, wether a given node has at least one non-leaf chid
        
        is_leaf_node - returns a boolean value indicating wether a node is a leaf
        '''
        #derivable fields:
        self.max_depth = len(label_mappings)-1
        #Build the classification tree.
        PRINTER("[MlHierarchical: init]: start of training...")
        self.continue_deepening = continue_deepening#wether to continue deepening from a child_id
        self.is_leaf_node = is_leaf_node
        self.mltree = tree_dfs_builder(records, 
                                       lambda records, curr_depth, child_id: self.node_builder(records, curr_depth, child_id, classifier, label_mappings, train_labels), 
                                       lambda records, curr_depth, child_id: self.children_splitter(records, curr_depth, child_id, label_mappings, train_labels), self.max_depth, 0, 'START_NODE', self.continue_deepening)#we start at depth 0
    
    #----------------------------CLASSIFYING----------------------------
    def classify(self, sample):
        '''
        Classify using the classification tree. Return list of labels.
        
        Note: the order of the resulting list is not significant.
        
        '''
        return tree_dfs_explorer(sample, self.mltree, self.max_depth, 0, 
                    lambda result_data, input_data, curr_depth, max_depth: self.stop_condition(result_data, input_data, curr_depth, max_depth, self.is_leaf_node),
                    self.process_node, self.go_downwards, self.postprocess_result_data)
        #return reduce(lambda a, b: a+b, result)
    
    #----------------FOR TRAINING---------------#
    #----------------Functions needed to call tree_dfs_builder---------------#
    def node_builder(self, records, curr_depth, child_id, classifier, label_mappings, train_labels):
        '''
        How to build a node on a given tree depth.
        
        Signature as required by tree_dfs_builder.
        
        train_labels - the TOP LEVEL training labels
        
        '''
        #PRINTER("[MlHierarchical:node_builder]: creating a root node on curr_depth: "+str(curr_depth)+
        #        " and child_id: "+str(child_id)+" records:"+str(records())+" labels:"+str(train_labels))
        #curr_level_frecords = lambda: map_frecords(lambda: gen_record_filteredbyprefix(records, child_id), lambda rec: record_mappings[curr_depth](rec))
        
        #map train_labels to the current-level labels
        curr_labels = []
        list_of_all_labels = set() #set of current level labels
        for ind in xrange(len(train_labels)):
            curr_labels.append([])
        
        for ind in records():
            for label in train_labels[ind]:
                #if this is the first level or further level and at the same time is a child of child_id
                #print "label_mappings[curr_depth-1](label), child_id:", label_mappings[curr_depth-1](label), child_id
                if (curr_depth > 0 and label_mappings[curr_depth-1](label) == child_id) or curr_depth==0:
                    curr_labels[ind].append(label_mappings[curr_depth](label))
                    list_of_all_labels.add(label_mappings[curr_depth](label))
        #TODO: tutaj definiujemy funkcje labels_mapper
        #PRINTER("[MlHierarchical:node_builder]: passing argument to a classifier constructor: records, curr_labels: "
        #        +str(records())+" ,"+str(curr_labels)+" from child_id: "+str(child_id))
        return classifier(records(), curr_labels, list_of_all_labels)
    
    def children_splitter(self, records, curr_depth, child_id, label_mappings, train_labels):
        '''
        Split elements from records into buckets representing different labels.
        
        Signature as required by tree_dfs_builder.
        
        train_labels - the TOP LEVEL training labels
        '''
        PRINTER("[MlHierarchical:children_splitter]: Splitting records amongst the children at depth: "+str(curr_depth)+" and child_id: "+str(child_id))
        
        from collections import defaultdict
        children = defaultdict(lambda: [])
        for child in records():
            inserted_codes = set()#so that we do not inserted this record twice to the same bucket
            for code in train_labels[child]: #in map(label_mappings[curr_depth], self.label_extractor(child)):#for each code of this record:
                #print "[children_splitter] label_mappings[curr_depth-1](label), child_id, code:", label_mappings[curr_depth-1](code), child_id, label_mappings[curr_depth-1](code) == child_id, code
                if (curr_depth > 0 and label_mappings[curr_depth-1](code) == child_id) or curr_depth==0:
                    mapped_code = label_mappings[curr_depth](code)
                    #PRINTER("[MlHierarchical:children_splitter]: code, curr_depth, mapped_code: "+
                    #        str(code)+" "+str(curr_depth)+" "+str(mapped_code))
                    #print "mapped_code: ", mapped_code
                    if mapped_code not in inserted_codes:
                        #print "PASSED"
                        children[mapped_code].append(child)
                        inserted_codes.add(mapped_code)
        PRINTER("[MlHierarchical:children_splitter]: Got children splitting: "+str(list(children.iterkeys())    )+" out of child_id: "+str(child_id))
        return dict(children)
    #----------------End of Functions needed to call tree_dfs_builder---------------#
    
    #----------------FOR CLASSIFYING---------------#
    #----------------Functions needed to call tree_dfs_explorer---------------#
    def stop_condition(self, result_data, input_data, curr_depth, max_depth, is_leaf_node):
        if not result_data or curr_depth == max_depth or is_leaf_node(result_data):
            #PRINTER("[MlHierarchical: stop_condition]: either curr_labels is empty or curr_depth reached max:"+", "+str(curr_depth))
            return True
        return False
    def process_node(self, node, input_data, curr_depth):
        #PRINTER("[MlHierarchical: process_node]: classifying on level: "+str(curr_depth))
        return node.content.classify(input_data)
    
    def go_downwards(self, node, result_datum):
        PRINTER("[MlHierarchical: iterate_through_children]: looking for classification as: "+str(result_datum)+".")
        return node.children[result_datum]
    
    def postprocess_result_data(self, result):
        return reduce(lambda a, b: a+b, result)
    #----------------End of Functions needed to call tree_dfs_explorer---------------#