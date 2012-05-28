'''
Created on May 24, 2012

@author: mlukasik
'''
from __future__ import division
import mlknn_skeleton

class MlknnBasic(mlknn_skeleton.MlknnSkeleton):
    '''
    Naive Bayes with KNN as features.
    
    A classifier based on a publication: 
    Ml-knn: A Lazy Learning Approach to Multi-Label Learning 
    Min-Ling Zhang, Zhi-Hua Zhou.
    
    Processing of the whole dataset is being performed in order to 
    calculate a priori and a posteriori probabilities.
    '''


    def __init__(self, tobjects, find_nearest_neighbours, k, smoothing_param, get_labels, kernel, printer):
        '''
        Constructor.
        
        @type tobjects: list of training objects
        @param tobjects: used to calculate parameters (probabilities)
            and nearest neighbours amongst the training objects it returns;
            NOTE: if a user wants to manipulate, which codes to consider(e.g. higher or lower level) 
            it is good to give a specific tobjects parameter
        
        @type find_nearest_neighbours: function of signature:
            find_nearest_neighbours(sample, objects, excluding, how_many, distance)
        @param distance: finding closest points for sample amongst the objects,
        
        @type k: integer
        @param k: no. of neighbours taken into consideration
        
        @type k: smoothing_param
        @param smoothing_param - min number of occurences of each label = as in the algorithm
        
        @type get_labels: function
        @param get_labels: returns list of labels assigned to a record
        
        @type kernel: function
        @param kernel: returns the importance measure of a neighour of given ordinal number
        
        @type printer: function
        @param printer: prints important steps of algorithms
        '''
        self.tobjects = tobjects
        self.find_nearest_neighbours = find_nearest_neighbours
        self.k = k
        self.smoothing_param = smoothing_param
        self.get_labels = get_labels
        self.kernel = kernel
        self.printer = printer
        
        #find labels:
        self.labels = super(MlknnBasic, self).find_all_labels(self.tobjects, self.get_labels)
        self.printer(str(self.labels))
        
        #compute the probabilities:
        self.labelprobabilities, self.labelcounterprobabilities = self.__get_label_probabilities()
        c, c_prim = super(MlknnBasic, self).calculate_label_counts(self.tobjects, self.labels, 
                                                                   self.find_nearest_neighbours,
                                                                   self.get_labels, self.kernel, self.printer)
        print "[MlknnBasic] c, c_prim:", c, c_prim
        self.posteriorprobabilities_true, self.posteriorprobabilities_false = self.__get_posterior_probabilities(c, c_prim)

#-------------------------------------------TRAINING-----------------------------------------------#
    def __get_label_probabilities(self):
        '''
        Calculates label occurences probabilities.
        '''
        d = {}#label probabilities
        elems_cnt = 0
        
        for r in self.tobjects:
            for code in self.get_labels(r):
                d[code] = d.get(code, self.smoothing_param)+1
            elems_cnt+=1
        
        df = {}#label counter probabilities
        for k, v in d.iteritems():
            d[k] = v/(self.smoothing_param*2 + elems_cnt)
            df[k] = 1-d[k]
        return d, df
    
    def __get_posterior_probabilities(self, c, c_prim):
        '''
        Computing the posterior probabilities P (Ej |Hb ).
        
        Names of data structures reflect the names used in the article 
        (see comment for the class).
        '''
        peh_true = {}
        peh_false = {}
        for code in self.labels:
            peh_true[code] = {}
            peh_false[code] = {}
                
        for code in self.labels:
            sum_c = sum(c[code].itervalues())
            sum_c_prim = sum(c_prim[code].itervalues())
            for i in c[code].iterkeys():
                peh_true[code][i] = (self.smoothing_param + c[code][i])/(self.smoothing_param * (self.k + 2) + sum_c)
            for i in c_prim[code].iterkeys():
                peh_false[code][i] = (self.smoothing_param + c_prim[code][i])/(self.smoothing_param * (self.k + 2) + sum_c_prim) 
        
        return peh_true, peh_false
    
#-------------------------------------------CLASSIFYING-----------------------------------------------#
    def get_unnormalized_probabilities_for_class(self, sample, code, neighbouring_value):
        '''
        Returns the unnormalized probabilities for a sample being a code and not being a code.
        In Bayes algorithm it suffices to compare them to get the answer wether to assign
        the code or not.
        '''
        tproba = self.labelprobabilities[code]*self.posteriorprobabilities_true[code][neighbouring_value]
        fproba = self.labelcounterprobabilities[code]*self.posteriorprobabilities_false[code][neighbouring_value]
        return tproba, fproba
    
    def classify(self, sample):
        '''
        Classify sample using KNN with use of precomputed probabilities. Return labels of closest points.
        '''
        result = []
        neighs_per_code = self.count_neighbours_per_code(sample)
        #for each code determine wether it is describing the sample or not:
        for code in self.labels:
            tproba, fproba = self.get_unnormalized_probabilities_for_class(sample, code, neighs_per_code.get(code, 0))
            #IDEA: zrobic tutaj tproba/fproba > trained_value_on_validation_set
            if tproba>fproba:
                result.append(code)
        return result