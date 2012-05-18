'''
Created on Nov 3, 2011

@author: mlukasik
'''
from __future__ import division
from itertools import izip

import sys
sys.path.append(r'../')
from tools.stop_words_list import STOP_WORDS_LIST
from tools.text_to_words import text_to_words

class JaccardDistance(object):
    """
    Encapsulates distance calculations between Zbl records.
    
    Calculates a jaccard index between texts representing the 2 documents.
    
    The texts are built by merging the: abstracts, titles and keywords.
    
    ------------
    Old comment:
    A propo problemu dopasowywania autorow:
    Problem grafowy: lepiej zrobic tak, ze wybieramy minimalny blad dopasowujac autorow 
    - do tego moze lepiej poczytac Cormena. Moze tez algorytm wegierski, biorac pierwszych min, 
    ale to bedzie troszke gorsze niz wczesniejszy pomysl.
    
    """
    def __init__(self, frecords, frecords_size, training_turns, 
                 stopwords = STOP_WORDS_LIST):
        """
        Train weights and shifts.
        
        """
        self.stopwords = stopwords
        self.weights, self.shifts = self.calc_weights(frecords, frecords_size, training_turns)
        
    def dist_txt(self, x, y):
        """
        Calculates distance between 2 given texts.
        
        It calculates 1 - (set(x)&set(y) / set(x)|set(y)).
        
        TESTED.
        """
        x_s = set(text_to_words(x))
        y_s = set(text_to_words(y))
        return len(x_s & y_s)/len(x_s | y_s)

    def dist_vector(self, x, y):
        """
        Calculates a vector of numbers, which reflects distance between records x and y; 
        the bigger the numbers in the vector, the further apart are the 2 records    
        
        Assumes format of ZBL. x and y are dictionaries of features.
        
        """
        dist = []
        
        #txt:
        dist.append(self.dist_txt(" ".join([x['ab'], x['ti'], x['ut']]), 
                                  " ".join([y['ab'], y['ti'], y['ut']])))
        #dates:
        #dist.append(abs(int(x['py']) - int(y['py']))/70)
        #authors:
        #dist.append(self.dist_txt(x['au'], y['au']))
        #journal:
        #dist.append(dist_str(x['jt'], y['jt']))
        #publisher:
        #dist.append(self.dist_str(x['jp'], y['jp']))
        
        return dist
    
    def distance(self, x, y):
        """
        Calculates distance between records: x and y.
        
        TESTED.
        
        """
        vec_shifted = (i-j for i, j in izip(self.dist_vector(x, y), self.shifts))
        vec_normalized = (i*j for i, j in izip(vec_shifted, self.weights))
        
        return sum(vec_normalized) 
    
    def calc_weights(self, frecords, frecords_size, training_turns):
        """
        Calculate weights from elems number of random records from frecords.
        
        TESTED.

        """
        if training_turns==0:
            return None, None
        
        #1. choose training_turns number of elements in random:
        import random
        elements = sorted(random.sample(xrange(frecords_size), training_turns), reverse=True)
        chosen = []
        
        ind = 0
        curr = elements.pop()
        for r in frecords():
            if ind==curr:
                chosen.append(r)
                if len(elements)==0:
                    break
                curr = elements.pop()
            ind+=1
        
        #2. calculate distances all vs all:
        distances = []
        for first in xrange(len(chosen)):
            for second in xrange(first+1, len(chosen)):
                distances.append(self.dist_vector(chosen[first], chosen[second]))
        
        #3. calculate shifts:
        shifts = []
        for i in xrange(len(distances[0])):
            shifts.append(sum(x[i] for x in distances)/len(distances))
            
        #print "distances:", distances
        #4. calculate weights:
        weights = []
        for i in xrange(len(distances[0])):
            weights.append(1/(sum(abs(x[i]-shifts[i]) for x in distances)/len(distances)))
        
        return weights, shifts