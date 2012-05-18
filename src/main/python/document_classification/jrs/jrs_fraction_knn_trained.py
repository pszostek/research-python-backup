'''
Created on Mar 24, 2012

@author: mlukasik
'''
from __future__ import division
from collections import defaultdict
from jrs_knn_multilabel import knn_repetitions_multilabel, count_distinct_objects
from itertools import izip

def PRINTER(x):
    print '[FractionKnnJrsTrained] '+x
    #pass

class FractionKnnJrsTrained(object):
    '''
    For each label adjusts the threshold 
    (a fraction of all the nearest neighbours that has to be of that class) 
    on the training set.
    
    distances - list of distances is assumed to be symmetric with smallest distance
        between object and itself!
    records - which indices are to be considered from distances
    '''

    
    def __init__(self, distances, records, train_labels, k, list_of_all_labels):
        '''
        distances - list of lists of distances
            for example distance between x and y: distances[x][y].
        records - which indices are to be considered from distances
        '''
        #PRINTER('distances, records, train_labels '+str(distances)+" "+str(records)+" "+str(train_labels))

        self.k = k
        self.train_labels = train_labels
        self.list_of_all_labels = list_of_all_labels
        self.records = records
        
        label_counts = self.calculate_label_counts(distances, records, train_labels, k, list_of_all_labels)
        #PRINTER('label_counts: ')
        #for label in label_counts:
            #PRINTER('label_counts[label][c] '+label+' '+str(label_counts[label]['c']))
            #PRINTER('label_counts[label][c_prim] '+label+' '+str(label_counts[label]['c_prim']))
            
        #find threshold per class:
        self.fraction_knn_thresholds, self.fmeasure_per_class, self.precision_per_class, self.recall_per_class, self.representants_per_class = self.calculate_fraction_knn_thresholds(label_counts) 
        
        PRINTER('-----------------------------------------')
        PRINTER('FRACTION KNN WITH K: '+str(self.k))
        PRINTER('SHOWING STATISTICS PER CLASS')
        #for thresh, f1, prec, recall, representants in izip(self.fraction_knn_thresholds, self.fmeasure_per_class, self.precision_per_class, self.recall_per_class, self.representants_per_class):
        for key in sorted(self.representants_per_class.iterkeys()):
            PRINTER('Label: '+str(key))
            PRINTER('Fraction knn threshold: '+str(self.fraction_knn_thresholds[key]))
            PRINTER('Precision: '+str(self.precision_per_class[key]))
            PRINTER('Recall: '+str(self.recall_per_class[key]))
            PRINTER('Fmeasure: '+str(self.fmeasure_per_class[key]))
            PRINTER('Representants: '+str(self.representants_per_class[key]))
        PRINTER('-----------------------------------------')

    def calculate_label_counts(self, distances, records, train_labels, k, list_of_all_labels):
        '''
        Calculates the label counts c and c_prim.
        '''
        #init c and c' per a class:
        label_counts = {}
        for label in list_of_all_labels:
            label_counts[label] = {'c': defaultdict(lambda: 0), 'c_prim': defaultdict(lambda: 0)}
        
        #find c and c' per a class:
        for ind in records:
            distance_vector = distances[ind]
            #print "ind, distance_vector, train_labels[ind], k, train_labels:", ind, distance_vector, train_labels[ind], k, train_labels
            labels = knn_repetitions_multilabel(distance_vector, records, train_labels, k+1)#k+1 because we will consider the sample itself
            neigh_counts = count_distinct_objects(labels)
            #substract all the labels of the sample being classified
            for self_label in train_labels[ind]:
                neigh_counts[self_label]-=1
            
            oracle_ans = set(train_labels[ind])
            
            for label in list_of_all_labels:
                #label in oracle labelling:
                if label in oracle_ans:
                    label_counts[label]['c'][neigh_counts.get(label, 0)] += 1
                #label NOT in oracle labelling:
                else:
                    label_counts[label]['c_prim'][neigh_counts.get(label, 0)] += 1
        return label_counts

    def calculate_fraction_knn_thresholds(self, label_counts):
        '''
        Calculates the fraction, how many times a label has to occur to decide about it.
        The decision is made by maximizing the f-measure on training data.
        '''
        fraction_knn_thresholds = {}
        fmeasure_per_class = {}
        precision_per_class = {}
        recall_per_class = {}
        representants_per_class = {}
        #for each label
        for label in self.list_of_all_labels:
            print "considering label: ", label
            #for each possible threshold:
            best_thresh = -1
            best_fmeasures_precision = -1
            best_fmeasures_recall = -1
            best_fmeasure = -1
            try:
                max_key_c = max(label_counts[label]['c'].iterkeys())
                try:
                    max_key_c_prim = max(label_counts[label]['c_prim'].iterkeys())
                except:
                    max_key_c_prim = 0
                max_key = max(max_key_c, max_key_c_prim)
            except:
                print '[calculate_fraction_knn_thresholds] ERROR in max(max(...'
                print 'label_counts[label][c].iterkeys():', dict(label_counts[label]['c'])
                print 'label_counts[label][c_prim].iterkeys():', dict(label_counts[label]['c_prim'])
                print 'label:', label
                print 'self.k:', self.k
                
                import sys
                sys.exit(1)
            
            for thresh in xrange(1, (max_key)+1):
                print "-considering thresh: ", thresh
                print "-list corresponding to TP: ", range(thresh, max_key+1)
                print "-list corresponding to FP: ", range(thresh, max_key+1)
                print "-list corresponding to FN: ", range(0, thresh)
                TP = sum([label_counts[label]['c'][i] for i in xrange(thresh, max_key+1)])
                FP = sum([label_counts[label]['c_prim'][i] for i in xrange(thresh, max_key+1)])
                FN = sum([label_counts[label]['c'][i] for i in xrange(0, thresh)])
                print "-TP, FP, FN:", TP, FP, FN
                
                precision = 0
                if (TP+FP)>0:
                    precision = TP/(TP+FP)
                recall = 0
                if (TP+FN)>0:
                    recall = TP/(TP+FN)
                fmeasure = 0
                if (precision+recall)>0:
                    fmeasure = 2*precision*recall/(precision+recall)
                print "-precision, recall, fmeasure:", precision, recall, fmeasure
                
                if fmeasure > best_fmeasure:
                    best_thresh = thresh
                    best_fmeasure = fmeasure
                    best_fmeasures_precision = precision
                    best_fmeasures_recall = recall
                
                if sum(label_counts[label]['c'].itervalues()) != TP + FN:
                    print "BLAD w [calculate_fraction_knn_thresholds]: sum(label_counts[label]['c'][i]) != TP + FN"
                    
                    print 'label_counts[label][c]', label_counts[label]['c']
                    print 'label_counts[label][c_prim]', label_counts[label]['c_prim']
                    print 'thresh:', thresh
                    print 'TP:', TP
                    print 'FN:', FN
                    print 'FP:', FP
                    
                    print 'self.k:', self.k
                    print 'max_key:', max_key
                    
                    import sys
                    sys.exit(1)
                
                representants_per_class[label] = TP + FN
            
            fraction_knn_thresholds[label] = best_thresh  
            fmeasure_per_class[label] = best_fmeasure  
            precision_per_class[label] = best_fmeasures_precision  
            recall_per_class[label] = best_fmeasures_recall
            
        return fraction_knn_thresholds, fmeasure_per_class, precision_per_class, recall_per_class, representants_per_class

    def classify(self, sample_distances):
        nearest_labels = knn_repetitions_multilabel(sample_distances, self.records, self.train_labels, self.k)
        neigh_counts = count_distinct_objects(nearest_labels)
        
        result = []
        #for each label check the threshold:
        for label in self.list_of_all_labels:
            PRINTER('[classify]: condidering label, neigh_counts[label],  self.fraction_knn_thresholds[label] '+
                    str(label)+", "+str(neigh_counts[label])+", "+str(self.fraction_knn_thresholds[label]))
            if neigh_counts[label] >= self.fraction_knn_thresholds[label]:
                result.append(label)
        PRINTER('[classify]: result '+str(result))
        return result

if __name__ == "__main__":
    
    distances = [[0, 1, 2, 3, 4], [1, 0, 1, 2, 3], [2, 1, 0, 1, 2], [3, 2, 1, 0, 1], [4, 3, 2, 1, 0]]
    labels = [['A', 'B'], ['A', 'C'], ['D', 'C'], ['D', 'C'], ['D']]
    #frequency_dict = {'A':4, 'B':1, 'C':100, 'D':9}# 'F':3, 'H':0}
    #labels = [['A', 'B', 'D'], ['D', 'B', 'F'], ['F', 'B'], ['B'], ['H'], ['C']]
    #labels = [['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['H'], ['A', 'B', 'D']]
    k = 2
    list_of_all_labels = ['A', 'B', 'C', 'D']
    mlknn_jrs = FractionKnnJrsTrained(distances, xrange(len(distances)), labels, k, list_of_all_labels)
    print mlknn_jrs.fmeasure_per_class
    print mlknn_jrs.classify([3, 2, 5, 1, 3])