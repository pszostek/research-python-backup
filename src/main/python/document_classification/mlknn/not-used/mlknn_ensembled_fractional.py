'''
Created on April, 07, 2012

@author: mlukasik

MLKNN classifier.
'''
from __future__ import division
from collections import defaultdict
from find_all_labels import find_all_labels

def PRINTER(x):
    #pass
    import logging
    logging.info(x)

class MlKnnFractionalEnsembledStrongest(object):
    '''
    Naive Bayes with KNN as features.
    
    Modification of a classifier based on a publication: 
    Ml-knn: A Lazy Learning Approach to Multi-Label Learning 
    Min-Ling Zhang, Zhi-Hua Zhou.
    
    A threshold is being chosen for each class, maximizing the f-measure.
    
    Ensemble of such MlKnn's is created - strongest' vote in terms of f-measures is
    chosen.
    
    Processing of the whole dataset is being performed in order to 
    calculate a priori and a posteriori probabilities.
    '''

    def __init__(self, frecords, distance, find_closest_points, k_list, 
                 get_labels_of_record):
        '''
        Constructor.
        
        @type frecords: list of records
        @param frecords: used to calculate parameters (probabilities)
            and nearest neighbours amongst the records it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific frecords parameter
            
        @type distance: object that contains a method of signature: distance(rec1, rec2)
        @param distance: returns distance measure between 2 records
        
        @type find_closest_points: function of signature:
            find_closest_points(sample, records, excluding, how_many, distance);
            It returns training objects which are closest to the sample, in a sorted form, increasing
            order in terms of their distance from sample.
        @param distance: finding closest points,
        
        @type k_list: list of integers
        @param k_list: list of no. of neighbours taken into consideration
        
        @type get_labels_of_record: function
        @param get_labels_of_record: returns list of labels assigned to a record
        
        '''
        self.frecords = list(frecords())#TODO: zrobic podawanie listy skoro i tak robi sie liste z tego!
        self.distance = distance
        self.find_closest_points = find_closest_points
        self.k_list = k_list
        self.k_max = max(k_list)
        PRINTER('[MlKnnFractionalEnsembledStrongest: init] max k: '+str(self.k_max))
        self.get_labels_of_record = get_labels_of_record
        
        self.list_of_all_labels = find_all_labels(self.frecords, self.get_labels_of_record)
        PRINTER('[MlKnnFractionalEnsembledStrongest: init] labels: '+str(self.list_of_all_labels))
        
        #compute the counts of the form c[k][label][i] 
        #<- how many times for k, label i-neighbouring codes codes have the same label:
        self.c, self.c_prim = self.__calculate_label_counts()
        
        self.fraction_knn_thresholds = {}
        self.fraction_knn_fmeasures = {}
        for k in self.k_list:
            self.fraction_knn_thresholds[k], self.fraction_knn_fmeasures[k] = self.__calculate_thresholds(self.c[k], self.c_prim[k])
        
    def __calculate_label_counts(self):
        '''
        Calculate label counts in neighbourhood in the training set.
        (Leave one out method).
        
        '''
        #preparation
        c = {}
        c_prim = {}
        for k in self.k_list:
            c[k] = {}
            c_prim[k] = {}
            for label in self.list_of_all_labels:
                c[k][label] = {}
                c_prim[k][label] = {}
                for i in xrange(k+2):
                    #number of elements of a given label which have i neighbours of a given label
                    c[k][label][i] = 0
                    c_prim[k][label][i] = 0
        
        #for each record compute
        elem_cnt = 0
        for r in self.frecords:
            print '[__calculate_label_counts]: record:', r
            labels_codes = self.get_labels_of_record(r)
            #print "labels_codes:", labels_codes
            elem_cnt+=1
            if elem_cnt%100 == 1:
                PRINTER("[MlKnnFractionalEnsembledStrongest.__get_posterior_probabilities]: training in step: "+str(elem_cnt))
                
            #NOTE: it is important to allow repetitions in the method called below
            #earlier there was: list(set(self.classify_stupid(r)))
            #and it is wrong because it deletes repetitions!
            k_max_neighbours = self.classify_stupid_raw(r, self.k_max)
            print '-[__calculate_label_counts]:k_max_neighbours:', k_max_neighbours
            
            for k in self.k_list:
                #here we store how many records from the neighbours have each of the codes that have been assigned to r
                d = defaultdict(lambda: 0)
                print '--[__calculate_label_counts]:neighbours for k:', k, "self.convert_records2labels(k_max_neighbours)[:k]:", self.convert_records2labels(k_max_neighbours)[:k]
                for code in self.convert_records2labels(k_max_neighbours)[:k]:
                    d[code]+=1
                for code in self.list_of_all_labels:
                    if code in labels_codes:
                        #PRINTER("[Mlknn.__get_posterior_probabilities]: adding to c: "+str(code)+" "+ str(d[code]))
                        if d[code] <= k:
                            c[k][code][d[code]] += 1
                        else:
                            c[k][code][k+1] += 1
                    else:
                        if d[code] <= k:
                            c_prim[k][code][d[code]] += 1
                        else:
                            c_prim[k][code][k+1] += 1

        #save the counts to the classifier, so that it is possible to investigate the 
        #properties of these counts
        return c, c_prim
    
    def __calculate_thresholds(self, c, c_prim):
        '''
        Compute the thresholds, maximizing f-measure.
        '''
        fraction_knn_thresholds = {}
        fmeasure_per_class = {}
        precision_per_class = {}
        recall_per_class = {}
        representants_per_class = {}
        #for each label
        for label in self.list_of_all_labels:
            #print "[MLKNNFRACTIONAL]: considering label: "+label
            best_thresh = -1
            best_fmeasures_precision = -1
            best_fmeasures_recall = -1
            best_fmeasure = -1
            
            #how many iterations have to be performed:
            max_key = max(max(c[label].iterkeys()), max(c_prim[label].iterkeys())) 
            
            #for each possible threshold:
            for thresh in xrange(max_key+1):
                #if there is at least this many neighbours, treat a sample as of this class
                #print "-[MLKNNFRACTIONAL]considering thresh: ", thresh
                TP = sum([c[label][i] for i in xrange(thresh, max_key+1)])
                FP = sum([c_prim[label][i] for i in xrange(thresh, max_key+1)])
                FN = sum([c[label][i] for i in xrange(0, thresh)])
                #print "-TP, FP, FN:", TP, FP, FN
                
                precision = 0
                if (TP+FP)>0:
                    precision = TP/(TP+FP)
                recall = 0
                if (TP+FN)>0:
                    recall = TP/(TP+FN)
                fmeasure = 0
                if (precision+recall)>0:
                    fmeasure = 2*precision*recall/(precision+recall)
                #print "-[MLKNNFRACTIONAL]precision, recall, fmeasure:", precision, recall, fmeasure
                
                if fmeasure > best_fmeasure:
                    best_thresh = thresh
                    best_fmeasure = fmeasure
                    best_fmeasures_precision = precision
                    best_fmeasures_recall = recall
                
                if sum(c[label].itervalues()) != TP + FN:
                    print "BLAD w [calculate_fraction_knn_thresholds]: sum(label_counts[label]['c'][i]) != TP + FN"
                    print 'label:', label
                    print 'label_counts[label][c]', c[label]
                    print 'label_counts[label][c_prim]', c_prim[label]
                    print 'thresh:', thresh
                    print 'TP:', TP
                    print 'FN:', FN
                    print 'FP:', FP
                    
                    print 'max_key:', max_key
                    
                    import sys
                    sys.exit(1)
                
                representants_per_class[label] = TP + FN
            
            fraction_knn_thresholds[label] = best_thresh  
            fmeasure_per_class[label] = best_fmeasure  
            precision_per_class[label] = best_fmeasures_precision  
            recall_per_class[label] = best_fmeasures_recall
        return fraction_knn_thresholds, fmeasure_per_class
    
    def count_neighbours_per_code(self, nearest_neighbours):
        '''
        Counts number of neighbours amongst the k nearest neighbours per a code.
        '''
        neigh_codes = {}
        #count neighbouring codes
        for code in nearest_neighbours:#list(set(self.classify_stupid_no_exclude(sample))):
            if code not in neigh_codes:
                neigh_codes[code]=1
            elif neigh_codes[code] < self.k+1:
                neigh_codes[code]+=1
        return neigh_codes
    
    def classify(self, sample):
        '''
        Classify sample using ensemble fractional KNN with use of precomputed probabilities. Return labels of closest points.
        
        '''
        answer = {}
        for code in self.list_of_all_labels:
            answer[code] = {}
            answer[code]['decision'] = False
            answer[code]['certainty'] = 0.0
        
        k_max_neighbours = self.classify_stupid_raw(sample, self.k_max)
        print '[classify]: k_max_neighbours:', k_max_neighbours
        
        for k in self.k_list:
            print '[classify]: k:', k
            neigh_codes = self.count_neighbours_per_code(k_max_neighbours[:k])
            
            print '[classify]: neigh_codes:', neigh_codes
            #for each code determine wether it is describing the sample or not:
            for code in self.list_of_all_labels:
                if self.fraction_knn_fmeasures[k][code] > answer[code]['certainty']:
                    answer[code]['decision'] = code in neigh_codes
                    answer[code]['certainty'] = self.fraction_knn_fmeasures[k][code] 
                    
        return [code for code in self.list_of_all_labels if answer[code]['decision']]
            
    def classify_stupid_raw(self, sample, k):
        '''
        Classify element using KNN without use of precomputed probabilities. Return closest points.
        Note: user is supposed to extract labels by himself.
        
        '''
        return self.find_closest_points(sample, self.frecords, [sample], k, self.distance.distance)

    def convert_records2labels(self, closest_records):
        '''
        Return labels of closest_records.
        Note: codes may occur several times, which is REQUIRED from this method if this reflects the truth.
        
        '''
        if len(closest_records)==0:
            return []
        return reduce(lambda a, b: a+b, map(lambda x: self.get_labels_of_record(x), closest_records))
