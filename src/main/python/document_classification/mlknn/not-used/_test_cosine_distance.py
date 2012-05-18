'''
Created on Dec 27, 2011

@author: mlukasik
'''
from __future__ import division
import unittest

from cosine_distance import CosineDistance

class Test(unittest.TestCase):

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    def testDistTxt(self):
        
        lrecords = []
        for k, v in enumerate(self.letters):
            lrecords.append((2*k, v))
        
        def frecords():
            for i in lrecords:
                yield i
                
        training_turns = 0
        zd = CosineDistance(frecords, len(lrecords), training_turns, stopwords = [])
        
        x = "mama ma czerwonego, zielonego kotka"  #5
        y =  "tata nie ma czerwonego, czarnego krokodyla ani kotka" #8
        z = "mama oraz tata maja kotka" #5
        #nie wspolne: 7 
        self.assertEqual(zd.dist_txt(x, y), 3)
        self.assertEqual(zd.dist_txt(x, z), 2)
        self.assertEqual(zd.dist_txt(y, z), 2)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()