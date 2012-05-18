'''
Created on Nov 23, 2011

@author: mlukasik
'''
import sys
sys.path.append(r'../') 
from wordsfreq import select_descriptive_words
from features import records_to_words_weights_converter
from zbl2py import record_read
from classifier_tester import LeaveOneOut
from classifier_tree import TreeSingleTagWordsClassifier
from mainleave1out_biggestcategory_svm import extract_most_common_categ

if __name__ == '__main__':
    #read words that are most important:
    extr_fromfname = sys.argv[1]
    basefname = sys.argv[2]
    words_count = int(sys.argv[3])
    thresh_div = float(sys.argv[4])
    records_file = sys.argv[5]
    test_samples = int(sys.argv[6])
    
    print "Arguments read:"
    print "extr_fromfname =", extr_fromfname
    print "basefname =", basefname
    print "words_count =", words_count
    print "thresh_div =", thresh_div
    print "records_file =", records_file
    print "test_samples =", test_samples
    
    words = select_descriptive_words.select_descriptive_words_quotientmethod(extr_fromfname, basefname, words_count, thresh_div)
    #read records and convert them into feature-vectors:
    frecords = list(records_to_words_weights_converter.convert_records_to_words(record_read.read_list_records(records_file), words))
    #create frecors with numerical etiquettes:
    #build multi-label-SVM based on this data:
    most_common_categ, max_cnt = extract_most_common_categ(frecords)
    print "Most common category is:", most_common_categ, " with ", max_cnt, " occurences."
    
    loo = LeaveOneOut(lambda samples: TreeSingleTagWordsClassifier(most_common_categ, samples, featurenames=words), frecords, lambda x: [int(most_common_categ in x[1])])
    corr = loo.test(test_samples)
    print "Correctness:", corr