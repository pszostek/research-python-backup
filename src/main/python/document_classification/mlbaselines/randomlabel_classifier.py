'''
Created on Feb 22, 2012

@author: mlukasik

Classifier returning a random label assuming a uniform distribution.
'''
from __future__ import division
import random

import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import mc2lmc_tomka_blad

def PRINTER(x):
    #pass
    import logging
    logging.info(x)
    #print x#

classify_oracle = lambda x: mc2lmc_tomka_blad(x) #because function assigned outside from a class doesn't pickle!
        
class RandomLabelClassifier(object):
    '''
    Assign a random subset of labels to a given sample.
    
    Takes use of the information on how many labels have been assigned by oracle.  
    '''


    def __init__(self, frecords, get_labels_of_record, find_all_labels, classify_oracle):
        '''
        Constructor.
        
        @type frecords: generator
        @param frecords: generator returning records, is used to calculate parameters (probabilities)
            and nearest neighbours amongst the records it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific frecords parameter
        
        @type get_labels_of_record: function
        @param get_labels_of_record: returns list of labels assigned to a record
        
        @type find_all_labels: function
        @param find_all_labels: returns list of all labels in frecords
        
        @type classify_oracle: function
        @param classify_oracle: returning the true labels of a record
        '''
        self.labels = find_all_labels(frecords)
        PRINTER('[RandomLabelClassifier: init] labels: '+str(self.labels))
    
    def classify(self, sample):
        '''
        Classify sample choosing random subset.
        '''
        subset_size = len(classify_oracle(sample))
        return random.sample(self.labels, subset_size)