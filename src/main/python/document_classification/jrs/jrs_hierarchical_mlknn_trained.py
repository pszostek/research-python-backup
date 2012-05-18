'''
Created on Mar 19, 2012

@author: mlukasik
'''
from __future__ import division
from jrs_mlknn_adapted import MlKnnJrs

import sys
sys.path.append(r'../')
sys.path.append(r'../../')


import jrs_hierarchical

def PRINTER(x):
    print '[HierarchicalJrsTrained] '+x
    #pass

class HierarchicalMlknnJrsClassifier(object):
    '''
    
    The top level adaptation of hierarchical classifier with Fractional KNNs in nodes.
    
    Mapping from the integer labels into strings is performed internally.
    
    distances - list of distances is assumed to be symmetric with smallest distance
        between object and itself!
    '''

    
    def __init__(self, distances, train_labels_input, k, label_mappings, continue_deepening, is_leaf_node):
        '''
        distances - list of lists of distances
            for example distance between x and y: distances[x][y].
        '''
        train_labels = []
        for _ in train_labels_input:
            train_labels.append([])
        
        for ind, l in enumerate(train_labels_input):
            train_labels[ind] = map(lambda x: str(x), l)
        
        train_generator = lambda: xrange(len(distances))
        knn_callable = lambda records, labels, list_of_all_labels: MlKnnJrs(distances, records, labels, k, list_of_all_labels)
        
        #label_mappings = (lambda x: x[:2], lambda x: x[:3], lambda x: x)
        #record_mappings = (lambda x: gen_1record_prefixed(x, 2), lambda x: gen_1record_prefixed(x, 3), lambda x: x)
        
        PRINTER("----------------------------------------")
        PRINTER("Training Hierarchical Fractional Knn...")
        from time import time
        start = time()
        self.hierarhical_mlknn = jrs_hierarchical.JrsMlHierarchical(train_generator, train_labels, knn_callable, 
                                                                    label_mappings, continue_deepening, is_leaf_node)
        PRINTER("Time taken for training:"+str(start-time()))
        PRINTER("----------------------------------------")

    def classify(self, sample_distances):
        classification_result = self.hierarhical_mlknn.classify(sample_distances)
        return map(lambda x: int(x), classification_result)

if __name__ == "__main__":
    
    #distances = [[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 0, 1, 2], [3, 2, 1, 0, 1], [4, 3, 2, 1, 0]]
    #labels = [['A', 'B', 'E'], ['A', 'C', 'E'], ['D', 'C','F'], ['D', 'C'], ['D', 'F', 'G']]
    #frequency_dict = {'A':4, 'B':1, 'C':100, 'D':9}# 'F':3, 'H':0}
    #labels = [['A', 'B', 'D'], ['D', 'B', 'F'], ['F', 'B'], ['B'], ['H'], ['C']]
    #labels = [['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['H'], ['A', 'B', 'D']]
    
    distances = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [1, 0, 1, 2, 3, 4, 5, 6, 7], [2, 1, 0, 1, 2, 3, 4, 5, 6], 
                 [3, 2, 1, 0, 1, 2, 3, 4, 5], [4, 3, 2, 1, 0, 1, 2, 3, 4], [5, 4, 3, 2, 1, 0, 1, 2, 3], 
                 [6, 5, 4, 3, 2, 1, 0, 1, 2], [7, 6, 5, 4, 3, 2, 1, 0, 1], [8, 7, 6, 5, 4, 3, 2, 1, 0]]
    labels = [['A', 'B', 'C'], ['A', 'D', 'C'], ['B', 'D', 'C', 'Z'], ['B', 'C', 'F', 'Z'], ['E', 'F', 'G', 'Z'], 
              ['E', 'H', 'G'], ['H', 'G', 'I'], ['F', 'G', 'I'], ['G']]
    
    k = 3
    list_of_all_labels = set(reduce(lambda x, y: x+y, labels))
    
    def mapper1(x):
        if x=='A' or x=='B' or x == 'C' or x == 'D':
            return 'subparent1'
        elif x=='Z':
            return x
        else:
            return 'subparent2'
    
    def mapper2(x):
        if x=='A' or x=='B':
            return 'subparent11'
        elif x=='C' or x=='D':
            return 'subparent12'
        elif x=='E' or x=='F':
            return 'subparent21'
        elif x=='G' or x=='H' or x=='I':
            return 'subparent22'
        
    def mapper3(x):
        if x=='G' or x=='H':
            return 'subparent111'
        return x
    
    label_mappings = (mapper1, mapper2, mapper3, lambda x: x)
    
    def continue_deepening(x):
        #print 'continue_deepening: x:', x, type(x)
        return x in ['subparent1', 'subparent2', 'subparent22', 'START_NODE']
    
    def is_leaf_node(x):
        return x in list_of_all_labels
        
    
    mlknn_jrs = HierarchicalFractionalJrsClassifier(distances, labels, k, label_mappings, continue_deepening, is_leaf_node)
    #print mlknn_jrs.fmeasure_per_class
    print mlknn_jrs.classify([1, 3, 3, 1, 2, 4, 6, 9, 11])
    print mlknn_jrs.classify([111, 113, 113, 111, 2, 4, 1, 1, 11])