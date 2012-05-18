'''
Created on Feb 13, 2012

@author: mlukasik
'''
from __future__ import division
from __future__ import absolute_import

import logging

import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import gen_1record_prefixed, gen_record, gen_record_prefixed, gen_lmc, gen_record_fromshifts, gen_record_filteredbylabels, mc2lmc_tomka_blad
from tools.msc_processing import get_labels_min_occurence
#for splitting the data into training and testing
from tools.randomly_divide import randomly_divide
from mltools.multilabel_evaluate import multilabel_evaluate_printresults

import ml_hierarchical

def PRINTER(x):
    print x

if __name__ == '__main__':
    load_hierarchical_path = sys.argv[1]
    load_train_generator = sys.argv[2]
    lenlabels_path = sys.argv[3]
    
    PRINTER("Input arguments:")
    PRINTER("load_hierarchical_path: "+str(load_hierarchical_path))
    PRINTER("load_train_generator: "+str(load_train_generator))
    PRINTER("lenlabels_path: "+str(lenlabels_path))

    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    
    from tools.pickle_tools import read_pickle
    hierarhical_mlknn = read_pickle(load_hierarchical_path)
    test_generator = read_pickle(load_train_generator) 
    lenlabels = read_pickle(lenlabels_path) 
    
    #print "Finding out if the ML-hierarchical has internal data..."
    #check_internal_data(hierarhical_mlknn)
    
    
    print "----------------------------------------------------"
    #print "MLKNN:"
    #print "PRINTING TEST SAMPLES:"
    #for i in test_generator:
    #    print classify_oracle(i)
    
    classify_oracle = lambda x: mc2lmc_tomka_blad(x)
    multilabel_evaluate_printresults(lambda: test_generator, classify_oracle, hierarhical_mlknn.classify, lenlabels, 
                    {'full label': lambda x: x, 'half label': lambda x: x[:3], 'low label': lambda x: x[:2]})
    
    #print "----------------------------------------------------"
    #print "STUPID KNN:"
    #multilabel_evaluate_printresults(test_generator, classify_oracle, hierarhical_mlknn.classify_stupid, len(labels), 
    #                #{'full label': lambda x: x, 'short label': lambda x: x[:1]})
    #                {'full label': lambda x: x, 'half label': lambda x: x[:3], 'low label': lambda x: x[:2]})