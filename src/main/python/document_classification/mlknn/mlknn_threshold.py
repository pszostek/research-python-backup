'''
Created on May 31, 2012

@author: mlukasik
'''
from __future__ import division
import mlknn_skeleton

class MlknnThreshold(mlknn_skeleton.MlknnSkeleton):
    '''
    Naive Bayes with KNN as features.
    
    Modification of a classifier based on a publication: 
    Ml-knn: A Lazy Learning Approach to Multi-Label Learning 
    Min-Ling Zhang, Zhi-Hua Zhou.
    
    A threshold is being chosen for each class, maximizing the f-measure.
    
    Processing of the whole dataset is being performed in order to 
    calculate a priori and a posteriori probabilities.
    '''

    def __init__(self, tobjects, find_nearest_neighbours, k, smoothing_param, get_labels, kernel, printer, 
                 neigh_events = None):#range(k+2)):
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
        self.neigh_events = range(k+2)#neigh_events
        if neigh_events:
            self.neigh_events = neigh_events
        
        #find labels:
        self.labels = super(MlknnThreshold, self).find_all_labels(self.tobjects, self.get_labels)
        self.printer(str(self.labels))
        
        #compute the probabilities:
        self.c, self.c_prim = super(MlknnThreshold, self).calculate_label_counts(self.tobjects, self.labels, 
                                                                   self.find_nearest_neighbours, k,
                                                                   self.get_labels, self.kernel, self.printer)
        self.fraction_knn_thresholds, self.fmeasure_per_class = self.__calculate_thresholds()

#-------------------------------------------TRAINING-----------------------------------------------#
    
    def calculate_thresholds(self, c, c_prim):
        '''
        Compute the thresholds, maximizing f-measure.
        '''
        fraction_knn_thresholds = {}
        fmeasure_per_class = {}
        precision_per_class = {}
        recall_per_class = {}
        representants_per_class = {}
        #for each label
        for label in self.labels:
            #print "[MLKNNFRACTIONAL]: considering label: "+label
            best_thresh = -1
            best_fmeasures_precision = -1
            best_fmeasures_recall = -1
            best_fmeasure = -1
            
            #sorted keys to be checked:
            keys = sorted(set(c[label].iterkeys()) | set(c_prim[label].iterkeys())) 
            
            #for each possible threshold:
            for ind, thresh in enumerate(keys):
                #if there is at least this many neighbours, treat a sample as of this class
                #print "-[MLKNNFRACTIONAL]considering thresh: ", thresh
                TP = sum([c[label].get(i, 0) for i in keys[ind:]])
                FP = sum([c_prim[label].get(i, 0) for i in keys[ind:]])
                FN = sum([c[label].get(i, 0) for i in keys[:ind]])
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
                    print "ERROR in w [calculate_fraction_knn_thresholds]: sum(label_counts[label]['c'][i]) != TP + FN"
                    print 'label:', label
                    print 'label_counts[label][c]', c[label]
                    print 'label_counts[label][c_prim]', c_prim[label]
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
    
#-------------------------------------------CLASSIFYING-----------------------------------------------#
    def classify(self, sample):
        '''
        Classify sample using KNN with use of precomputed values. Return labels of closest points.
        '''
        answer = []
        neigh_codes =  super(MlknnThreshold, self).count_neighbours_per_code(sample, self.find_nearest_neighbours, self.k, self.get_labels, self.kernel)
        for code in self.labels:
            #print '[MLKNNFRACTIONAL] code neigh_codes.get(code, 0), self.fraction_knn_thresholds[code]', code, neigh_codes.get(code, 0), self.fraction_knn_thresholds[code]
            if neigh_codes.get(code, 0) > self.fraction_knn_thresholds[code]:
                answer.append(code)
        return answer