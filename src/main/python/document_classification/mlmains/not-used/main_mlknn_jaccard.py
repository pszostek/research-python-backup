'''
Created on Dec 29, 2011

@author: mlukasik

Main module, which uses mlknn on ZBL data.
'''
from __future__ import division
from __future__ import absolute_import

import logging

import sys
sys.path.append(r'../')
#lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
#sys.path.append(lib_path)
#for reading records and finding labels
from data_io.zbl_record_generators import gen_record, gen_record_prefixed, gen_lmc, gen_record_fromshifts, gen_record_filteredbylabels, mc2lmc_tomka_blad
from tools.msc_processing2 import get_labels_min_occurence
#for splitting the data into training and testing
from tools.randomly_divide import randomly_divide
from tools.multilabel_evaluate import multilabel_evaluate_printresults
#for mlknn
import mlknn
import find_closest_points
import jaccard_distance

if __name__ == '__main__':
    if len(sys.argv) < 8:
        print "Sample call:"
        print "python"+sys.argv[0]+"../zbl2py/springer011211.txt 2 5 5 1 500 mc ti ut ab"
    fname = sys.argv[1]
    codeprefixlen = int(sys.argv[2])
    mincodeoccurences = int(sys.argv[3])
    k = int(sys.argv[4])
    smoothingparam = int(sys.argv[5])
    distancetrainingsteps = int(sys.argv[6])
    filtered_by = sys.argv[7:]
    
    print "Input arguments:"
    print "fname:", fname
    print "codeprefixlen:", codeprefixlen
    print "mincodeoccurences", mincodeoccurences
    print "k:", k
    print "smoothingparam:", smoothingparam
    print "distancetrainingsteps:", distancetrainingsteps
    print "filtered_by:", filtered_by

    log_level = logging.INFO
    logging.basicConfig(level=log_level)
    
    #prepare generators
    rec_generator = lambda: gen_record(fname, filtered_by)
    prefixed_rec_generator = lambda: gen_record_prefixed(rec_generator, codeprefixlen)
    prefix_code_generator = lambda: gen_lmc(prefixed_rec_generator)
    
    #generate labels
    print "generating labels..."
    labels = get_labels_min_occurence(prefix_code_generator, mincodeoccurences)
    labelsset = set(labels)
    print "labels generated."
    print labels
    
    #gen filtered records:
    prefix_code_generator = lambda: gen_record_filteredbylabels(prefixed_rec_generator, labelsset)
    print "counting elements..."
    elements_count = len(list(prefix_code_generator()))
    print "number of elements:", elements_count
    
    #split into training and testing samples
    print "splitting into training and testing..."
    train_inds, test_inds = randomly_divide(elements_count, int(elements_count/10))
    train_generator = lambda: gen_record_fromshifts(prefix_code_generator, train_inds)
    test_generator = lambda: gen_record_fromshifts(prefix_code_generator, test_inds)
    print "splitted."
    
    #train mlknn:
    print "training distance..."
    zbldistance = jaccard_distance.JaccardDistance(train_generator, elements_count-int(elements_count/10), distancetrainingsteps)
    #zbldistance = lsi_distance.LsiDistance(train_generator, elements_count-int(elements_count/10), distancetrainingsteps, number_of_topics = 100)
    print "training mlknn..."
    mk = mlknn.MlKnn(train_generator, zbldistance, find_closest_points.find_closest_points, 
                         k, smoothingparam)
    
    classify_oracle = lambda x: mc2lmc_tomka_blad(x)
    print "----------------------------------------------------"
    print "MLKNN:"
    multilabel_evaluate_printresults(test_generator, classify_oracle, mk.classify, len(labels), 
                    {'full label': lambda x: x, 'half label': lambda x: x[:3], 'low label': lambda x: x[:2]})
    
    print "----------------------------------------------------"
    print "STUPID KNN:"
    multilabel_evaluate_printresults(test_generator, classify_oracle, mk.classify_stupid, len(labels), 
                    #{'full label': lambda x: x, 'short label': lambda x: x[:1]})
                    {'full label': lambda x: x, 'half label': lambda x: x[:3], 'low label': lambda x: x[:2]})