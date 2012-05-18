'''
Created on Feb 21, 2012

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
from mlknn.mlknn import MlKnn
from mlknn.find_closest_points import find_closest_points
from mlknn.jaccard_distance import JaccardDistance
from mltools.ml_hierarchical import MlHierarchical

def PRINTER(x):
    logging.info('[main_train_hierarchical_mlknn][main]: '+str(x))
    #print '[main_train_mlknn][main]: '+str(x)

if __name__ == '__main__':
    try:
        load_train_generator_path = sys.argv[1]
    except:
        print '1st argument expected: path to a pickled generator of a training set'
        sys.exit(1)
    try:
        load_labels_path = sys.argv[2]
    except:
        print '2nd argument expected: path to a pickled list of labels'
        sys.exit(1)
    try:
        load_elements_count_path = sys.argv[3]
    except:
        print '3d argument expected: path to a pickled elements count'
        sys.exit(1)
    try:
        save_classifier_path = sys.argv[4]
    except:
        print '4th argument expected: path to where to save the classifier'
        sys.exit(1)
    try:
        k = int(sys.argv[5])
    except:
        print '5th argument expected: k parameter'
        sys.exit(1)
    try:
        smoothingparam = int(sys.argv[6])
    except:
        print '6th argument expected: smoothing parameter'
        sys.exit(1)
    try:
        distancetrainingsteps = int(sys.argv[7])
    except:
        print '7th argument expected: distancetrainingsteps parameter'
        sys.exit(1)
    try:
        load_test_generator = sys.argv[8]
    except:
        print '8th argument expected: load_test_generator parameter'
        sys.exit(1)
    
    PRINTER("Loading the input data...")
    from tools.pickle_tools import read_pickle
    train_generator_list = read_pickle(load_train_generator_path) 
    lenlabels = len(read_pickle(load_labels_path)) 
    elements_count = read_pickle(load_elements_count_path) 
    
    train_generator = lambda: train_generator_list
    #train mlknn:
    PRINTER("Training Distance...")
    zbldistance = JaccardDistance(train_generator, elements_count-int(elements_count/10), distancetrainingsteps)
    
    get_labels_of_record = mc2lmc_tomka_blad
    mlknn_callable = lambda train_gen, get_labels_of_record_arg: MlKnn(train_gen, zbldistance, find_closest_points, 
                         k, smoothingparam, get_labels_of_record_arg)
    
    label_mappings = (lambda x: x[:2], lambda x: x[:3], lambda x: x)
    
    PRINTER("Training hierarchical mlknn...")
    from time import time
    start = time()
    hierarhical_mlknn = MlHierarchical(train_generator, mlknn_callable, label_mappings, get_labels_of_record)
    PRINTER("time taken for training:"+str(start-time()))
    
    PRINTER("Testing hierarchical mlknn...")
    test_generator = read_pickle(load_test_generator) 
    labels = read_pickle(load_labels_path)
    
    #print "Finding out if the ML-hierarchical has internal data..."
    #check_internal_data(hierarhical_mlknn)
    classify_oracle = mc2lmc_tomka_blad
    
    #print "----------------------------------------------------"
    #print "Hierachical MLKNN:"
    from mltools.multilabel_evaluate import multilabel_evaluate_printresults
    PRINTER("-----------RESULTS-----------")
    multilabel_evaluate_printresults(lambda: test_generator, classify_oracle, hierarhical_mlknn.__getattribute__('classify'), len(labels), 
                    {'full label': lambda x: x, 'half label': lambda x: x[:3], 'low label': lambda x: x[:2]}, labels)
    
    #from tools.pickle_tools import save_pickle
    #save_pickle(hierarhical_mlknn, save_classifier_path)
    