'''
Created on Jan 2, 2012

@author: mlukasik

Evaluation of a multilabel classifier.
'''
from __future__ import division

def PRINTER_ONSCREEN(x):
    print x

def PRINTER_LOG(x):
    #import logging
    #logging.info(x)
    #print x#PRINTER x#PRINTER_LOG(x)
    pass

def multilabel_evaluate(test_generator, classify_oracle, classify_try, labels_len, label_functions = {'full label': lambda x: x}):
    '''
    Evaluate a multi-label classifier, comparing its results against the oracle classifier. 
    
    Arguments:
    test_generator - function returning generator, which returns test instances
    classify_oracle - the TRUE labelling of a record, e.g. def classify_oracle(record) -> [label1, label2, label3]
    classify_try - the classifier, e.g. def classify(record) -> [label1, label2, label3]
    labels_len - number of all possible labels
    label_functions - functions mapping the labels into format which user wants to count. It is useful, if the labels are of hierarchical format,
        and a user wants to count the statistics for different hierarchies
    
    Example usage in _test_multilabel_evaluate.
    
    Tested.
    '''
    accuracy = {}
    precision = {}
    recall = {}
    fmeasure = {}
    hammingloss = {}
    subset01loss = {}
    
    for i, _ in label_functions.iteritems():
        accuracy[i] = 0
        precision[i] = 0
        recall[i] = 0
        fmeasure[i] = 0
        hammingloss[i] = 0
        subset01loss[i] = 0
        
    elements_count = 0
    
    #FOR EACH RECORD:
    for rec in test_generator():
        elements_count+=1
        
        if elements_count % 100 == 1:
            PRINTER_LOG("[multilabel_evaluate]: iteration: "+str(elements_count))
        
        #classify record:
        oracle_ans = classify_oracle(rec)
        classif_ans = classify_try(rec)
        #PRINTER_LOG("[multilabel_evaluate]: oracle_ans: "+str(oracle_ans))
        
        #FOR EACH LABEL MAPPING FUNCTION:
        for i, labelf in label_functions.iteritems():
            #PRINTER_LOG("[multilabel_evaluate] i, labelf:"+str(i)+" "+str(labelf))
            #PRINTER_LOG("[multilabel_evaluate] map(labelf, classif_ans)):"+str(map(labelf, classif_ans)))
            
            zi = map(labelf, classif_ans)
            yi = map(labelf, oracle_ans)
            
            #PRINTER_LOG("[multilabel_evaluate]: -----------------------")
            #PRINTER_LOG("[multilabel_evaluate]: predicted: "+str(zi))
            #PRINTER_LOG("[multilabel_evaluate]: should be: "+str(yi))
            #PRINTER_LOG("[multilabel_evaluate]: -----------------------")
            
            zi_set = set(zi)
            yi_set = set(yi)
            
            #ACCURACY:
            accuracy[i] += len(zi_set & yi_set)/len(zi_set | yi_set)
            
            #PRECISION:
            if len(zi_set) > 0:
                curr_prec = len(zi_set & yi_set)/len(zi_set)
            else:
                curr_prec = 0
            precision[i] += curr_prec
            
            #RECALL:
            if len(yi_set) > 0:
                curr_recall = len(zi_set & yi_set)/len(yi_set)
            else:
                curr_recall = 0
            recall[i] += curr_recall
            
            #F-MEASURE:
            if (curr_prec+curr_recall) == 0:
                fmeasure[i] += 0
            else:          
                fmeasure[i] += 2.0*(curr_prec*curr_recall)/(curr_prec+curr_recall)
            
            #LOSS MEASURES: 
            hammingloss[i] += (len(zi_set - yi_set)+len(yi_set - zi_set))
            subset01loss[i] += int(zi_set != yi_set)
    
    #DIVIDE BY NUMBER OF SAMPLES:
    for i in label_functions.iterkeys():
        accuracy[i] /= elements_count
        precision[i] /= elements_count
        recall[i] /= elements_count
        fmeasure[i] /= elements_count
        hammingloss[i] /= (elements_count*labels_len)
        subset01loss[i] /= elements_count
    
    return accuracy, precision, recall, hammingloss, subset01loss, fmeasure

