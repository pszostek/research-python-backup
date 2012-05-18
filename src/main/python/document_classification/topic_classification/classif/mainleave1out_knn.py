'''
Created on Nov 16, 2011

@author: mlukasik
'''
import sys
sys.path.append(r'../') 
from zbl2py import record_read
from classifier_tester import LeaveOneOutAllCategories
from classifier_knn import KnnMatrixClassifier

import os
#lib_path = os.path.abspath(os.path.sep.join(['..', 'topic_classification']))
#sys.path.append(lib_path)

lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
sys.path.append(lib_path)
from data_io.zbl_record_generators import gen_record, mc2lmc_tomka_blad

if __name__ == '__main__':
    records_file = sys.argv[1]
    test_samples = int(sys.argv[2])
    
    print "Arguments read:"
    print "records_file =", records_file
    print "test_samples =", test_samples
    
    frecords = lambda: gen_record(records_file, ['mc', 'ti', 'ab', 'au'])

    #loo = LeaveOneOutAllCategories(KnnMatrixClassifier, frecords, mc2lmc_tomka_blad)
    #corr = loo.test(test_samples)
    #print "Correctness:", corr
    print "---training a classifier..."
    knn = KnnMatrixClassifier(frecords, 7000, 100, mc2lmc_tomka_blad)
    print "---performing leave one out..."
    corr = knn.loo(test_samples)
    print "COrrectness:", corr