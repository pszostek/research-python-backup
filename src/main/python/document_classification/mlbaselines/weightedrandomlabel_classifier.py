'''
Created on Feb 22, 2012

@author: mlukasik

Classifier returning a random label from a weigherd distribution.
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

def PRINTER_TESTS(x):
    pass
    #print x

classify_oracle = lambda x: mc2lmc_tomka_blad(x) #because function assigned outside from a class doesn't pickle!

class WeightedRandomLabelClassifier(object):
    '''
    Assign a random subset of labels to a given sample.
    
    Takes use of the information on how many labels have been assigned by oracle.  
    '''


    def __init__(self, frecords, get_labels_of_record, classify_oracle2):
        '''
        Constructor.
        
        @type frecords: generator
        @param frecords: generator returning records, is used to calculate parameters (probabilities)
            and nearest neighbours amongst the records it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific frecords parameter
        
        @type get_labels_of_record: function
        @param get_labels_of_record: returns list of labels assigned to a record
        
        @type classify_oracle2: function
        @param classify_oracle2: returning the true labels of a record
        '''
        #self.get_labels_of_record = get_labels_of_record
        self.label2count, self.all_occurences = self.get_counted_labels(frecords, get_labels_of_record)
        PRINTER_TESTS("[init:]self.label2count "+str(self.label2count))
        PRINTER_TESTS("[init:]self.all_occurences "+str(self.all_occurences))
        #self.classify_oracle = classify_oracle
        PRINTER('[WeightedRandomLabelClassifier: init] labels: '+str(list(self.label2count.iterkeys())))
        
    def get_counted_labels(self, frecords, get_labels_of_record):
        '''
        Return a dictionary label -> its count.
        '''
        from collections import defaultdict
        label2count = defaultdict(lambda: 0)
        all_occurences = 0
        for rec in frecords():
            for l in get_labels_of_record(rec):
                label2count[l]+=1
                all_occurences+=1
        return dict(label2count), all_occurences
    
    def random_weighted_subset(self, subset_size):
        '''
        Find a random subset of size subset_size, according to weights in label2count
        '''
        PRINTER_TESTS("[random_weighted_subset:]subset_size "+str(subset_size))
        
        excluded_labels = set()
        excluded_count = 0
        result = []
        #choose a new label as many times as subset_size: 
        for _ in xrange(subset_size):
            PRINTER_TESTS("[random_weighted_subset:]result "+str(result))
            PRINTER_TESTS("[random_weighted_subset:]excluded_count "+str(excluded_count))
            
            choice = random.randint(1, self.all_occurences-excluded_count)
            PRINTER_TESTS("[random_weighted_subset:] tossing from up to: "+str(self.all_occurences-excluded_count))
            PRINTER_TESTS("[random_weighted_subset:] got: "+str(choice))
            #find out which label the 'choice' corresponds to
            curr_choice = 0
            for l, count in self.label2count.iteritems():
                if l not in excluded_labels:
                    curr_choice += count
                    if curr_choice>=choice:
                        result.append(l)
                        excluded_labels.add(l)
                        excluded_count += count
                        break
        return result
                    
        
    def classify(self, sample):
        '''
        Classify sample choosing random subset.
        '''
        subset_size = len(classify_oracle(sample))
        return self.random_weighted_subset(subset_size)