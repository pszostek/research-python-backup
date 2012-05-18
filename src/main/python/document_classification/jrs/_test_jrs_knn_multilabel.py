'''
Created on Mar 10, 2012

@author: mlukasik
'''
from jrs_knn_multilabel import knn_fraction_multilabel
import unittest

class jrsKnnMultilabelTest(unittest.TestCase):
    
    def testKnnFractionMultilabel(self):
        distances = [1, 2, 1, 2]
        distances2 = [2, 1, 2, 1]
        labels = [['A', 'B'], ['C', 'D'], ['A', 'C'], ['B', 'D']]
        #frequency_dict = {'A':4, 'B':1, 'C':100, 'D':9}# 'F':3, 'H':0}
        #labels = [['A', 'B', 'D'], ['D', 'B', 'F'], ['F', 'B'], ['B'], ['H'], ['C']]
        #labels = [['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['H'], ['A', 'B', 'D']]
        k = 2
        
        #print knn_multilabel_halfbayesian(distances, labels, k, 2, frequency_dict)
        #print knn_multilabel_halfbayesian(distances2, labels, k ,2, frequency_dict)
        self.assertEqual(knn_fraction_multilabel(distances, labels, k, 2), ['A'])
        self.assertEqual(knn_fraction_multilabel(distances2, labels, k, 2), ['D'])

if __name__ == "__main__":
    unittest.main()