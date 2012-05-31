'''
Created on April, 07, 2011

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

class MlKnnFractional(object):
    '''
    @deprecated: use MlknnThreshold instead.
    
    Naive Bayes with KNN as features.
    
    Modification of a classifier based on a publication: 
    Ml-knn: A Lazy Learning Approach to Multi-Label Learning 
    Min-Ling Zhang, Zhi-Hua Zhou.
    
    A threshold is being chosen for each class, maximizing the f-measure.
    
    Processing of the whole dataset is being performed in order to 
    calculate a priori and a posteriori probabilities.
    '''

    def __init__(self, tobjects, distance, find_closest_points, k, 
                 get_labels_of_record):
        '''
        Constructor.
        
        @type tobjects: list of records
        @param tobjects: used to calculate parameters (probabilities)
            and nearest neighbours amongst the records it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific tobjects parameter
            
        @type distance: object that contains a method of signature: distance(rec1, rec2)
        @param distance: returns distance measure between rec1 and rec2
        
        @type find_closest_points: function of signature:
            find_closest_points(sample, records, excluding, how_many, distance)
        @param distance: finding closest points,
        
        @type k: integer
        @param k: no. of neighbours taken into consideration
        
        @type get_labels_of_record: function
        @param get_labels_of_record: returns list of labels assigned to a record
        
        '''
        self.tobjects = tobjects()
        self.distance = distance
        self.find_closest_points = find_closest_points
        self.k = k
        self.get_labels_of_record = get_labels_of_record
        self.list_of_all_labels = find_all_labels(self.tobjects, self.get_labels_of_record)
        
        #compute the counts:
        self.c, self.c_prim = self.__calculate_label_counts()
        self.fraction_knn_thresholds, self.fmeasure_per_class = self.__calculate_thresholds()
        #print '[MlKnnFractional: init] '+str(k)+', self.fraction_knn_thresholds: ', self.fraction_knn_thresholds
        #print '[MlKnnFractional: init] '+str(k)+', self.fmeasure_per_class: ', self.fmeasure_per_class
        
    def __calculate_label_counts(self):
        '''
        Calculate label counts in neighbourhood in the training set.
        (Leave one out method).
        
        '''
        #preparation
        c = {}
        c_prim = {}
        for label in self.list_of_all_labels:
            c[label] = {}
            c_prim[label] = {}
            for i in xrange(self.k+2):
                #number of elements of a given label which have i neighbours of a given label
                c[label][i] = 0
                c_prim[label][i] = 0
        
        #for each record compute
        elem_cnt = 0
        for r in self.tobjects:
            labels_codes = self.get_labels_of_record(r)
            #print "labels_codes:", labels_codes
            elem_cnt+=1
            if elem_cnt%100 == 1:
                PRINTER("[MlKnnFractional.__get_posterior_probabilities]: training in step: "+str(elem_cnt))
                
            d = defaultdict(lambda: 0)
            #NOTE: it is important to allow repetitions in the method called below
            #earlier there was: list(set(self.classify_stupid(r)))
            #and it is wrong because it deletes repetitions!
            for code in self.classify_stupid(r):
                d[code]+=1
            for code in self.list_of_all_labels:
                if code in labels_codes:
                    #PRINTER("[Mlknn.__get_posterior_probabilities]: adding to c: "+str(code)+" "+ str(d[code]))
                    if d[code] <= self.k:
                        c[code][d[code]] += 1
                    else:
                        c[code][self.k+1] += 1
                else:
                    if d[code] <= self.k:
                        c_prim[code][d[code]] += 1
                    else:
                        c_prim[code][self.k+1] += 1

        #save the counts to the classifier, so that it is possible to investigate the 
        #properties of these counts
        return c, c_prim
    
    def __calculate_thresholds(self):
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
            max_key = max(max(self.c[label].iterkeys()), max(self.c_prim[label].iterkeys())) 
            
            #for each possible threshold:
            for thresh in xrange(max_key+1):
                #if there is at least this many neighbours, treat a sample as of this class
                #print "-[MLKNNFRACTIONAL]considering thresh: ", thresh
                TP = sum([self.c[label][i] for i in xrange(thresh, max_key+1)])
                FP = sum([self.c_prim[label][i] for i in xrange(thresh, max_key+1)])
                FN = sum([self.c[label][i] for i in xrange(0, thresh)])
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
                
                if sum(self.c[label].itervalues()) != TP + FN:
                    print "BLAD w [calculate_fraction_knn_thresholds]: sum(label_counts[label]['c'][i]) != TP + FN"
                    print 'label:', label
                    print 'label_counts[label][c]', self.c[label]
                    print 'label_counts[label][c_prim]', self.c_prim[label]
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
        return fraction_knn_thresholds, fmeasure_per_class

    def count_neighbours_per_code(self, sample):
        '''
        Counts number of neighbours amongst the self.k nearest neighbours per a code.
        '''
        neigh_codes = {}
        #count neighbouring codes
        for code in self.classify_stupid(sample):#list(set(self.classify_stupid_no_exclude(sample))):
            if code not in neigh_codes:
                neigh_codes[code]=1
            elif neigh_codes[code] < self.k+1:
                neigh_codes[code]+=1
        return neigh_codes
    
    def classify(self, sample):
        '''
        Classify sample using KNN with use of precomputed probabilities. Return labels of closest points.
        
        '''
        answer = []
        neigh_codes = self.count_neighbours_per_code(sample)
        #print '[MLKNNFRACTIONAL] neigh_codes:', neigh_codes
        #for each code determine wether it is describing the sample or not:
        for code in self.list_of_all_labels:
            #print '[MLKNNFRACTIONAL] code neigh_codes.get(code, 0), self.fraction_knn_thresholds[code]', code, neigh_codes.get(code, 0), self.fraction_knn_thresholds[code]
            if neigh_codes.get(code, 0) > self.fraction_knn_thresholds[code]:
                answer.append(code)
        return answer
            
    def classify_stupid_raw(self, sample):
        '''
        Classify element using KNN without use of precomputed probabilities. Return closest points.
        Note: user is supposed to extract labels by himself.
        
        '''
        return self.find_closest_points(sample, self.tobjects, [sample], self.k, self.distance.distance)

    def classify_stupid(self, sample):
        '''
        Classify element using KNN without use of precomputed probabilities. Return labels of closest points.
        Note: codes may occur several times, which is REQUIRED from this method if this reflects the truth.
        
        '''
        labels_assigned = self.classify_stupid_raw(sample)
        if len(labels_assigned)==0:
            return []
        return reduce(lambda a, b: a+b, map(lambda x: self.get_labels_of_record(x), labels_assigned))

    def classify_stupid_raw_no_exclude(self, sample):
        '''
        Classify element using KNN without use of precomputed probabilities and without excluding any points
        from the training set. Return closest points.
        Note: user is supposed to extract labels by himself.
        
        '''
        
        return self.find_closest_points(sample, self.tobjects, [], self.k, self.distance.distance)

    def classify_stupid_no_exclude(self, sample):
        '''
        Classify element using KNN without use of precomputed probabilities and without excluding any points. 
        Return labels of closest points.
        Note: codes may occur several times, which is REQUIRED from this method if this reflects the truth.
        
        '''
        closest_samples = self.classify_stupid_raw_no_exclude(sample)
        return reduce(lambda a, b: a+b, map(lambda x: self.get_labels_of_record(x), closest_samples))