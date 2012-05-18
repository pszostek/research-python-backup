'''
Created on Jan 18, 2012

@author: mlukasik
'''
from __future__ import division
import unittest
import multilabel_evaluate

class Test(unittest.TestCase):

    def testMultilabelEvaluate(self):
        test_generator = lambda: range(20)
        classify_oracle = lambda x: [str(int(x%3==0))+str(int(x%2==0))]
        classify_try = lambda x: [str(int(x%3==0))+str(int(x%4==0))]
        labels_len = 2#because 2 labels: True and False
        label_functions = {'full label': lambda x: x, 'short label': lambda x: x[:1]}
        
        #print '[testMultilabelEvaluate] test_generator:', test_generator, test_generator()
        #print '[testMultilabelEvaluate] classify_oracle classify_try:', classify_oracle(1), classify_try(4)
        
        accuracy, precision, recall, hammingloss, subset01loss, fmeasure = multilabel_evaluate.multilabel_evaluate(test_generator, classify_oracle, classify_try, labels_len, label_functions)
        
        self.assertEqual(accuracy['short label'], 1)
        self.assertEqual(precision['short label'], 1)
        self.assertEqual(recall['short label'], 1)
        self.assertEqual(hammingloss['short label'], 0)
        self.assertEqual(subset01loss['short label'], 0)
        
        self.assertEqual(accuracy['full label'], 0.75)
        self.assertEqual(precision['full label'], 0.75)
        self.assertEqual(recall['full label'], 0.75)
        self.assertEqual(hammingloss['full label'], 0.25)
        self.assertEqual(subset01loss['full label'], 0.25)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()