'''
Created on Dec 26, 2011

@author: mlukasik
'''
from find_closest_points import find_closest_points
import unittest

class FindClosestPointsTest(unittest.TestCase):
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    
    def testAcyclicListDistance(self):
        lrecords = []
        for k, v in enumerate(self.letters):
            lrecords.append((2*k, v))
        
        def frecords():
            for i in lrecords:
                yield i
                
        distance = lambda a, b: abs(a[0]-b[0])
        
        s = lrecords[0]
        self.assertEqual(sorted(find_closest_points(s, frecords(), [s], 3, distance)), [(2, 'b'), (4, 'c'), (6, 'd')])
        s = lrecords[5]
        self.assertEqual(sorted(find_closest_points(s, frecords(), [s], 4, distance)), [(6, 'd'), (8, 'e'), (12, 'g'), (14, 'h')])
        s = lrecords[9]
        self.assertEqual(sorted(find_closest_points(s, frecords(), [s], 3, distance)), [(12, 'g'), (14, 'h'), (16, 'i')])
        
    def testCyclicListDistance(self):
        lrecords = []
        for k, v in enumerate(self.letters):
            lrecords.append((k, v))
        
        def frecords():
            for i in lrecords:
                yield i
        
        distance = lambda a, b: min(abs(a[0]-b[0]), len(self.letters)-max(a[0], b[0])+min(a[0], b[0]))
        
        s = lrecords[0]
        #print s
        self.assertEqual(sorted(find_closest_points(s, frecords(), [s], 4, distance)), [(1, 'b'), (2, 'c'), (8, 'i'), (9, 'j')])
        s = lrecords[5]
        self.assertEqual(sorted(find_closest_points(s, frecords(), [s], 4, distance)), [(3, 'd'), (4, 'e'), (6, 'g'), (7, 'h')])
        s = lrecords[9]
        self.assertEqual(sorted(find_closest_points(s, frecords(), [s], 4, distance)), [(0, 'a'), (1, 'b'), (7, 'h'), (8, 'i')])

if __name__ == "__main__":
    unittest.main()