'''
Created on Nov 3, 2011

@author: mlukasik

Klasyfikacja przy uzyciu 3nn - dla kazdej probki testowej robimy leave-one-out, a nastepnie dodajemy do siebie kody kladyfikacyjne 3 najblizszych recordow. 
Nastepnie sprawdzamy dlugosc przeciecia zbioru kodow najblizszych oraz zbioru kodow porownywanych. Stosunek tych dwoch wielkosci to jakos klasyfikacji (w zakresie 0-1).

Problemy: jak zbudowac klasyfikator? czy da sie nie tworzyc macierzy podobienstw? Wydaje sie, ze zlozonosc O(n^2) to przy 20k rekordach za duzo.
'''
from __future__ import division
import sys
sys.path.append(r'../') 
from features.find_closest_points_dmatrix import find_closest_points
from features.distance_measure import dist, calc_weights


import os
lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
sys.path.append(lib_path)
from data_io.zbl_record_generators import mc2lmc_tomka_blad

class KnnMatrixClassifier(object):
    """
    Classify using knn based on calculating distances only when necessary.
    
    """
    def __init__(self, frecords, frecords_len, elems4weights, distance = dist):
        """
        """
        self.frecords = frecords
        self.frecords_len = frecords_len
        self.elems4weights = elems4weights
        self.distance = distance
        print "calculating weights..."
        self.weights, self.shifts = calc_weights(self.frecords, self.frecords_len, self.elems4weights)
        print "weights are:"
        print "weights:", self.weights
        print "shifts:", self.shifts
        self.sample_classif_func = mc2lmc_tomka_blad
    
    def classify(self, sample, excluding = [], closest=3):
        """
        Classify sample, findig 'closest' number of closest points and assigning their classification codes
        
        """
        #print "sample", sample
        #print "excluding", excluding
        f = lambda x, y: dist(x, y, self.weights, self.shifts)
        best_elems = find_closest_points(sample, self.frecords, excluding, closest, f)
        #print "best_elems", best_elems
        return reduce(lambda x, y: x+y, map(lambda r: mc2lmc_tomka_blad(r), best_elems))

    def loo(self, iters, doprint=True): 
        import random
        correctness=0
        #main loop:
        for _ in range(iters):
            i = random.randint(0, self.frecords_len-1)
            if doprint:
                print "looking for elemnt no:", i
            #print "looking for i:", i
            ind = 0
            elem = -1
            for r in self.frecords():
                if ind==i:
                    elem=r
                    break
                ind+=1
            
            if doprint:
                print "classifying it"
            classif_ans = self.classify(elem, [elem])
            if doprint:
                print i, "classified as:", classif_ans, "when it's:", self.sample_classif_func(elem)
            true_ans = set(self.sample_classif_func(elem))
            correctness += len(set(classif_ans) & true_ans)/len(true_ans)
            
        return correctness