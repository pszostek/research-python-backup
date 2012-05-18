'''
Created on Dec 29, 2011

@author: mlukasik
'''
import unittest
import sys
sys.path.append(r'../')
from msc_processing2 import count_msc_occurences, get_labels_min_occurence

class Test(unittest.TestCase):

    def testCountMscOccurences(self):
        
        def code_generator():
            for i in xrange(1, 10):
                yield range(i)
        
        r = count_msc_occurences(code_generator)
        self.assertEqual(r, {0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1})
    
    def testGetLabelsMinOccurence(self):
        
        def code_generator():
            for i in xrange(1, 10):
                yield range(i)
        
        r = get_labels_min_occurence(code_generator, 3)
        self.assertEqual(r, [0, 1, 2, 3, 4, 5, 6])
        
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()