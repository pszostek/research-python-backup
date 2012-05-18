'''
Created on Feb 21, 2012

@author: mlukasik
'''
from __future__ import division
from __future__ import absolute_import

import logging

log_level = logging.INFO
logging.basicConfig(level=log_level)
    
import sys
sys.path.append(r'../')

from data_io.zbl_record_generators import mc2lmc_tomka_blad, gen_lmc
from tools.msc_processing import get_labels_min_occurence

from data_io.zbl_record_generators import gen_1record_prefixed
from split_train_test_highest import split_train_test_highest
#for mlknn
from mlbaselines.randomlabel_classifier import RandomLabelClassifier

def PRINTER(x):
    logging.info('[main_train_random][main]: '+str(x))
    #print '[main_train_mlknn][main]: '+str(x)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        PRINTER("Not enough of argument!")
        exit(1)
    
    load_train_generator_path = sys.argv[1]
    load_labels_path = sys.argv[2]
    load_elements_count_path = sys.argv[3]
    save_classifier_path = sys.argv[4]
    
    PRINTER("Input arguments:")
    PRINTER("load_train_generator_path: "+str(load_train_generator_path))
    PRINTER("load_labels_path: "+str(load_labels_path))
    PRINTER("load_elements_count_path: "+str(load_elements_count_path))
    PRINTER("save_classifier_path: "+str(save_classifier_path))
    
    from tools.pickle_tools import read_pickle
    train_generator_list = read_pickle(load_train_generator_path) 
    lenlabels = len(read_pickle(load_labels_path)) 
    elements_count = read_pickle(load_elements_count_path) 
    
    train_generator = lambda: train_generator_list
    get_labels_of_record = mc2lmc_tomka_blad
    find_all_labels = lambda frecords: get_labels_min_occurence(lambda: gen_lmc(frecords), 1)
    classify_oracle = lambda x: mc2lmc_tomka_blad(x)
    
    random_classif = RandomLabelClassifier(train_generator, get_labels_of_record, find_all_labels, classify_oracle)
    
    from tools.pickle_tools import save_pickle
    save_pickle(random_classif, save_classifier_path)
    