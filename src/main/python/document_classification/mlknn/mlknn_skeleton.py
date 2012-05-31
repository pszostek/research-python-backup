'''
Created on May 23, 2012

@author: mlukasik
'''
from __future__ import division
from collections import defaultdict

import find_all_labels

class MlknnSkeleton(object):
    '''
    This is a skeleton of MLKNN, which is further extended by the MLKNN itself and its variations.
    '''

    #-------------------------------------------TRAINING-----------------------------------------------#             
    def find_all_labels(self, tobjects, get_labels):
        return find_all_labels.find_all_labels(tobjects, get_labels)
    
    def calculate_label_counts(self, tobjects, labels, find_nearest_neighbours, k, get_labels, kernel, printer):
        '''
        Calculate label counts in neighbourhood in the training set.
        (Leave one out method).
        
        @type tobjects: list of training objects
        @param tobjects: training objects
        
        @type labels: list of strings
        @param labels: list of labels.
        
        @type get_labels: function
        @param get_labels: returns list of labels assigned to an object
        
        @type get_neigh_labels: function
        @param get_neigh_labels: returns list of labels assigned to the neighbours of an object
            (with repetitions)
        
        @type kernel: function
        @param kernel: returns the importance measure of a neighour of given ordinal number
        
        @type printer: function
        @param printer: prints a given string.
        '''
        #preparation
        c = {}
        c_prim = {}
        for label in labels:
            c[label] = {}
            c_prim[label] = {}

        #for each record compute
        elem_cnt = 0
        for r in tobjects:
            elem_cnt+=1
            if elem_cnt%100 == 1:
                printer("[MlknnSkeleton][__get_posterior_probabilities]: training in step: "+str(elem_cnt))

            rlabels = get_labels(r)
            d = {}

            for ind, neighbhour in enumerate(find_nearest_neighbours(r, k)):
                for label in get_labels(neighbhour):
                    d[label] = d.get(label, 0)+kernel(ind)
            for code in labels:
                neigh_count = d.get(code, 0)
                if code in rlabels:
                    c[code][neigh_count] = c[code].get(neigh_count, 0)+1
                else:
                    c_prim[code][neigh_count] = c_prim[code].get(neigh_count, 0)+1

        return c, c_prim

    def count_neighbours_per_code(self, sample, find_nearest_neighbours, k, get_labels, kernel):
        '''
        Counts number of neighbours amongst the k nearest neighbours per a code.
        
        @type kernel: function
        @param kernel: returns the importance measure of a neighour of given ordinal number
        '''
        neigh_labels = {}
        for ind, neighbhour in enumerate(find_nearest_neighbours(sample, k)):
            for label in get_labels(neighbhour):
                neigh_labels[label] = neigh_labels.get(label, 0)+kernel(ind)
        return neigh_labels
    
                
if __name__ == "__main__":
    import doctest
    doctest.testmod()