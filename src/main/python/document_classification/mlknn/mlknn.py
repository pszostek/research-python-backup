'''
Created on Dec 26, 2011

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

class MlKnn(object):
    '''
    Naive Bayes with KNN as features.
    
    A classifier based on a publication: 
    Ml-knn: A Lazy Learning Approach to Multi-Label Learning 
    Min-Ling Zhang, Zhi-Hua Zhou.
    
    Processing of the whole dataset is being performed in order to 
    calculate a priori and a posteriori probabilities.
    '''


    def __init__(self, tobjects, distance, find_closest_points, k, smoothing_param, get_labels_of_record):
        '''
        Constructor.
        
        @type tobjects: list of training objects
        @param tobjects: used to calculate parameters (probabilities)
            and nearest neighbours amongst the training objects it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific tobjects parameter
            
        @type distance: object that contains a method of signature: distance(rec1, rec2)
        @param distance: returns distance measure between rec1 and rec2
        
        @type find_closest_points: function of signature:
            find_closest_points(sample, objects, excluding, how_many, distance)
        @param distance: finding closest points for sample amongst the objects,
        
        @type k: integer
        @param k: no. of neighbours taken into consideration
        
        @type k: smoothing_param
        @param smoothing_param - min number of occurences of each label = as in the algorithm
        
        @type get_labels_of_record: function
        @param get_labels_of_record: returns list of labels assigned to a record
        
        '''
        self.tobjects = tobjects#list(tobjects())
        self.distance = distance
        self.find_closest_points = find_closest_points
        self.k = k
        self.smoothing_param = smoothing_param
        self.get_labels_of_record = get_labels_of_record
        self.labels = find_all_labels(self.tobjects, self.get_labels_of_record)
        PRINTER('[MlKnn: init] labels: '+str(self.labels))
        self.threshold = self.init_zero_thresholds(self.labels)
        #compute the probabilities:
        self.labelprobabilities, self.labelcounterprobabilities = self.__get_label_probabilities()
        self.posteriorprobabilities = self.__get_posterior_probabilities()
    
    #-------------------------------------------TRAINING-----------------------------------------------#
    def init_zero_thresholds(self, labels):
        '''
        Initialize a dictionary, mapping each label into 0.
        '''
        threshold = {}
        for label in labels:
            threshold[label] = 0
        return threshold 
    
    def __get_label_probabilities(self):
        '''
        Calculates label occurences probabilities.
        
        TESTED.
        '''
        d = {}#label probabilities
        elems_cnt = 0
        
        for r in self.tobjects:
            for code in self.get_labels_of_record(r):
                try:
                    d[code]+=1
                except:
                    d[code]=1+self.smoothing_param
            elems_cnt+=1
        
        df = {}#label counter probabilities
        for k, v in d.iteritems():
            d[k] = v/(self.smoothing_param*2 + elems_cnt)
            df[k] = 1-d[k]
        return d, df
    
    def __get_posterior_probabilities(self):
        '''
        Computing the posterior probabilities P (Ej |Hb ).
        
        Names of data structures reflect the names used in the article 
        (see comment for the class).
        
        TESTED.
        '''
        #preperation
        c = {}
        c_prim = {}
        for label in self.labels:
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
                PRINTER("[Mlknn.__get_posterior_probabilities]: training in step: "+str(elem_cnt))
            
            d = defaultdict(lambda: 0)
            #NOTE: it is important to allow repetitions in the method called below
            #earlier there was: list(set(self.classify_stupid(r)))
            #and it is wrong because it deletes repetitions!
            for code in self.classify_stupid(r):
                d[code]+=1
            for code in self.labels:
                if code in labels_codes:
                    if d[code] <= self.k:
                        c[code][d[code]] += 1
                    else:
                        c[code][self.k+1] += 1
                else:
                    if d[code] <= self.k:
                        c_prim[code][d[code]] += 1
                    else:
                        c_prim[code][self.k+1] += 1
        
        #compute the final values:
        peh = {}
        for code in self.labels:
            peh[code] = {}
            for i in xrange(self.k+2):
                peh[code][i] = {}
                
        for code in self.labels:
            sum_c = sum(c[code].itervalues())
            sum_c_prim = sum(c_prim[code].itervalues())
            for i in xrange(self.k+2):
                peh[code][i][True] = (self.smoothing_param + c[code][i])/(self.smoothing_param * (self.k + 2) + sum_c)
                peh[code][i][False] = (self.smoothing_param + c_prim[code][i])/(self.smoothing_param * (self.k + 2) + sum_c_prim) 
        
        #save the counts to the classifier, so that it is possible to investigate the 
        #properties of these counts
        self.c = c
        self.c_prim = c_prim
        
        return peh
    
    def get_unnormalized_probabilities_for_class(self, sample, code, neigh_of_code):
        '''
        Returns the unnormalized probabilities for a sample being a code and not being a code.
        In Bayes algorithm it suffices to compare them to get the answer wether to assign
        the code or not.
        '''
        tproba = self.labelprobabilities[code]*self.posteriorprobabilities[code][neigh_of_code][True]
        fproba = self.labelcounterprobabilities[code]*self.posteriorprobabilities[code][neigh_of_code][False]
        return tproba, fproba

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
        #for each code determine wether it is describing the sample or not:
        for code in self.labels:
            tproba, fproba = self.get_unnormalized_probabilities_for_class(sample, code, neigh_codes.get(code, 0))
            #IDEA: zrobic tutaj tproba/fproba > trained_value_on_validation_set
            if tproba>fproba+self.threshold[code]:
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