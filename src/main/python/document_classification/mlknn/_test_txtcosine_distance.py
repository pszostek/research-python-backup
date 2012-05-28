'''
Created on May 21, 2012

@author: mlukasik
'''
from __future__ import division
import unittest

from txt_cosine_distance import TxtCosineDistance

class Test(unittest.TestCase):

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    
    def testDist(self):
        
        x = "423: 2      ,       1756: 1 ,       2187: 1 ,       2459: 1 ,       2769: 1 ,       3040: 1 ,       3982: 1 ,       4013: 2 ,       4283: 1 ,       4593: 1"  #5
        y =  "453: 2      ,       2187: 1 ,       2459: 1 ,       2769: 1 ,       4593: 1" #8
        z = "1 : 1"
        #nie wspolne: 7 
        dx = {'g0': x}
        dy = {'g0': y}
        dz = {'g0': z}
        
        lrecords = [dx, dy, dz]

        training_turns = len(lrecords)
        zd = TxtCosineDistance('g0')

        #self.assertEqual(zd.distance(x, y), 7/13)
        print "zd.dist_txt(dx, dy)", zd.distance(dx, dy)
        print "zd.dist_txt(dz, dy)", zd.distance(dz, dy)
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()