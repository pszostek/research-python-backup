'''
Created on Jul 04, 2012

@author: mlukasik
'''
import sys
sys.path.append(r'../')
from main_K_fold_distmat import gen_train_test_kfold
from main_train_classifier_distmat import main
import logging
log_level = logging.INFO
logging.basicConfig(level=log_level)

def PRINTER(x):
    logging.info('[evaluate_k_kfold]: '+str(x))
    
def evaluate_k_kfold(labels, labelsset, train_generator, train_elements_count, classifier_name, k, smoothing_param, distancematrix, kfold):
    '''
    Evaluates a knn-based classifier using k-fold.
    '''
    measures = [[] for _ in xrange(6)]#6 measures
    for train_generator2, test_generator2 in gen_train_test_kfold(labelsset, train_generator, train_elements_count, kfold):
        sub_measures = main(train_generator2, labels, train_elements_count, classifier_name, k, smoothing_param, distancematrix, test_generator2)
        for i, sub_m in enumerate(sub_measures):
            measures[i].append(sub_m)
    #summarize, each :
    final_measures = [{} for _ in xrange(6)]
    for ind, final_measure in enumerate(final_measures):
        for key in measures[0][0].keys():
            final_measure[key] = 0
        for key in measures[0][0].keys():
            for measure in measures[ind]:
                final_measure[key] += measure[key]
        for key in measures[0][0].keys():
            final_measure[key] /= len(measures[0])
    return final_measure
        
if __name__ == "__main__":
    try:
        fname = sys.argv[1]
    except:
        print '1st argument: file name with zbl records.'
        sys.exit(1)
    try:
        codeprefixlen = int(sys.argv[2])
    except:
        print '2nd argument: length of a prefix of codes to be considered'
        sys.exit(1)
    try:
        mincodeoccurences = int(sys.argv[3])
    except:
        print '3d argument: minimum occurence of each of the codes.'
        sys.exit(1)
    try:
        classifier_name = sys.argv[4]
    except:
        print '4th argument expected: name of a classifier'
        sys.exit(1)
    try:
        k = sys.argv[5]
    except:
        print '5th argument expected: k parameter'
        sys.exit(1)
    try:
        smoothing_param = int(sys.argv[6])
    except:
        print '6th argument expected: smoothing parameter'
        sys.exit(1)
    try:
        distancematrix = sys.argv[7]
    except:
        print '7th argument expected: path to distance matrix.'
        sys.exit(1)
    try:
        kfold = int(sys.argv[8])
    except:
        print '8th argument: how many folds.'
        sys.exit(1)
    try:
        filtered_by = sys.argv[9:]
    except:
        print '8th argument: field names which have to occur for the record to be considered.'
        sys.exit(1)
    """
    PRINTERMAIN("Input arguments:")
    PRINTERMAIN("fname: "+fname)
    PRINTERMAIN("codeprefixlen: "+str(codeprefixlen))
    PRINTERMAIN("mincodeoccurences: "+str(mincodeoccurences))
    PRINTERMAIN("save_train_generator_path: "+save_train_generator_path)
    PRINTERMAIN("save_test_generator_path: "+save_test_generator_path)
    PRINTERMAIN("save_labels_path: "+save_labels_path)
    PRINTERMAIN("save_elements_count_path: "+save_elements_count_path)
    PRINTERMAIN("filtered_by: "+str(filtered_by))
    """
    from main_train_classifier_distmat import main
    #curr_accuracy, curr_precision, curr_recall, curr_hammingloss, curr_subset01loss, curr_fmeasure
    measures = [[] for _ in xrange(6)]#6 measures
    for train_generator, test_generator, elements_count, labels, elements_count in gen_train_test_kfold(fname, codeprefixlen, mincodeoccurences, filtered_by, kfold):
        from choose_best_k import evaluate_k_kfold
        train_elements_count = len(train_generator)
        k_evaluation = evaluate_k_kfold(labels, labelsset, lambda: train_generator, train_elements_count, classifier_name, k, smoothing_param, distancematrix, kfold)
        #sys.exit(1)
        sub_measures = main(train_generator, labels, elements_count, classifier_name, k, smoothing_param, distancematrix, test_generator)
        for i, sub_m in enumerate(sub_measures):
            measures[i].append(sub_m)
    #summarize, each :
    final_measures = [{} for _ in xrange(6)]
    for ind, final_measure in enumerate(final_measures):
        for key in measures[0][0].keys():
            final_measure[key] = 0
        for key in measures[0][0].keys():
            for measure in measures[ind]:
                final_measure[key] += measure[key]
        for key in measures[0][0].keys():
            final_measure[key] /= len(measures[0])
    
    from mltools.multilabel_evaluate import multilabel_evaluate_printresults
    PRINTERMAIN("---FINAL RESULTS---")
    def PRINTER_PARAM(x):
        print x
    multilabel_evaluate_printresults(*final_measures)