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
    #logging.info('[MlHierarchical]'+x)
    #print '[MlHierarchical]'+x
    pass

class MlHierarchical(object):
    '''
    A hierarchical classifier, which is a tree of multi-label classifiers. 
    
    Since the classifiers are multi-label, the classifiers are in the parental nodes, indicating which child
    shall be traversed next (as opposed to the solution, where a binary classifier occupies each child node,
    indicating wether to traverse a node or not).
    
    '''

    def __init__(self, frecords, classifier, label_mappings, get_labels_of_record):
        '''
        Constructor.
        
        frecords - generator returning records.
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific frecords parameter
            
        classifier - constructor of a multi-label classifier, parametrized by frecords and get_labels_of_record only.
        
        label_mappings - a list equal to depth of a classification tree that is to be constructed. consecutive elements are functions that
            map label into sub-label that is important in the current node-level
            
        get_labels_of_record - returns a list of labels of the record
        '''
        #derivable fields:
        self.max_depth = len(label_mappings)-1
        self.get_labels_of_record = get_labels_of_record
        #Build the classification tree.
        PRINTER("[init]: start of training...")
        self.mltree = tree_dfs_builder(frecords, 
                                       lambda records, curr_depth, child_id: self.node_builder(records, curr_depth, child_id, classifier, label_mappings, get_labels_of_record), 
                                       lambda records, curr_depth, child_id: self.children_splitter(records, curr_depth, child_id, label_mappings, get_labels_of_record), 
                                       self.max_depth, 0, '', lambda x: True)#we start at depth 0
    
    #----------------------------CLASSIFYING----------------------------
    def classify(self, sample):
        '''
        Classify using the classification tree. Return list of labels.
        
        Note: the order of the resulting list is not significant.
        
        '''
        return tree_dfs_explorer(sample, self.mltree, self.max_depth, 0, self.stop_condition,
                      self.process_node, self.go_downwards, self.postprocess_result_data)
        #return reduce(lambda a, b: a+b, result)
    
    #----------------FOR TRAINING---------------#
    #----------------Functions needed to call tree_dfs_builder---------------#
    def get_labels_of_record_nested(self, x, curr_depth, child_id, classifier, label_mappings, get_labels_of_record): 
        result = []
        #print '[get_labels_of_record_nested]: codes:', map(label_mappings[curr_depth], get_labels_of_record(x))
        for code in get_labels_of_record(x):
            #print '[get_labels_of_record_nested]: code, child_id, label_mappings[curr_depth](code):',  code, child_id, label_mappings[curr_depth](code)
            #print '[get_labels_of_record_nested]: curr_depth==0 or label_mappings[curr_depth-1](code)',  curr_depth==0, label_mappings[curr_depth-1](code)
            if curr_depth==0 or label_mappings[curr_depth-1](code) == child_id:
                #print '[get_labels_of_record_nested]: appending'
                result.append(label_mappings[curr_depth](code))
        return result
    
    def node_builder(self, records, curr_depth, child_id, classifier, label_mappings, get_labels_of_record):
        '''
        How to build a node on a given tree depth.
        
        Signature as required by tree_dfs_builder.
        
        '''
        PRINTER("[node_builder]: creating a root node on curr_depth: "+str(curr_depth)+" and child_id: "+str(child_id))
        #curr_level_frecords = lambda: map_frecords(lambda: gen_record_filteredbyprefix(records, child_id), lambda rec: record_mappings[curr_depth](rec))
        
        #PRINTER("[node_builder]: records: "+str(records()))
        return classifier(records, lambda x: self.get_labels_of_record_nested(x, curr_depth, child_id, classifier, label_mappings, get_labels_of_record))
    
    def children_splitter(self, records, curr_depth, child_id, label_mappings, get_labels_of_record):
        '''
        Split elements from records into buckets representing different labels.
        
        Signature as required by tree_dfs_builder.
        
        '''
        from collections import defaultdict
        children = defaultdict(lambda: [])
        for child in records:
            inserted_codes = set()#so that we do not inserted same record twice to the same bucket
            #print '[children_splitter] record:', child, ' child_id:', child_id, 'curr_depth:', curr_depth
            for code in get_labels_of_record(child):#for each code of this record:
                #print '[children_splitter] code:', code, ' label_mappings[curr_depth-1](code):', label_mappings[curr_depth-1](code)
                #ten kod musi byc podkategoria child_id
                if curr_depth == 0 or label_mappings[curr_depth-1](code) == child_id:
                    #nie wstawiamy rekordu 2 razy do tego samego kubelka:
                    descendant_code = label_mappings[curr_depth](code)
                    if descendant_code not in inserted_codes:
                        #print '[children_splitter] wstawiamy:', descendant_code
                        children[descendant_code].append(child)
                        inserted_codes.add(descendant_code)
        return dict(children)
    #----------------End of Functions needed to call tree_dfs_builder---------------#
    
    #----------------FOR CLASSIFYING---------------#
    #----------------Functions needed to call tree_dfs_explorer---------------#
    def stop_condition(self, result_data, input_data, curr_depth, max_depth):
        if not result_data or curr_depth == max_depth:
            PRINTER("[stop_condition]: either curr_labels is empty or curr_depth reached max:"+", "+str(curr_depth))
            return True
    def process_node(self, node, input_data, curr_depth):
        PRINTER("[process_node]: classifying on level: "+str(curr_depth))
        return node.content.classify(input_data)
    
    #def iterate_through_children(self, node, result_data):
    #    for label in result_data:
    #        PRINTER("[iterate_through_children]: looking for classification as: "+str(label)+".")
    #        yield node.children[label]
    
    def go_downwards(self, node, result_datum):
        PRINTER("[go_downwards]:: looking for classification as: "+str(result_datum)+".")
        return node.children[result_datum]
    
    def postprocess_result_data(self, result):
        return reduce(lambda a, b: a+b, result)
    #----------------End of Functions needed to call tree_dfs_explorer---------------#