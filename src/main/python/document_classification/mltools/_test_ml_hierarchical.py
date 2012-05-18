'''
Created on Apr 9, 2012

@author: mlukasik
'''
from __future__ import division
import unittest

from ml_hierarchical import MlHierarchical

import sys
sys.path.append(r'../')
from data_io.zbl_io import MULTIVAL_FIELD_SEPARATOR
from data_io.zbl_record_generators import mc2lmc_tomka_blad, gen_lmc
from tools.msc_processing import get_labels_min_occurence
from mlknn.mlknn_fractional import MlKnnFractional
from mlknn.find_closest_points import find_closest_points

class Test(unittest.TestCase):


    def testGetLabelProbabilities(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"b"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"e"+MULTIVAL_FIELD_SEPARATOR+"f"})
        lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"f"})
        lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"})
        lrecords.append({'ab': 6, 'ut': "", "ti": "", "mc":"g"})
        
        def frecords():
            for i in lrecords:
                yield i
                
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        
        class A:
            def __init__(self):
                self.distance = distance
        mlknn_fractional_callable = lambda arg_records, arg_get_labels_of_record: MlKnnFractional(arg_records, A(), find_closest_points, 
                         k, arg_get_labels_of_record)
        
        def mapper1(x):
            if x in ['a', 'b', 'c', 'd', 'e']:
                return 'FIRST'
            else:
                return 'SECOND'
        
        def mapper2(x):
            if mapper1(x) == 'FIRST':
                if x in ['a', 'b']: 
                    return 'FIRST1'
                else:
                    return 'FIRST2'
            else:
                if x in ['f', 'h']:
                    return 'SECOND1'
                else:
                    return 'SECOND2'
        
        
        label_mappings = [mapper1, mapper2, lambda x:x]
        get_labels_of_record = mc2lmc_tomka_blad
        
        
        hierarchical_classifier = MlHierarchical(frecords, mlknn_fractional_callable, label_mappings, get_labels_of_record)
        self.assertEqual(sorted(hierarchical_classifier.classify({'ab': 0.5, 'ut': "", "ti": ""})), ['a', 'b', 'd', 'e'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()