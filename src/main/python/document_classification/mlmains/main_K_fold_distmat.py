'''
Created on Feb 22, 2012

@author: mlukasik


'''
import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import gen_1record_prefixed, gen_record, gen_record_prefixed, gen_lmc, gen_record_fromshifts, gen_record_filteredbylabels, mc2lmc_tomka_blad
from tools.msc_processing import get_labels_min_occurence
#for splitting the data into training and testing
from tools.randomly_divide import randomly_divide

import logging
log_level = logging.INFO
logging.basicConfig(level=log_level)

def PRINTERMAIN(x):
    logging.info('[main_K_fold_distmat][main]: '+str(x))
    #print '[split_train_test_highest][main]: '+str(x)

def PRINTER(x):
    #pass
    #import logging
    #logging.info(x)
    logging.info('[main_K_fold_distmat][main]: '+str(x))
    #print '[split_train_test_highest]: '+str(x)

def evaluate_k_fold(classifier_name, k, smoothing_param, distancematrix, kfold, labels, labelsset, prefix_code_generator, elements_count):
    '''
    Evaluates a knn-based classifier using k-fold.
    '''
    measures = [[] for _ in xrange(6)] #6 measures
    for train_generator, test_generator in gen_train_test_kfold(labelsset, prefix_code_generator, elements_count, kfold):
        sub_measures = main(train_generator, labels, elements_count, classifier_name, k, smoothing_param, distancematrix, test_generator)
        for i, sub_m in enumerate(sub_measures):
            measures[i].append(sub_m) #summarize, each :
    
    final_measures = [{} for _ in xrange(6)]
    for ind, final_measure in enumerate(final_measures):
        for key in measures[0][0].keys():
            final_measure[key] = 0
        
        for key in measures[0][0].keys():
            for measure in measures[ind]:
                final_measure[key] += measure[key]
        
        for key in measures[0][0].keys():
            final_measure[key] /= len(measures[0])
    
    return final_measures

def load_labels_codegen_elemcnt(fname, codeprefixlen, mincodeoccurences, filtered_by):
    #prepare generators
    rec_generator = lambda:gen_record(fname, filtered_by)
    prefixed_rec_generator = lambda:gen_record_prefixed(rec_generator, codeprefixlen)
    prefix_code_generator = lambda:gen_lmc(prefixed_rec_generator)
    #generate labels
    PRINTER('generating labels...')
    labels = get_labels_min_occurence(prefix_code_generator, mincodeoccurences)
    PRINTER('labels generated:')
    PRINTER(str(labels))
    
    #gen filtered records:
    labelsset = set(labels)
    prefix_code_generator = lambda:gen_record_filteredbylabels(prefixed_rec_generator, labelsset)
    PRINTER('counting elements...')
    elements_count = len(list(prefix_code_generator()))
    PRINTER('number of elements' +str(elements_count))
    
    return labels, labelsset, prefix_code_generator, elements_count
    
def gen_train_test_kfold(labelsset, prefix_code_generator, elements_count, kfold):
    #split into training and testing samples
    buckets = [[] for _ in xrange(kfold)]
    for ind in xrange(elements_count):
        buckets[ind%kfold].append(ind)
    
    #print "buckets:", buckets
    
    for test_bucket_ind in xrange(kfold):
        test_inds = buckets[test_bucket_ind]
        train_inds = sorted(reduce(lambda a, b: a+b, buckets[:test_bucket_ind]+buckets[test_bucket_ind+1:]))
        
        #print "test_inds:", test_inds, len(test_inds)
        #print "train_inds:", train_inds, len(train_inds)
        
        train_generator = list(gen_record_fromshifts(prefix_code_generator, train_inds))
        test_generator = list(gen_record_fromshifts(prefix_code_generator, test_inds))
        
        yield train_generator, test_generator

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
    labels, labelsset, prefix_code_generator, elements_count = load_labels_codegen_elemcnt(fname, codeprefixlen, mincodeoccurences, filtered_by)
    from main_train_classifier_distmat import main
    #curr_accuracy, curr_precision, curr_recall, curr_hammingloss, curr_subset01loss, curr_fmeasure
    final_measures = evaluate_k_fold(classifier_name, k, smoothing_param, distancematrix, kfold, labels, labelsset, prefix_code_generator, elements_count)
    
    from mltools.multilabel_evaluate import multilabel_evaluate_printresults
    PRINTERMAIN("---FINAL RESULTS---")
    def PRINTER_PARAM(x):
        print x
    multilabel_evaluate_printresults(*(final_measures+[PRINTER_PARAM]))