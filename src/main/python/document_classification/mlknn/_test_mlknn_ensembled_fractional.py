'''
Created on Dec 27, 2011

@author: mlukasik
'''
from __future__ import division
import unittest
import mlknn_ensembled_fractional, find_closest_points_sorted

#import os, sys
#lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
#sys.path.append(lib_path)
import sys
sys.path.append(r'../')
from data_io.zbl_io import MULTIVAL_FIELD_SEPARATOR
from data_io.zbl_record_generators import mc2lmc_tomka_blad, gen_lmc
from tools.msc_processing import get_labels_min_occurence

get_labels_of_record = mc2lmc_tomka_blad
find_all_labels = lambda frecords: get_labels_min_occurence(lambda: gen_lmc(frecords), 1)

class Test(unittest.TestCase):


    def testGetLabelProbabilities(self):
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"c"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"c"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"d"+MULTIVAL_FIELD_SEPARATOR+"e"})
        lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"e"})
        lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"g"})
        
        def frecords():
            for i in lrecords:
                yield i
                
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k_list = [2, 3, 4]
        
        class A:
            def __init__(self):
                self.distance = distance
            
        mk = mlknn_ensembled_fractional.MlKnnFractionalEnsembledStrongest(frecords, A(), find_closest_points_sorted.find_closest_points_sorted, 
                         k_list, get_labels_of_record)
        
        print "classify record of val 1:", mk.classify({'ab': 1, 'ut': "", "ti": "", "mc":"c"+MULTIVAL_FIELD_SEPARATOR+"d"})
        
        
        print "classify record of val 3.5:", mk.classify({'ab': 3.5, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"e"})
        #self.assertEqual(dict(mk.c), {'a': {0: 0, 1: 2, 2: 0, 3: 0}, 'c': {0: 0, 1: 2, 2: 0, 3: 0}, 'b': {0: 1, 1: 0, 2: 0, 3: 0}, 'e': {0: 0, 1: 2, 2: 0, 3: 0}, 'd': {0: 0, 1: 2, 2: 0, 3: 0}, 'g': {0: 1, 1: 0, 2: 0, 3: 0}, 'f': {0: 0, 1: 2, 2: 0, 3: 0}})
        #self.assertEqual(dict(mk.c_prim), {'a': {0: 3, 1: 1, 2: 0, 3: 0}, 'c': {0: 2, 1: 1, 2: 1, 3: 0}, 'b': {0: 4, 1: 1, 2: 0, 3: 0}, 'e': {0: 2, 1: 1, 2: 1, 3: 0}, 'd': {0: 0, 1: 4, 2: 0, 3: 0}, 'g': {0: 4, 1: 1, 2: 0, 3: 0}, 'f': {0: 3, 1: 1, 2: 0, 3: 0}})
        #self.assertEqual(dict(mk.fraction_knn_thresholds)['a'], 1)
        #print '[testGetLabelProbabilities] mk.fraction_knn_thresholds: ', mk.fraction_knn_thresholds
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    