def multilabel_evaluate_labelerrors(test_generator, classify_oracle, classify_try, labels_len, label_functions, labels):
    '''
    Evaluate a multi-label classifier, checking each label in terms of FP, TP, FN measures.
    
    Arguments:
    test_generator - function returning generator, which returns test instances
    classify_oracle - the TRUE labelling of a record, e.g. def classify_oracle(record) -> [label1, label2, label3]
    classify_try - the classifier, e.g. def classify(record) -> [label1, label2, label3]
    labels_len - number of all possible labels
    label_functions - functions mapping the labels into format which user wants to count. It is useful, if the labels are of hierarchical format,
        and a user wants to count the statistics for different hierarchies
    labels - all labels list
    '''
    #a dictionary describing errors that occur in the process of classification
    #save number of true positives, false positives, true negatives, false negatives
    label2error = {}
    
    for i, _ in label_functions.iteritems():
        label2error[i] = {}
        
    elements_count = 0
    
    #FOR EACH RECORD:
    for rec in test_generator():
        elements_count+=1
        
        #classify record:
        oracle_ans = classify_oracle(rec)
        classif_ans = classify_try(rec)
        #PRINTER_LOG("[multilabel_evaluate]: oracle_ans: "+str(oracle_ans))
        
        #FOR EACH LABEL MAPPING FUNCTION:
        for i, labelf in label_functions.iteritems():
            #PRINTER_LOG("[multilabel_evaluate] i, labelf:"+str(i)+" "+str(labelf))
            #PRINTER_LOG("[multilabel_evaluate] map(labelf, classif_ans)):"+str(map(labelf, classif_ans)))
            
            zi = map(labelf, classif_ans)
            yi = map(labelf, oracle_ans)
            
            zi_set = set(zi)
            yi_set = set(yi)
                        
            for code in set(map(labelf, labels)):
                if code not in label2error[i]:
                    label2error[i][code] = {'TP': 0, 'TN':0, 'FP':0, 'FN':0}
                
                if code in zi_set and code in yi_set:
                    label2error[i][code]['TP']+=1
                elif code in zi_set and code not in yi_set:
                    label2error[i][code]['FP']+=1
                elif code not in zi_set and code in yi_set:
                    label2error[i][code]['FN']+=1
                elif code not in zi_set and code not in yi_set:
                    label2error[i][code]['TN']+=1
    
    print "[multilabel_evaluate_labelerrors] elements_count:", elements_count
    
    return label2error

def multilabel_evaluate_printresults(test_generator, classify_oracle, classify_try, labels_len, label_functions, labels):
    '''
    test_generator - function returning generator, which returns test instances
    classify_oracle - the TRUE labelling of a record, e.g. def classify_oracle(record) -> [label1, label2, label3]
    classify_try - the classifier, e.g. def classify(record) -> [label1, label2, label3]
    labels_len - number of all possible labels
    label_functions - functions mapping the labels into format which user wants to count. It is useful, if the labels are of hierarchical format,
        and a user wants to count the statistics for different hierarchies
        
    Print the results on the screen.
    
    '''
    
    accuracy, precision, recall, hammingloss, subset01loss, fmeasure = multilabel_evaluate(test_generator, classify_oracle, classify_try, labels_len, label_functions)
    label2error = multilabel_evaluate_labelerrors(test_generator, classify_oracle, classify_try, labels_len, label_functions, labels)
    
    PRINTER_ONSCREEN("=====================================================")
    PRINTER_ONSCREEN("=================EVALUATION MEASURES=================")
    PRINTER_ONSCREEN("=====================================================")
    
    for i in label_functions.iterkeys():
        PRINTER_ONSCREEN("=================Results for label function: "+str(i)+" =================")
        PRINTER_ONSCREEN("Accuracy: "+str(accuracy[i]))
        PRINTER_ONSCREEN("Precision: "+str(precision[i]))
        PRINTER_ONSCREEN("Recall: "+str(recall[i]))
        PRINTER_ONSCREEN("F-measure: "+str(fmeasure[i]))
        PRINTER_ONSCREEN("Hammingloss: "+str(hammingloss[i]))
        PRINTER_ONSCREEN("Subset01loss: "+str(subset01loss[i]))
    
    """PRINTER_ONSCREEN("=====================================================")
    PRINTER_ONSCREEN("=================Errors on labels====================")
    PRINTER_ONSCREEN("=====================================================")
    
    for i in label_functions.iterkeys():
        PRINTER_ONSCREEN("=================Results for label function: "+str(i)+" =================")
        for label, labeldict in label2error[i].iteritems():
            PRINTER_ONSCREEN("Label: "+str(label))
            PRINTER_ONSCREEN("\tTP: "+str(labeldict['TP']))
            PRINTER_ONSCREEN("\tFP: "+str(labeldict['FP']))
            PRINTER_ONSCREEN("\tTN: "+str(labeldict['TN']))
            PRINTER_ONSCREEN("\tFN: "+str(labeldict['FN']))
       """     