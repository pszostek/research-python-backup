'''
Created on Dec 27, 2011

@author: mlukasik
'''
from __future__ import division
import unittest
import mlknn, find_closest_points

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
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"b"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"e"+MULTIVAL_FIELD_SEPARATOR+"f"})
        lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"a"})
        lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"})
        lrecords.append({'ab': 6, 'ut': "", "ti": "", "mc":"g"})
        
        def frecords():
            for i in lrecords:
                yield i
                
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        smoothing_param = 1
        
        class A:
            def __init__(self):
                self.distance = distance
            
        mk = mlknn.MlKnn(frecords, A(), find_closest_points.find_closest_points, 
                         k, smoothing_param, find_all_labels, get_labels_of_record)
        
        d = {'a': (1+4)/(1*2+7),'b': (1+3)/(1*2+7), 
             'd':(1+1)/(1*2+7), 'e':(1+1)/(1*2+7), 'f':(1+1)/(1*2+7), 
             'g':(2+1)/(1*2+7), 'h':(1+1)/(1*2+7)}
        self.assertEqual(dict(mk.labelprobabilities), d)
        
        df = {}
        for k in d:
            df[k] = 1-d[k]
        self.assertEqual(dict(mk.labelcounterprobabilities), df)
        
    def testGetPosteriorProbabilities(self):
        letters = ['a', 'b', 'c', 'd', 'e']
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"b"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"c"+MULTIVAL_FIELD_SEPARATOR+"e"})
        
        def frecords():
            for i in lrecords:
                yield i
                
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        smoothing_param = 1
        class A:
            def __init__(self):
                self.distance = distance
        
        mk = mlknn.MlKnn(frecords, A(), find_closest_points.find_closest_points, 
                         k, smoothing_param, find_all_labels, get_labels_of_record)
        
        #print 'mk.labelprobabilities: ', mk.labelprobabilities
        #print 'mk.labelcounterprobabilities: ', mk.labelcounterprobabilities
        
        d = {'a': {0: {False: 0.16666666666666666, True: 0.3333333333333333}, 
                   1: {False: 0.3333333333333333, True: 0.3333333333333333}, 
                   2: {False: 0.3333333333333333, True: 0.16666666666666666}, 
                   3: {False: 0.16666666666666666, True: 0.16666666666666666}}}
             #'b': {0: {False: 0.25, True: 1/6}, 1: {False: 0.25, True: 1/3}, 2: {False: 0.5, True: 0.5}}}
        self.assertEqual(dict(mk.posteriorprobabilities)['a'], d['a'])
        #self.assertEqual(dict(mk.posteriorprobabilities)['b'], d['b'])
        
        
    def testClassify(self):
        letters = ['a', 'b', 'c', 'd', 'e']
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"b"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"c"+MULTIVAL_FIELD_SEPARATOR+"e"})
        
        def frecords():
            for i in lrecords:
                yield i
                
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        smoothing_param = 1
        
        class A:
            def __init__(self):
                self.distance = distance
             
        mk = mlknn.MlKnn(frecords, A(), find_closest_points.find_closest_points, 
                         k, smoothing_param, find_all_labels, get_labels_of_record)
        
        #make sure about the label probabilities:
        d = {'a': 0.5,'b': 2/3, 'c':1/3, 'd':1/3, 'e':1/3}
        self.assertEqual(dict(mk.labelprobabilities), d)
        
        #make sure about the posterior probabilities:
        d = {'a': {0: {False: 0.16666666666666666, True: 0.3333333333333333}, 
                   1: {False: 0.3333333333333333, True: 0.3333333333333333}, 
                   2: {False: 0.3333333333333333, True: 0.16666666666666666}, 
                   3: {False: 0.16666666666666666, True: 0.16666666666666666}}}
             #'b': {0: {False: 0.25, True: 1/6}, 1: {False: 0.25, True: 1/3}, 2: {False: 0.5, True: 0.5}}}
        self.assertEqual(dict(mk.posteriorprobabilities)['a'], d['a'])
        #self.assertEqual(dict(mk.posteriorprobabilities)['b'], d['b'])
        
        #check the classification:
        self.assertEqual(set(mk.classify({'ab': 0.5, 'ut': "", "ti": ""}))&set(['a', 'b']), set(['b']))
        self.assertEqual(set(mk.classify({'ab': 3.5, 'ut': "", "ti": ""}))&set(['a', 'b']), set(['b']))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    