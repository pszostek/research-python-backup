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
from mlknn.mlknn_fractional import MlKnnFractional
from mlknn.find_closest_points import find_closest_points
from mlknn.mlknn_adjust_thresholds import mlknn_adjust_thresholds
from mlknn.jaccard_distance import JaccardDistance

def PRINTER(x):
    logging.info('[main_train_mlknn][main]: '+str(x))
    #print '[main_train_mlknn][main]: '+str(x)

if __name__ == '__main__':
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
        save_classifier_path = sys.argv[4]
    except:
        print '4th argument expected: path to where a classifier is to be saved'
        sys.exit(1)
    try:
        k = int(sys.argv[5])
    except:
        print '5th argument expected: k parameter'
        sys.exit(1)
    try:
        distancetrainingsteps = int(sys.argv[6])
    except:
        print '6th argument expected: number of steps in training to be performed'
        sys.exit(1)
    
    try:
        distancetype = sys.argv[7]
    except:
        print '7th argument expected: type of distance. Available: jac, g0, g1, g2'
        sys.exit(1)
        
    PRINTER('Loading training list...')
    from tools.pickle_tools import read_pickle
    train_generator_list = read_pickle(load_train_generator_path)
    
    PRINTER('Loading labels path and elements count...')
    lenlabels = len(read_pickle(load_labels_path)) 
    elements_count = read_pickle(load_elements_count_path) 
    
    PRINTER("training distance...")
    train_generator = lambda: train_generator_list
    if distancetype=='jac':
        from mlknn.jaccard_distance import JaccardDistance
        zbldistance = JaccardDistance(train_generator, elements_count-int(elements_count/10), distancetrainingsteps)
    else:
        from mlknn.txt_cosine_distance import TxtCosineDistance 
        zbldistance = TxtCosineDistance(distancetype)
    
    PRINTER("Finding label list...")
    get_labels_of_record = mc2lmc_tomka_blad
    find_all_labels = lambda frecords: get_labels_min_occurence(lambda: gen_lmc(frecords), 1)
    
    PRINTER("Training MLKNN...")
    from time import time
    start = time()
    mlknn_single = MlKnnFractional(train_generator, zbldistance, find_closest_points, 
                         k, get_labels_of_record)
    PRINTER("Time taken for training:"+str(start-time()))
    
    from tools.pickle_tools import save_pickle
    PRINTER("MLKNN: pickling the classifier...")
    save_pickle(mlknn_single, save_classifier_path)
    