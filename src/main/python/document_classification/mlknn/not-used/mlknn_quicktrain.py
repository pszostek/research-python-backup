'''
Created on Jan 1, 2012

@author: mlukasik
'''
from __future__ import division

from mlknn import MlKnn

#import os, sys
#lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
#sys.path.append(lib_path)
import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import mc2lmc_tomka_blad

class MlKnnQuickTrain(MlKnn):
    '''
    
    A quicker version, training the posterior probabilities based on only a part of the
    training data.
    '''
    def __init__(self, frecords, distance, find_closest_points, k, labels, 
                 smoothing_param, min_label_occurence, ismlknn = True):
        '''
        Constructor.
        
        frecords - generator returning records, is used to calculate parameters (probabilities)
            and nearest neighbours amongst the records it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific frecords parameter
            
        distance - function which calculates distance, of signature: distance(rec1, rec2)
        
        find_closest_points - function finding closest points, of signature:
            find_closest_points(sample, records, excluding, how_many, distance)
        
        k - no. of neighbours taken into consideration
        
        labels - list of labels
        
        smoothing_param - min number of occurences of each label
        
        min_label_occurence - minimum label occurence count when training the posterior probabilities
        
        ismlknn - calculate the probabilities from the paper; it is possible not to calculate them,
            if the user wants to use classify_stupid functions only
        
        '''
        self.frecords = frecords
        self.distance = distance
        self.find_closest_points = find_closest_points
        self.k = k
        self.labels = labels
        self.smoothing_param = smoothing_param
        #pre-computations:
        if ismlknn:
            self.labelprobabilities, self.labelcounterprobabilities = self.get_label_probabilities()
            self.posteriorprobabilities = self.get_posterior_probabilities_quicktrain(min_label_occurence)

    def get_posterior_probabilities_quicktrain(self, min_label_occurence):
        '''
        Computing the posterior probabilities P (Ej |Hb ).
        Training only on part of the data set, so that each label occurs at least min_label_occurence.
        
        #todo: do shuffling when choosing elements.
        '''
        from collections import defaultdict
        #preperation
        c = {}
        c_prim = {}
        labels_cnt = {}
        for label in self.labels:
            c[label] = {}
            c_prim[label] = {}
            for i in xrange(self.k+1):
                #number of elements of a given label which have i neighbours of a given label
                c[label][i] = 0
                c_prim[label][i] = 0
            labels_cnt[label] = 0
        #for each record compute
        elem_cnt = 0#todel
        for r in self.frecords():
            #if all the labels occur minimum no of times, break:
            if len(labels_cnt) == 0:
                break
            
            labels_codes = mc2lmc_tomka_blad(r)
            
            elem_cnt+=1#todel
            if elem_cnt%100 == 1:#todel
                print elem_cnt#todel
            
            print "labels_cnt:", labels_cnt
            #check if this records brings some improve, and update
            is_important = False
            for l in labels_codes:
                if l in labels_cnt:
                    is_important = True
                    labels_cnt[l] += 1
                    if labels_cnt[l] >= min_label_occurence:
                         labels_cnt.pop(l)
            if is_important:
                d = defaultdict(lambda: 0)
                for code in self.classify_stupid(r):
                    d[code]+=1
                for code in self.labels:
                    if code in labels_codes:
                        c[code][d[code]] += 1
                    else:
                        c_prim[code][d[code]] += 1
                    
        #compute the final values:
        peh = {}
        for code in self.labels:
            peh[code] = {}
            for i in xrange(self.k+1):
                peh[code][i] = {}
                
        for code in self.labels:
            sum_c = sum(c[code].itervalues())
            sum_c_prim = sum(c_prim[code].itervalues())
            for i in xrange(self.k+1):
                peh[code][i][True] = (self.smoothing_param + c[code][i])/(self.smoothing_param * (self.k + 1) + sum_c)
                peh[code][i][False] = (self.smoothing_param + c_prim[code][i])/(self.smoothing_param * (self.k + 1) + sum_c_prim) 
        return peh