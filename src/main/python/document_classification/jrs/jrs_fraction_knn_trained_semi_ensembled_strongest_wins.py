'''
Created on Mar 21, 2012

@author: mlukasik
'''
from __future__ import division
from collections import defaultdict
from jrs_knn_multilabel import knn_repetitions_multilabel, count_distinct_objects
from jrs_fraction_knn_trained import FractionKnnJrsTrained

def PRINTER(x):
    print '[FractionKnnJrsTrainedSemiEnsembledStrongestWins] '+x

class FractionKnnJrsTrainedSemiEnsembledStrongestWins(object):
    '''
    As FractionKnnJrsTrained, but calculates thresholds for more than 1 k (k1, k2, ...), 
    preferably up to k3. The fraction knns are ranked according to the f-measure per class.
    
    The intuition is similar to using a few density estimators at once.
    
    Also, it uses a normal knn with ranked neighbours, in case no etiquette is returned by Fractions.
    
    distances - list of distances is assumed to be symmetric with smallest distance
        between object and itself!
    
    k_list - list of k parameters
    '''

    
    def __init__(self, distances, records, train_labels, k_list, list_of_all_labels):
        '''
        distances - list of lists of distances
            for example distance between x and y: distances[x][y].
            
        k_list - list of k parameters
        
        min_weight - minimum weight that has to be assigned to a label to take it
        
        NOTE: it can be implemented more efficiently, by not calling KNN k_list times, but once instead when
            having sorted elements by their distance.
        '''
        self.k_list = k_list
        self.train_labels = train_labels
        self.list_of_all_labels = list_of_all_labels
        
        self.classifiers = []
        for k in k_list:
            self.classifiers.append(FractionKnnJrsTrained(distances, records, train_labels, k, list_of_all_labels))
            
        label2fmeasures = {}
        for classifier in self.classifiers:
            for l,f1 in classifier.fmeasure_per_class.iteritems():
                f1list = label2fmeasures.get(l,[])
                f1list.append(f1)
                label2fmeasures[l] = f1list
        import jrs_io                
        for label,fmeasures in label2fmeasures.iteritems(): 
            line = str(label)+" "+str(max(fmeasures))
            jrs_io.file_append_line("jrs_fraction_knn_the_strongest_labelfmeasures.txt", line)                
                
        print f1list
            

    def classify(self, sample_distances):
        label_per_certainty = defaultdict(lambda: (False, -1))
        for classifier in self.classifiers:
            labels_guessed = set(classifier.classify(sample_distances))
            for label in self.list_of_all_labels:
                if label_per_certainty[label][1] < classifier.fmeasure_per_class[label]:
                    label_per_certainty[label] = (label in labels_guessed, classifier.fmeasure_per_class[label])
        
        #PRINTER('[classify]:------------------------------------')
        #PRINTER('[classify]: '+str(dict(label_per_certainty)))
        #PRINTER('[classify]:------------------------------------')
        return [label for label, (take_it, weight) in label_per_certainty.iteritems() if take_it]

        
if __name__ == "__main__":
    
    distances = [[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 0, 1, 2], [3, 2, 1, 0, 1], [4, 3, 2, 1, 0]]
    labels = [['A', 'B'], ['A', 'C'], ['D', 'C'], ['D', 'C'], ['D']]
    #frequency_dict = {'A':4, 'B':1, 'C':100, 'D':9}# 'F':3, 'H':0}
    #labels = [['A', 'B', 'D'], ['D', 'B', 'F'], ['F', 'B'], ['B'], ['H'], ['C']]
    #labels = [['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['H'], ['A', 'B', 'D']]
    k = 2
    list_of_all_labels = ['A', 'B', 'C', 'D']
    mlknn_jrs = FractionKnnJrsTrainedSemiEnsembledStrongestWins(distances, xrange(len(distances)), labels, [1, 2, 3], list_of_all_labels)
    
    print mlknn_jrs.classify([3, 2, 5, 1, 3])