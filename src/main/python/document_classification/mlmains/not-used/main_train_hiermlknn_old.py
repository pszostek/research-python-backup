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
    if len(sys.argv) < 8:
        PRINTER("Not enough of argument!")
        exit(1)
    
    load_train_generator_path = sys.argv[1]
    load_labels_path = sys.argv[2]
    load_elements_count_path = sys.argv[3]
    save_classifier_path = sys.argv[4]
    
    k = int(sys.argv[5])
    smoothingparam = int(sys.argv[6])
    distancetrainingsteps = int(sys.argv[7])
    
    PRINTER("Input arguments:")
    PRINTER("load_train_generator_path: "+str(load_train_generator_path))
    PRINTER("load_labels_path: "+str(load_labels_path))
    PRINTER("load_elements_count_path: "+str(load_elements_count_path))
    PRINTER("save_classifier_path: "+str(save_classifier_path))
    
    PRINTER("k: "+str(k))
    PRINTER("smoothingparam: "+str(smoothingparam))
    PRINTER("distancetrainingsteps: "+str(distancetrainingsteps))
    
    PRINTER("-------------------------------------------")
    
    PRINTER("Loading the input data.")
    from tools.pickle_tools import read_pickle
    train_generator_list = read_pickle(load_train_generator_path) 
    lenlabels = len(read_pickle(load_labels_path)) 
    elements_count = read_pickle(load_elements_count_path) 
    
    train_generator = lambda: train_generator_list
    #train mlknn:
    PRINTER("Training Distance...")
    zbldistance = JaccardDistance(train_generator, elements_count-int(elements_count/10), distancetrainingsteps)
    
    get_labels_of_record = mc2lmc_tomka_blad
    find_all_labels = lambda frecords: get_labels_min_occurence(lambda: gen_lmc(frecords), 1)
    
    mlknn_callable = lambda train_gen: MlKnn(train_gen, zbldistance, find_closest_points, 
                         k, smoothingparam, find_all_labels, get_labels_of_record)
    
    label_mappings = (lambda x: x[:2], lambda x: x[:3], lambda x: x)
    record_mappings = (lambda x: gen_1record_prefixed(x, 2), lambda x: gen_1record_prefixed(x, 3), lambda x: x)
    
    PRINTER("Training hierarchical mlknn...")
    from time import time
    start = time()
    hierarhical_mlknn = MlHierarchical(train_generator, mlknn_callable, label_mappings, record_mappings)
    PRINTER("time taken for training:"+str(start-time()))
    
    from tools.pickle_tools import save_pickle
    save_pickle(hierarhical_mlknn, save_classifier_path)
    