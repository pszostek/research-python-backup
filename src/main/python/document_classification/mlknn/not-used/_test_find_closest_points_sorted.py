'''
Created on Dec 26, 2011

@author: mlukasik
'''
from find_closest_points_sorted import find_closest_points_sorted
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
        
        print '[FindClosestPointsTest:testAcyclicListDistance] lrecords', lrecords
                
        distance = lambda a, b: abs(a[0]-b[0])
        
        s = lrecords[0]
        #print "for s:", s, "find_closest_points_sorted(s, frecords(), [s], 3, distance):", find_closest_points_sorted(s, frecords(), [s], 3, distance)
        self.assertEqual(find_closest_points_sorted(s, frecords(), [s], 3, distance), [(2, 'b'), (4, 'c'), (6, 'd')])
        
        s = (9.5, 'rr')
        self.assertTrue(find_closest_points_sorted(s, frecords(), [lrecords[5]], 4, distance) == [(8, 'e'), (12, 'g'), (6, 'd'), (14, 'h')])
        
        s = lrecords[9]
        #print "for s:", s, "find_closest_points_sorted(s, frecords(), [s], 3, distance):", find_closest_points_sorted(s, frecords(), [s], 3, distance)
        self.assertEqual(find_closest_points_sorted(s, frecords(), [s], 3, distance), [(16, 'i'), (14, 'h'), (12, 'g')])
        
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
        #print "for s:", s, "find_closest_points_sorted(s, frecords(), [s], 4, distance):", find_closest_points_sorted(s, frecords(), [s], 4, distance)
        self.assertEqual(find_closest_points_sorted(s, frecords(), [s], 4, distance), [(9, 'j'), (1, 'b'), (2, 'c'), (8, 'i')])
        s = lrecords[5]
        #print "for s:", s, "find_closest_points_sorted(s, frecords(), [s], 4, distance):", find_closest_points_sorted(s, frecords(), [s], 4, distance)
        self.assertEqual(sorted(find_closest_points_sorted(s, frecords(), [s], 4, distance)), [(3, 'd'), (4, 'e'), (6, 'g'), (7, 'h')])
        s = lrecords[9]
        #print "for s:", s, "find_closest_points_sorted(s, frecords(), [s], 4, distance):", find_closest_points_sorted(s, frecords(), [s], 4, distance)
        self.assertEqual(sorted(find_closest_points_sorted(s, frecords(), [s], 4, distance)), [(0, 'a'), (1, 'b'), (7, 'h'), (8, 'i')])

if __name__ == "__main__":
    unittest.main()