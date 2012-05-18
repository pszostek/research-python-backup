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
from data_io.zbl_record_generators import gen_1record_prefixed, gen_record, gen_record_prefixed, gen_lmc, gen_record_fromshifts, gen_record_filteredbylabels, mc2lmc_tomka_blad
from tools.msc_processing import get_labels_min_occurence
#for splitting the data into training and testing
from tools.randomly_divide import randomly_divide
from mltools.multilabel_evaluate import multilabel_evaluate_printresults
#from mltools import ml_hierarchical

#from tools import ml_hierarchical
#import mlknn

def PRINTER(x):
    logging.info('[main_test][main]: '+str(x))
    #print x

if __name__ == '__main__':
    try:
        load_classifier_path = sys.argv[1]
    except:
        print 'First argument expected: path to a pickled classifier.'
        sys.exit(1)
    try:
        load_test_generator = sys.argv[2]
    except:
        print 'Second argument expected: path to a pickled test set.'
        sys.exit(1)
    try:
        labels_path = sys.argv[3]
    except:
        print '3d argument expected: path to a pickled labels list.'
        sys.exit(1)
    try:
        classify_method_name = sys.argv[4]
    except:
        print '4th argument expected: classify method name.'
        sys.exit(1)
    
    #PRINTER("Input arguments:")
    #PRINTER("load_classifier_path: "+str(load_classifier_path))
    #PRINTER("load_test_generator: "+str(load_test_generator))
    #PRINTER("labels_path: "+str(labels_path))
    #PRINTER("classify_method_name: "+str(classify_method_name))
    
    from tools.pickle_tools import read_pickle
    classifier = read_pickle(load_classifier_path)
    test_generator = read_pickle(load_test_generator) 
    labels = read_pickle(labels_path)
    
    #print "Finding out if the ML-hierarchical has internal data..."
    #check_internal_data(hierarhical_mlknn)
    classify_oracle = mc2lmc_tomka_blad
    
    #print "----------------------------------------------------"
    #print "Hierachical MLKNN:"
    PRINTER("-----------RESULTS-----------")
    multilabel_evaluate_printresults(lambda: test_generator, classify_oracle, classifier.__getattribute__(classify_method_name), len(labels), 
                    {'full label': lambda x: x, 'half label': lambda x: x[:3], 'low label': lambda x: x[:2]}, labels)
    