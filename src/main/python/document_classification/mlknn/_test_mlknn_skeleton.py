'''
Created on May 23, 2012

@author: mlukasik
'''
import unittest
import mlknn_skeleton
import find_closest_points_sorted

def merge_lists(lists):
    return reduce(lambda a, b: a+b, lists) 

class Test(unittest.TestCase):
    def testGetCounts(self):
        MULTIVAL_FIELD_SEPARATOR = "$"
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"c"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"c"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"d"+MULTIVAL_FIELD_SEPARATOR+"e"})
        lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"e"})
        lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"g"})
        
        labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        
        class A:
            def __init__(self):
                self.distance = distance
                
        def printer(x):
            pass
        
        def get_labels(r):
            return r['mc'].split(MULTIVAL_FIELD_SEPARATOR)
        
        def get_neighbours(sample):
            return find_closest_points_sorted.find_closest_points_sorted(sample, lrecords, [sample], k, distance)
            
        mk = mlknn_skeleton.MlknnSkeleton()
        
        c, c_prim = mk.calculate_label_counts(lrecords, labels, get_neighbours, get_labels, lambda i: 1, printer)
        #print "c:", c
        #print "c_prim:", c_prim
        
        self.assertEqual(c['a'][1], 2)
        self.assertEqual(c['b'][0], 1)
        self.assertEqual(c['c'][1], 2)
        self.assertEqual(c['e'][1], 2)
        
        
        self.assertEqual(c_prim['e'][1], 1)
        self.assertEqual(c_prim['e'][2], 1)
        #self.assertEqual(c_prim, {'a': {0: 3, 1: 1, 2: 0, 3: 0}, 'c': {0: 2, 1: 1, 2: 1, 3: 0}, 'b': {0: 4, 1: 1, 2: 0, 3: 0}, 'e': {0: 2, 1: 1, 2: 1, 3: 0}, 'd': {0: 0, 1: 4, 2: 0, 3: 0}, 'g': {0: 4, 1: 1, 2: 0, 3: 0}, 'f': {0: 3, 1: 1, 2: 0, 3: 0}})
    def testCountNeighboursPerCode(self):
        MULTIVAL_FIELD_SEPARATOR = "$"
        lrecords = []
        lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
        lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"c"})
        lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"c"+MULTIVAL_FIELD_SEPARATOR+"d"})
        lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"d"+MULTIVAL_FIELD_SEPARATOR+"e"})
        lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"e"})
        lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"f"+MULTIVAL_FIELD_SEPARATOR+"g"})
        
        labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        #training_turns = len(lrecords)
        distance = lambda a, b: abs(a['ab']-b['ab'])
        #avg = (7/13 + 6/10 + 9/13)/3
        k = 2
        
        class A:
            def __init__(self):
                self.distance = distance
                
        def printer(x):
            print x
        
        def get_labels(r):
            return r['mc'].split(MULTIVAL_FIELD_SEPARATOR)
        
        def get_neighbours(sample):
            return find_closest_points_sorted.find_closest_points_sorted(sample, lrecords, [sample], k, distance)
           
        mk = mlknn_skeleton.MlknnSkeleton()
        
        print mk.count_neighbours_per_code(lrecords[0], get_neighbours, get_labels, lambda x: 1)
if __name__ == "__main__":
    unittest.main()