'''
Created on May 31, 2012

@author: mlukasik
'''
from __future__ import division
import mlknn_threshold

class MlknnTEnsembled(mlknn_threshold.MlknnThreshold):
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

    def __init__(self, tobjects, find_nearest_neighbours, k_list, get_labels, kernel, printer, 
                 obj_id = 'an', neigh_events = None):#range(k+2)):
        '''
        Constructor.
        
        @type tobjects: list of training objects
        @param tobjects: used to calculate parameters (probabilities)
            and nearest neighbours amongst the training objects it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific tobjects parameter
        
        @type find_nearest_neighbours: function of signature:
            find_nearest_neighbours(sample, objects, excluding, how_many, distance), returning neighbours in sorted order
        @param distance: finding closest points for sample amongst the objects,
        
        @type k_list: list of integers
        @param k_list: consecutive no. of neighbours taken into consideration
        
        @type get_labels: function
        @param get_labels: returns list of labels assigned to a record
        
        @type kernel: function
        @param kernel: returns the importance measure of a neighour of given ordinal number
        
        @type printer: function
        @param printer: prints important steps of algorithms
        '''
        self.tobjects = tobjects
        self.find_nearest_neighbours = find_nearest_neighbours
        self.k_list = k_list
        self.get_labels = get_labels
        self.kernel = kernel
        self.printer = printer
        self.obj_id = obj_id
        self.neigh_events = [range(k+2) for k in k_list]#neigh_events
        if neigh_events:
            self.neigh_events = neigh_events
        self.max_k = max(self.k_list)
        
        #find labels:
        self.labels = super(mlknn_threshold.MlknnThreshold, self).find_all_labels(self.tobjects, self.get_labels)
        self.printer(str(self.labels))
        
        #for each object calculate nearest neighbours in a sorted order
        nearest_neighbours = {}
        for obj in self.tobjects:
            nearest_neighbours[obj[self.obj_id]] = self.find_nearest_neighbours(obj, self.max_k)
        def find_nearest_neighbours_from_list(obj, k):
            return nearest_neighbours[obj[self.obj_id]][:k]
        
        #calculate the counts and threshold scores
        self.c, self.c_prim = {}, {}
        self.fraction_knn_thresholds, self.fmeasure_per_class = {}, {}
        for k in self.k_list:
            self.c[k], self.c_prim[k] = self.calculate_label_counts(self.tobjects, self.labels, 
                                                                   find_nearest_neighbours_from_list, k,
                                                                   self.get_labels, self.kernel, self.printer)
            self.fraction_knn_thresholds[k], self.fmeasure_per_class[k] = self.calculate_thresholds(self.c[k], self.c_prim[k])

        self.code2threshold = {}
        self.code2fmeasure = {}
        self.code2k = {}
        for code in self.labels:
            self.code2threshold[code] = None
            self.code2fmeasure[code] = None
            self.code2k[code] = None
        
        for code in self.labels:
            for k in self.k_list:
                if self.fmeasure_per_class[k][code] > self.code2fmeasure[code]:
                    self.code2fmeasure[code] = self.fmeasure_per_class[k][code]
                    self.code2threshold[code] = self.fraction_knn_thresholds[k][code]
                    self.code2k[code] = k
        
        print "self.code2threshold:", self.code2threshold
        print "self.code2fmeasure:", self.code2fmeasure
        print "self.code2k:", self.code2k
        
#-------------------------------------------CLASSIFYING-----------------------------------------------#
    def classify(self, sample):
        '''
        Classify sample using ensemble fractional KNN.
        
        '''
        answer = []
        nearest_neighbours = self.find_nearest_neighbours(sample, self.max_k)
        def find_nearest_neighbours_from_list(obj, k):
            return nearest_neighbours[:k]
        
        for code in self.labels:
            neigh_codes =  self.count_neighbours_per_code(sample, self.find_nearest_neighbours, self.code2k[code], self.get_labels, self.kernel)
        
            #print '[MLKNNFRACTIONAL] code neigh_codes.get(code, 0), self.fraction_knn_thresholds[code]', code, neigh_codes.get(code, 0), self.fraction_knn_thresholds[code]
            if neigh_codes.get(code, 0) > self.code2threshold[code]:
                answer.append(code)
        return answer