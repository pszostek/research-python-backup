'''
Created on Jun, 6, 2012

@author: mlukasik
'''
from __future__ import division
from __future__ import absolute_import

import logging

#log_level = logging.INFO
#logging.basicConfig(level=log_level)
    
import sys
sys.path.append(r'../')

from data_io.zbl_record_generators import gen_1record_prefixed
from split_train_test_highest import split_train_test_highest
from data_io.zbl_record_generators import mc2lmc_tomka_blad, gen_lmc
from tools.msc_processing import get_labels_min_occurence
#for mlknn
from mlknn.find_closest_points_sorted import find_closest_points_sorted

def PRINTER(x):
    logging.info('[main_train_hier_classifier][main]: '+str(x))
    #print '[main_train_mlknn][main]: '+str(x)

if __name__ == '__main__':
    import logging
    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    
    try:
        load_train_generator_path = sys.argv[1]
    except:
        print '1st argument expected: path to a generator of a training set'
        sys.exit(1)
    try:
        load_labels_path = sys.argv[2]
    except:
        print '2nd argument expected: path to a label list'
        sys.exit(1)
    try:
        load_elements_count_path = sys.argv[3]
    except:
        print '3d argument expected: path to a list of elements'
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
        load_test_generator = sys.argv[8]
    except:
        print '8th argument expected: load_test_generator parameter'
        sys.exit(1)
    
    PRINTER('Loading training list...')
    from tools.pickle_tools import read_pickle
    train_generator_list = read_pickle(load_train_generator_path)

    PRINTER('Loading labels path and elements count...')
    lenlabels = len(read_pickle(load_labels_path)) 
    elements_count = read_pickle(load_elements_count_path) 
    
    PRINTER("Finding label list...")
    get_labels_of_record = mc2lmc_tomka_blad
    find_all_labels = lambda frecords: get_labels_min_occurence(lambda: gen_lmc(frecords), 1)
    
    PRINTER("Loading distance matrix...")
    import sys
    sys.path.append(r'../')
    from data_io.matrix_io import fread_smatrix
    (rows, cols, data) = fread_smatrix(distancematrix)
    id2rowind, id2colind = {}, {}
    for ind, id in enumerate(rows):
        id2rowind[id] = ind
    for ind, id in enumerate(cols):
        id2colind[id] = ind
        
    print "len(train_generator_list):",len(train_generator_list)
    print "len(rows):",len(rows) 
    #print "(rows, cols, data):", (rows, cols, data)
    
        
    
    PRINTER("Training classifier...")
    from time import time
    
    def printer(x):
        #import logging
        logging.info('['+classifier_name+']'+x)

    def distance(a, b): 
        try:
            return data[id2rowind[a['an']]][id2colind[b['an']]]
        except:
            return data[id2colind[b['an']]][id2rowind[a['an']]]
    def get_neighbours(sample, k, train_gen):
        return find_closest_points_sorted(sample, train_gen, [sample], k, distance)
        
    start = time()
    if classifier_name=='mlknn-basic-tree':
        k = int(k)
        from mlknn import mlknn_basic
        mlknn_callable = lambda train_gen, get_labels_of_record_arg: mlknn_basic.MlknnBasic(train_gen, lambda sample, k: get_neighbours(sample, k, train_gen), 
                                                                           k, smoothing_param, get_labels_of_record_arg, lambda x:1, printer)
    
    elif classifier_name == 'mlknn-threshold-tree':
        k = int(k)
        from mlknn import mlknn_threshold
        mlknn_callable = lambda train_gen, get_labels_of_record_arg: mlknn_threshold.MlknnThreshold(train_gen, lambda sample, k: get_neighbours(sample, k, train_gen), 
                                                                           k, smoothing_param, get_labels_of_record_arg, lambda x:1, printer)
    
    elif classifier_name == 'mlknn-tensembled-tree':
        k = map(int, k.strip().split(','))
        PRINTER("loaded k-list: "+str(k))
        from mlknn import mlknn_tensembled
        mlknn_callable = lambda train_gen, get_labels_of_record_arg: mlknn_tensembled.MlknnTEnsembled(train_gen, lambda sample, k: get_neighbours(sample, k, train_gen), 
                                                                                                      k, get_labels_of_record_arg, lambda x:1, printer)

    label_mappings = (lambda x: x[:2], lambda x: x[:3], lambda x: x)
    
    
    from mltools.ml_hierarchical import MlHierarchical
    classifier = MlHierarchical(train_generator_list, mlknn_callable, label_mappings, get_labels_of_record)
        
    PRINTER("Time taken for training:"+str(start-time()))
    
    PRINTER("------------------------")
    PRINTER("---Testing classifier---")
    PRINTER("------------------------")
    test_generator = read_pickle(load_test_generator) 
    labels = read_pickle(load_labels_path)


    classify_oracle = mc2lmc_tomka_blad
    from mltools.multilabel_evaluate import multilabel_evaluate_printresults
    PRINTER("-----------RESULTS-----------")
    multilabel_evaluate_printresults(lambda: test_generator, classify_oracle, classifier.__getattribute__('classify'), len(labels), 
                    [('full label', lambda x: x), ('half label', lambda x: x[:3]), ('low label', lambda x: x[:2])], labels)
    
    