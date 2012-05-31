'''
Created on April, 22, 2012

@author: mlukasik

MLKNN classifier.
'''
from __future__ import division
from collections import defaultdict
from find_all_labels import find_all_labels
from mlknn_fractional import MlKnnFractional

def PRINTER(x):
    #pass
    import logging
    logging.info(x)

class MlKnnFractionalEnsembledStrongest(object):
    '''
    @deprecated: use MlknnTEnsembled instead.
    
    Naive Bayes with KNN as features.
    
    Modification of a classifier based on a publication: 
    Ml-knn: A Lazy Learning Approach to Multi-Label Learning 
    Min-Ling Zhang, Zhi-Hua Zhou.
    
    A threshold is being chosen for each class, maximizing the f-measure.
    
    Ensemble of such MlKnn's is created - strongest' vote in terms of f-measures is
    chosen.
    
    Processing of the whole dataset is being performed in order to 
    calculate a priori and a posteriori probabilities.
    
    NOTE: this is inefficient implementation. Good implementation: Compute the neighbours once for each sample
    (training or testing) and, having it sorted (or even heapify -> then time is linear) pop consecutive k
    elements. Now the time will linearly grow as the list of k's grows.
    '''

    def __init__(self, frecords, distance, find_closest_points, k_list, get_labels_of_record):
        '''
        Constructor.
        
        @type frecords: list of records
        @param frecords: used to calculate parameters (probabilities)
            and nearest neighbours amongst the records it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific frecords parameter
            
        @type distance: object that contains a method of signature: distance(rec1, rec2)
        @param distance: returns distance measure between 2 records
        
        @type find_closest_points: function of signature:
            find_closest_points(sample, records, excluding, how_many, distance);
            It returns training objects which are closest to the sample, in a sorted form, increasing
            order in terms of their distance from sample.
        @param distance: finding closest points,
        
        @type k_list: list of integers
        @param k_list: list of no. of neighbours taken into consideration
        
        @type get_labels_of_record: function
        @param get_labels_of_record: returns list of labels assigned to a record
        
        '''
        self.list_of_all_labels = find_all_labels(list(frecords()), get_labels_of_record)
        self.k_list = k_list
        PRINTER('[MlKnnFractionalEnsembledStrongest: init] labels: '+str(self.list_of_all_labels))
        PRINTER('[MlKnnFractionalEnsembledStrongest: init]: START OF TRAINING...')
        
        self.mlknn_fractionals = {}
        for k in self.k_list:
            self.mlknn_fractionals[k] = MlKnnFractional(frecords, distance, find_closest_points, k, 
                 get_labels_of_record)

        PRINTER('[MlKnnFractionalEnsembledStrongest: init]: END OF TRAINING...')
        
    
    def classify(self, sample):
        '''
        Classify sample using ensemble fractional KNN.
        
        '''
        answer = {}
        for code in self.list_of_all_labels:
            answer[code] = {}
            answer[code]['decision'] = False
            answer[code]['certainty'] = 0.0
        
        for k in self.k_list:
            #print '[classify]: k:', k
            sub_answer = set(self.mlknn_fractionals[k].classify(sample))
            #print 'sub_answer:', sub_answer
            #for each code determine wether it is describing the sample or not:
            for code in self.list_of_all_labels:
                #print 'considering code:', code
                sub_certainty = self.mlknn_fractionals[k].fmeasure_per_class[code]
                if sub_certainty > answer[code]['certainty']:
                    #print 'bigger certainty! ', code, sub_answer, code in sub_answer
                    answer[code]['decision'] = code in sub_answer
                    answer[code]['certainty'] = sub_certainty
            #print "after that, answer:", answer
        return [code for code in self.list_of_all_labels if answer[code]['decision']]