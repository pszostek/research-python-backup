'''
Created on Mar 8, 2012

'''
import sys
sys.path.append(r'../')
sys.path.append(r'../../')

from mltools import multilabel_evaluate
from itertools import izip

def jrs_evaluate(results_oracle, results_classifier):
    '''
    Evaluate a multilabel classifier.
    
    @type results_oracle: list of lists of strings
    @param results_classifier: labels assigned to each consecutive object by
        a an expert
    
    @type results_classifier: list of lists of strings
    @param results_classifier: labels assigned to each consecutive object by
        a classifier being evaluated
        
    '''
    precs = []
    recals = []
    f1s = []
    for oracle, pred in izip(results_oracle, results_classifier):
        try:
            prec = float(len(set(oracle).intersection(set(pred)))) / len(set(pred))
        except:
            prec = 0.0
        try:
            recall = float(len(set(oracle).intersection(set(pred)))) / len(set(oracle))
        except:
            recall = 0.0
        try:
            f1 = 2.0*prec*recall/(prec+recall)
        except:
            f1 = 0.0
        precs.append(prec)
        recals.append(recall)
        f1s.append(f1)
    
    avg_prec = sum(precs) / len(precs)
    avg_recal = sum(recals) / len(recals)
    avg_f1 = sum(f1s) / len(f1s)
    
    return  0.0, avg_prec, avg_recal, 0.0, 0.0, avg_f1 
    #print '[TOMKOWE]', avg_prec, avg_recal, avg_f1 
    
    labels_len = -1
    try:
        labels_len = len(set(reduce(lambda a, b: a+b, results_oracle+results_classifier)))
    except:
        print "[jrs_evaluate]: Blad w liczeniu reduce! results_oracle:", results_oracle, "results_classifier", results_classifier
        raise Exception("x")
    #oracle_ans = map(lambda x: set(x), results_oracle)
    #classif_ans = map(lambda x: set(x), results_classifier)
    #all_ans = set()
    #for i in oracle_ans+classif_ans:
    #    all_ans |= i
    
    #print 'all_ans', all_ans
    #print 'len(all_ans)', len(all_ans)
    
    #labels_len = len(all_ans)
    num_of_objects = len(results_oracle)
    test_generator = lambda: xrange(num_of_objects)
    
    classify_oracle = lambda x: results_oracle[x]
    classify_try = lambda x: results_classifier[x]
    
    results = multilabel_evaluate.multilabel_evaluate(test_generator, classify_oracle, classify_try, labels_len, {'full label': lambda x: x})
    
    #wynik = map(lambda x: x['full label'], results)
    #print '[Michalowe]', wynik[1], wynik[2], wynik[5] 
    
    return map(lambda x: x['full label'], results)

if __name__ == "__main__":
    print jrs_evaluate([[1, 2], [2, 3]], [[1, 2], [2, 3]])
    print jrs_evaluate([[1, 2], [1]], [[], []])