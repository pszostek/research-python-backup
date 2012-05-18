'''
Created on Mar 21, 2012

@author: mlukasik
'''
from __future__ import division
from collections import defaultdict
from jrs_knn_multilabel import knn_repetitions_multilabel, count_distinct_objects
from jrs_fraction_knn_trained import FractionKnnJrsTrained

def PRINTER(x):
    #print '[FractionKnnJrsTrainedSemiEnsembledStrongestWeighted] '+x
    pass

class FractionKnnJrsTrainedSemiEnsembledStrongestWeighted(object):
    '''
    As FractionKnnJrsTrained, but calculates thresholds for more than 1 k (k1, k2, ...), 
    preferably up to k3. The fraction knns are ranked according to the f-measure per class.
    
    The intuition is similar to using a few density estimators at once.
    
    Also, it uses a normal knn with ranked neighbours, in case no etiquette is returned by Fractions.
    
    distances - list of distances is assumed to be symmetric with smallest distance
        between object and itself!
    
    k_list - list of k parameters
    '''

    
    def __init__(self, distances, records, train_labels, k_list, list_of_all_labels, weighting_subset):
        '''
        distances - list of lists of distances
            for example distance between x and y: distances[x][y].
            
        k_list - list of k parameters
        
        weighting_subset - number of elements to be considered when weighting
        
        NOTE: it can be implemented more efficiently, by not calling KNN k_list times, but once instead when
            having sorted elements by their distance.
        '''
        self.k_list = k_list
        self.train_labels = train_labels
        self.list_of_all_labels = list_of_all_labels
        self.weighting_subset = weighting_subset
        
        self.classifiers = []
        for k in k_list:
            self.classifiers.append(FractionKnnJrsTrained(distances, records, train_labels, k, list_of_all_labels))

    def classify(self, sample_distances):
        label_per_certainty = defaultdict(lambda: [])
        for classifier in self.classifiers:
            labels_guessed = set(classifier.classify(sample_distances))
            for label in self.list_of_all_labels:
                label_per_certainty[label].append((classifier.fmeasure_per_class[label], label in labels_guessed))
        
        PRINTER("label_per_certainty: "+str(dict(label_per_certainty)))
        
        result = []
        for label in self.list_of_all_labels:
            important_values = sorted(label_per_certainty[label], key = lambda x: x[0], reverse=True)[:self.weighting_subset]
            PRINTER('IMPORTANT VALUES FOR: '+str(label)+": "+str(important_values))
            smallest_value = important_values[-1][0]#the last value which will be substracted from everything else
            ans = 0
            for value, bool_value in important_values[:-1]:
                if bool_value:
                    ans += value-smallest_value
                else:
                    ans -= value-smallest_value
            if ans > 0:
                result.append(label)
            if ans == 0 and important_values[0][1]==True:
                result.append(label)
        
        return result
        """
        import heapq
        best_matches = {}
        for label in self.list_of_all_labels:
            best_matches[label] = []
        
        PRINTER('---CLASSIFYING---')
        #choose as many elements as needed:
        for classifier in self.classifiers:
            PRINTER('Next classifier..')
            labels_guessed = set(classifier.classify(sample_distances))
            for label in self.list_of_all_labels:
                PRINTER('considering label:'+str(label))
                curr_fmeasure = classifier.fmeasure_per_class[label]
                PRINTER('curr_fmeasure:'+str(curr_fmeasure))
                curr_ans = label in labels_guessed
                PRINTER('curr_ans:'+str(curr_ans))
                if len(best_matches[label]) < self.weighting_subset:
                    heapq.heappush(best_matches[label], (curr_fmeasure, curr_ans))
                    PRINTER('pushing to the heap; now heap for label: '+str(label)+' '+str(best_matches[label]))
                elif curr_fmeasure > best_matches[label][0] :
                    PRINTER('pushing to the heap and popping:'+str(best_matches[label][0]))
                    heapq.heappushpop(best_matches[label], (curr_fmeasure, curr_ans))
                    PRINTER('now heap for label: '+str(label)+' '+str(best_matches[label]))
        
        PRINTER('---SUMMARIZING---')
        #find the answers in a weighted form:
        result = []
        for label in self.list_of_all_labels:
            PRINTER('Considering label: '+str(label)+' with heap: '+str(best_matches[label]))
            min_fmeasure = best_matches[label][0][0]
            PRINTER('min_fmeasure: '+str(min_fmeasure))
            ans = 0
            for curr_fmeasure, curr_ans in best_matches[label]:
                if curr_ans:
                    ans += (curr_fmeasure - min_fmeasure)
                else:
                    ans -= (curr_fmeasure - min_fmeasure)
            
            PRINTER('ans: '+str(ans))
            if ans > 0:
                result.append(label)
            if ans == 0:
                if best_matches[label][1]:
                    result.append(label)
                    
        return result
        """
        
if __name__ == "__main__":
    
    #distances = [[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 0, 1, 2], [3, 2, 1, 0, 1], [4, 3, 2, 1, 0]]
    #labels = [['A', 'B'], ['A', 'C'], ['D', 'C'], ['D', 'C'], ['D']]
    #frequency_dict = {'A':4, 'B':1, 'C':100, 'D':9}# 'F':3, 'H':0}
    #labels = [['A', 'B', 'D'], ['D', 'B', 'F'], ['F', 'B'], ['B'], ['H'], ['C']]
    #labels = [['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['H'], ['A', 'B', 'D']]
    #k = 2
    #k_list = [1, 2, 3]
    #list_of_all_labels = ['A', 'B', 'C', 'D']
    distances = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [1, 0, 1, 2, 3, 4, 5, 6, 7], [2, 1, 0, 1, 2, 3, 4, 5, 6], 
                 [3, 2, 1, 0, 1, 2, 3, 4, 5], [4, 3, 2, 1, 0, 1, 2, 3, 4], [5, 4, 3, 2, 1, 0, 1, 2, 3], 
                 [6, 5, 4, 3, 2, 1, 0, 1, 2], [7, 6, 5, 4, 3, 2, 1, 0, 1], [8, 7, 6, 5, 4, 3, 2, 1, 0]]
    labels = [['A', 'B', 'C'], ['A', 'D', 'C'], ['B', 'D', 'C', 'Z'], ['B', 'C', 'F', 'Z'], ['E', 'F', 'G', 'Z'], 
              ['E', 'H', 'G'], ['H', 'G', 'I'], ['F', 'G', 'I'], ['G']]
    
    k_list = [3, 4, 5, 6]
    list_of_all_labels = set(reduce(lambda x, y: x+y, labels))
    
    mlknn_jrs = FractionKnnJrsTrainedSemiEnsembledStrongestWeighted(distances, xrange(len(distances)), labels, k_list, list_of_all_labels, 3)
    
    print mlknn_jrs.classify([1, 3, 3, 1, 2, 4, 6, 9, 11])
    print mlknn_jrs.classify([111, 113, 113, 111, 2, 4, 1, 1, 11])