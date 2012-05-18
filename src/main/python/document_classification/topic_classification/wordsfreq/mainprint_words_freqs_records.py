'''
Created on Nov 9, 2011

@author: mlukasik
'''
import sys
import os
lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
sys.path.append(lib_path)
from tools.text2words import text_to_words
from data_io.zbl_record_generators import gen_record

from collections import defaultdict
    
def words_freqs(records, features):
    #count each word in abstract and title:
    all_w = 0
    words = defaultdict(lambda: 0)
    for rec in gen_record(records, features+['mc']):
        words_l = text_to_words(" ".join([rec[f] for f in features]) )
        for c in words_l:
            words[c]+=1
            all_w+=1
    print "count of all words:", all_w
    print "words found:"
    w_sorted = sorted(list(words.iteritems()), key=lambda x:x[1], reverse=True)
    for k, v in w_sorted:
        print k, ":", v
    
if __name__=="__main__":
    words_freqs(sys.argv[1], sys.argv[2:])