'''
Created on Mar 15, 2012

@author: mlukasik
'''
from __future__ import division

def PRINTER_REPORTER(x):
    import logging
    logging.info('[mlknn_adjust_thresholds] '+x)
def PRINTER_ONSCREEN(x):
    print '[mlknn_adjust_thresholds] '+x

def mlknn_adjust_thresholds(mlknn, validate_frecords, classify_oracle):
    '''
    Adjusts thresholds in mlknn for each class, optimizing the results on validate_frecords.
    '''
    #initialize the lists of moves:
    move_lists = {}
    for label in mlknn.labels:
        #G - good, B - bad
        move_lists[label] = {'G': [], 'B': []}
    
    for ind, validation_rec in enumerate(validate_frecords):
        if ind%100 == 0:
            PRINTER_REPORTER("Validation ind: "+str(ind))

        oracle_ans = set(classify_oracle(validation_rec))
        classif_ans = set(mlknn.classify(validation_rec))
        
        neigh_codes = mlknn.count_neighbours_per_code(validation_rec)
        
        #for each label from the sum of the labels returned by the oracle and the classifier:
        for label in mlknn.labels:
            tproba, fproba = mlknn.get_unnormalized_probabilities_for_class(validation_rec, label, neigh_codes.get(label, 0))
            
            #adjust curr_thresh_to_half so that it moves the result exactly to the half 
            #if label in classif_ans and label in oracle_ans:
            #    curr_thresh_to_half = (0.5*tproba-fproba)
            #elif label not in classif_ans and label not in oracle_ans:
            #    curr_thresh_to_half = (2*tproba-fproba)
            #elif label not in classif_ans and label in oracle_ans:
            #    curr_thresh_to_half = (0.5*tproba-fproba)
            #elif label in classif_ans and label not in oracle_ans:
            #    curr_thresh_to_half = (2*tproba-fproba)
            curr_thresh_to_half = (2*tproba-fproba)
            if label in oracle_ans:
                curr_thresh_to_half = (0.5*tproba-fproba)
            
            #if this was correct labeling:
            if (label in classif_ans and label in oracle_ans) or not (label in classif_ans or label in oracle_ans):
                move_lists[label]['G'].append(curr_thresh_to_half)
            #if this wasnt correct labeling:
            else:
                move_lists[label]['B'].append(curr_thresh_to_half)
    
    #adjust the moves:
    for key, move_list in move_lists.iteritems():
        #display the moves that have been generated:
        PRINTER_ONSCREEN(key)
        PRINTER_ONSCREEN("Good:")
        PRINTER_ONSCREEN(str(move_list['G']))
        PRINTER_ONSCREEN("Bad:")
        PRINTER_ONSCREEN(str(move_list['B']))
        PRINTER_ONSCREEN("-------------------------------------")
        #here is the work being done:
        mlknn.threshold[key] = sum(move_list['B'])/len(move_list['B'])
