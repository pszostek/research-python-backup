'''
Created on Dec 27, 2011

@author: mlukasik
'''
from __future__ import division
import unittest
import mlknn_basic, find_closest_points_sorted

#import os, sys
#lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
#sys.path.append(lib_path)
import sys
sys.path.append(r'../')
from data_io.zbl_io import MULTIVAL_FIELD_SEPARATOR
from data_io.zbl_record_generators import mc2lmc_tomka_blad, gen_lmc
from tools.msc_processing import get_labels_min_occurence

get_labels_of_record = mc2lmc_tomka_blad

class Test(unittest.TestCase):

    def build_mk(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"b"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"e"+MULTIVAL_FIELD_SEPARATOR+"f"})
        lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"a"})
        lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"})
        lrecords.append({'ab': 6, 'ut': "", "ti": "", "mc":"g"})
                
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        smoothing_param = 1
        
        class A:
            def __init__(self):
                self.distance = distance
            
        def get_neighbours(sample, k):
            return find_closest_points_sorted.find_closest_points_sorted(sample, lrecords, [sample], k, distance)
        
        def printer(x):
            pass
        
        mk = mlknn_basic.MlknnBasic(lrecords, get_neighbours, k, smoothing_param, get_labels_of_record, lambda x:1, printer)
        
        return mk

    def build_mlknn_old(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"b"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"e"+MULTIVAL_FIELD_SEPARATOR+"f"})
        lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"a"})
        lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"})
        lrecords.append({'ab': 6, 'ut': "", "ti": "", "mc":"g"})
                
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        smoothing_param = 1
        
        class A:
            def __init__(self):
                self.distance = distance
            
        def get_neighbours(sample):
            return find_closest_points_sorted.find_closest_points_sorted(sample, lrecords, [sample], k, distance)
        
        def printer(x):
            pass
        
        import find_closest_points, mlknn
        smoothing_param = 1
        mk2 = mlknn.MlKnn(lrecords, A(), find_closest_points.find_closest_points, 
                         k, smoothing_param, get_labels_of_record)
        return mk2

    def testGetLabelProbabilities(self):
        mk = self.build_mk()
        d = {'a': (1+4)/(1*2+7),'b': (1+3)/(1*2+7), 
             'd':(1+1)/(1*2+7), 'e':(1+1)/(1*2+7), 'f':(1+1)/(1*2+7), 
             'g':(2+1)/(1*2+7), 'h':(1+1)/(1*2+7)}
        self.assertEqual(dict(mk.labelprobabilities), d)
        
        df = {}
        for k in d:
            df[k] = 1-d[k]
        self.assertEqual(dict(mk.labelcounterprobabilities), df)
        
    def testGetPosteriorProbabilities(self):
        mk = self.build_mk()
        
        dt = {'a': {0: 0.3333333333333333, 
                   1: 0.3333333333333333, 
                   2: 0.16666666666666666, 
                   3: 0.16666666666666666}}
        
        df = {'a': {0: 0.16666666666666666, 
                   1: 0.3333333333333333, 
                   2: 0.3333333333333333, 
                   3: 0.16666666666666666}}
        
        mk_old = self.build_mlknn_old()
        
        #print "[testGetPosteriorProbabilities] printing the posterior probabilities: MLKNN and MLKNN_basic"
        for key1 in sorted( set(mk.posteriorprobabilities_true.keys()) | set(mk_old.posteriorprobabilities.keys()) ):
            #print "-",key1
            for key2 in sorted( set(mk.posteriorprobabilities_true[key1].keys()) | set(mk_old.posteriorprobabilities[key1].keys()) ):
                #print "--",key2
                #print "---",mk_old.posteriorprobabilities[key1][key2][True], mk.posteriorprobabilities_true[key1].get(key2, 0)
                self.assertEqual(mk_old.posteriorprobabilities[key1][key2][False], mk.posteriorprobabilities_false[key1].get(key2, 0))
        
        #print "[testGetPosteriorProbabilities] printing the posterior probabilities: MLKNN and MLKNN_basic"
        for key1 in sorted( set(mk.posteriorprobabilities_false.keys()) | set(mk_old.posteriorprobabilities.keys()) ):
            #print "-",key1
            for key2 in sorted( set(mk.posteriorprobabilities_false[key1].keys()) | set(mk_old.posteriorprobabilities[key1].keys()) ):
                #print "--",key2
                #print "---",mk_old.posteriorprobabilities[key1][key2][False], mk.posteriorprobabilities_false[key1].get(key2, 0)
                self.assertEqual(mk_old.posteriorprobabilities[key1][key2][False], mk.posteriorprobabilities_false[key1].get(key2, 0))
        
        #print "[MLKNN_BASIC]: dict(mk.posteriorprobabilities_true):", dict(mk.posteriorprobabilities_true)
        #print "[MLKNN_BASIC]: self.assertEqual(dict(mk.posteriorprobabilities_false):", dict(mk.posteriorprobabilities_false)
        #print "[MLKNN]: mk_old.posteriorprobabilities:", mk_old.posteriorprobabilities
        #self.assertEqual(dict(mk.posteriorprobabilities_true)['a'], dt['a'])
        #self.assertEqual(dict(mk.posteriorprobabilities_false)['a'], df['a'])  
    def testClassify(self):
        mk = self.build_mk()
        mk_old = self.build_mlknn_old()
        #make sure about the label probabilities:
        d = {'a': 0.5,'b': 2/3, 'c':1/3, 'd':1/3, 'e':1/3}
        #self.assertEqual(dict(mk.labelprobabilities), d)
        
        #make sure about the posterior probabilities:
        d = {'a': {0: {False: 0.16666666666666666, True: 0.3333333333333333}, 
                   1: {False: 0.3333333333333333, True: 0.3333333333333333}, 
                   2: {False: 0.3333333333333333, True: 0.16666666666666666}, 
                   3: {False: 0.16666666666666666, True: 0.16666666666666666}}}
             #'b': {0: {False: 0.25, True: 1/6}, 1: {False: 0.25, True: 1/3}, 2: {False: 0.5, True: 0.5}}}
        #self.assertEqual(dict(mk.posteriorprobabilities)['a'], d['a'])
        #self.assertEqual(dict(mk.posteriorprobabilities)['b'], d['b'])
        
        #check the classification:
        self.assertEqual(mk.classify({'ab': 0.5, 'ut': "", "ti": ""}), mk_old.classify({'ab': 0.5, 'ut': "", "ti": ""})) 
        self.assertEqual(mk.classify({'ab': 3.5, 'ut': "", "ti": ""}), mk_old.classify({'ab': 3.5, 'ut': "", "ti": ""})) 

if __name__ == "__main__":
    unittest.main()