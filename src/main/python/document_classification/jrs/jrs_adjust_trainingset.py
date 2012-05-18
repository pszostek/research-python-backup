
import random
import jrs_multilabel_classifier
import jrs_evaluation
import jrs_io
import time

def eval(testing2training_distances, training_labels, testing_labels, multilabel_classifier):
        predicted_labels = jrs_multilabel_classifier.classify_multilabel(testing2training_distances, training_labels, multilabel_classifier)
        accuracy, precision, recall, hammingloss, subset01loss, fmeasure =  jrs_evaluation.jrs_evaluate(testing_labels, predicted_labels)
        return fmeasure

def adjust_training_set(testing2training_distances, \
                        training_labels, testing_labels, multilabel_classifier, \
                        default_remove = False):    
    testing2training_distances  = jrs_io.copy_matrix(testing2training_distances) #we're working on copy
    training_labels             = list(training_labels)
     
    training_ixs = range(0, len(testing2training_distances[0])) #removal order
    random.shuffle(training_ixs)
    #print "Removal order:",training_ixs
                
    start_time = time.clock()    
    best_fmeasure                   = eval(testing2training_distances, training_labels, testing_labels, multilabel_classifier)
    best_testing2training_distances = jrs_io.copy_matrix(testing2training_distances)
    best_training_labels            = list(training_labels)
    removal_order = []   
    for i,training_ix in enumerate(training_ixs):
        #try removing single element from trainingset
        for row in testing2training_distances: 
            row.pop(training_ix)
        training_labels.pop(training_ix)
        #reevaluate
        #print "before reevaluation len(testing2training_distances[0])=",len(testing2training_distances[0])
        fmeasure = eval(testing2training_distances, training_labels, testing_labels, multilabel_classifier)
        #compare to previous results
        if (fmeasure > best_fmeasure) or (default_remove and fmeasure==best_fmeasure):
            removal_order.append(training_ix)
            #print "Removing col:",training_ix                    
            best_fmeasure                   = fmeasure                 
            best_testing2training_distances = jrs_io.copy_matrix(testing2training_distances)
            best_training_labels            = list(training_labels)   
            for j in xrange(i+1, len(training_ixs)): #correcting higher indexes
                if training_ixs[j] >= training_ix:
                    training_ixs[j] = training_ixs[j] - 1
            print "[adjust_training_set]",i,"fmeasure:",fmeasure, " in ", (time.clock() - start_time), "sec, training set size:",len(best_training_labels),len(testing2training_distances[0]) 
        else: #if fmeasure worse then reverting to previous training set
            testing2training_distances  = jrs_io.copy_matrix(best_testing2training_distances)
            training_labels             = list(best_training_labels)
            print "[adjust_training_set]",i,"skipping"
    
    print "[adjust_training_set] fmeasure: ",fmeasure, " in ", (time.clock() - start_time), "sec, training set size:",len(best_training_labels),len(testing2training_distances[0])
    return removal_order 

def remove_columns(matrix, removal_order):
    for row in matrix:
        for c in removal_order:
            row.pop(c)
    return matrix

def remove_list(lst, removal_order):
    for c in removal_order:
        lst.pop(c)
    return lst

    