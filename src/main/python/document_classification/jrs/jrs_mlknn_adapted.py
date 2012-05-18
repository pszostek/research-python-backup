'''
Created on Mar 10, 2012

@author: mlukasik
'''

import sys
sys.path.append(r'../')
sys.path.append(r'../../')


from mlknn import mlknn
from mlknn import find_closest_points

class MlKnnJrs(object):
    '''
    Naive Bayes with KNN as features adapted for JRS.
    '''

    
    def __init__(self, distances, records, labels, k, list_of_all_labels):
        '''
        distances - list of lists of distances
            for example distance between x and y: distances[x][y].
        '''
        
    
        self.records = []
        #for ind, distance_list in enumerate(distances):
        for ind in records:
            self.records.append({'id': ind, 'distances': distances[ind], 'labels': labels[ind]})
        
        def subdistance(x, y): 
            '''
            Distance between 2 records of format:
            {'id': ind, 'distances': distance_list, 'labels': labels[ind]}
            '''
            if x['id'] > -1:
                #print "[subdistance](x, y)", x, y, y['distances'][x['id']]
                return y['distances'][x['id']]
            #print "[subdistance](x, y)", x, y, x['distances'][y['id']]
            return x['distances'][y['id']]
        
        class ClassDistance:
            def __init__(self):
                self.distance = subdistance
        
        get_labels_of_record = lambda x: x['labels']
        
        self.mlknn = mlknn.MlKnn(lambda: self.records, ClassDistance(), 
                    find_closest_points.find_closest_points, k, 
                    1, lambda x: list_of_all_labels, get_labels_of_record)

    def classify(self, sample_distances):
        sample_formatted = {'id':-1, 'distances': sample_distances, 'labels':None}
        #print "[MlKnnJrs:classify]: classifying sample:", sample_formatted
        return self.mlknn.classify(sample_formatted)

if __name__ == "__main__":
    
    distances = [[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 0, 1, 2], [3, 2, 1, 0, 1], [4, 3, 2, 1, 0]]
    labels = [['A', 'B'], ['A', 'C'], ['D', 'C'], ['D', 'C'], ['D']]
    #frequency_dict = {'A':4, 'B':1, 'C':100, 'D':9}# 'F':3, 'H':0}
    #labels = [['A', 'B', 'D'], ['D', 'B', 'F'], ['F', 'B'], ['B'], ['H'], ['C']]
    #labels = [['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['H'], ['A', 'B', 'D']]
    k = 2
    list_of_all_labels = ['A', 'B', 'C', 'D']
    mlknn_jrs = MlKnnJrs(distances, labels, k, list_of_all_labels)
    print "mlknn_jrs.mlknn.c", mlknn_jrs.mlknn.c
    print "mlknn_jrs.mlknn.c_prim", mlknn_jrs.mlknn.c_prim
    
    print mlknn_jrs.classify([3, 2, 5, 1, 3])