'''
Created on Dec 27, 2011

@author: mlukasik
'''
from __future__ import division
import unittest

from jaccard_distance import JaccardDistance

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
        zd = JaccardDistance(frecords, len(lrecords), training_turns, stopwords = [])
        
        x = "mama ma czerwonego, zielonego kotka"  #5
        y =  "tata nie ma czerwonego, czarnego krokodyla ani kotka" #8
        z = "mama oraz tata maja kotka" #5
        #nie wspolne: 7 
        self.assertEqual(zd.dist_txt(x, y), 7/13)
        self.assertEqual(zd.dist_txt(x, z), 6/10)
        self.assertEqual(zd.dist_txt(y, z), 9/13)

    def testDist(self):
        
        x = "mama ma czerwonego, zielonego kotka"  #5
        y =  "tata nie ma czerwonego, czarnego krokodyla ani kotka. " #8
        z = "mama oraz tata maja kotka" #5
        #nie wspolne: 7 
        lrecords = []
        lrecords.append({'ab': x, 'ut': "", "ti": ""})
        lrecords.append({'ab': y, 'ut': "", "ti": ""})
        lrecords.append({'ab': z, 'ut': "", "ti": ""})
        
        def frecords():
            for i in lrecords:
                yield i
                
        training_turns = len(lrecords)
        zd = JaccardDistance(frecords, len(lrecords), training_turns, stopwords = [])
        

        self.assertEqual(zd.dist_txt(x, y), 7/13)
        self.assertEqual(zd.dist_txt(x, z), 6/10)
        self.assertEqual(zd.dist_txt(y, z), 9/13)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()