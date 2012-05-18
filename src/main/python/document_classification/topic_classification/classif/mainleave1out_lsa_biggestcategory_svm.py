'''
Created on Dec 15, 2011

@author: mlukasik
'''
import sys
sys.path.append(r'../') 
from features import lsa
from features.lsa import tfidf_matrix, find_concept_space
from stattools.low2high_msc import highlevel2lowlevel
from stattools.most_common_category import extract_most_common_categ
#from classifier_tester import LeaveOneOutAllCategories
#from classifier_svm import SvmSingleTagWordsClassifier

import os
#lib_path = os.path.abspath(os.path.sep.join(['..', 'topic_classification']))
#sys.path.append(lib_path)

lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
sys.path.append(lib_path)
from data_io.zbl_record_generators import gen_text_mc
from data_io import zbl_io

if __name__ == '__main__':
    #read words that are most important:
    fname = sys.argv[1]
    feature_tags = sys.argv[2:]
    
    print "Arguments read:"
    print "fname =", fname
    print "feature_tags =", feature_tags
    
    #1. find the most common category:
    most_common_categ = extract_most_common_categ( highlevel2lowlevel( gen_text_mc(fname, feature_tags), zbl_io.MULTIVAL_FIELD_SEPARATOR) )#but converting to high level!
    print "found most_common_categ:", most_common_categ
    
    #A, ti = tfidf_matrix(f)
    #Aconcept, all2concept = features_to_concept_space(A, num_of_concepts = 0)
    
    #for query in ["michal", "mateusz", "tata", "ma", "osiol", "kota"]:
    #    print "query:", query
    #    vquery = ti.get_tfidf(query)
    #    print np.dot(vquery, all2concept)
    
    #loo = LeaveOneOutAllCategories(SvmWordsClassifier, frecords)
    #corr = loo.test(test_samples)
    #print "Correctness:", corr