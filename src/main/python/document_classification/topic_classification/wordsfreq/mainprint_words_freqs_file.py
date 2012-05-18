'''
Created on Nov 13, 2011

@author: mlukasik
'''
import sys
import os
lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
sys.path.append(lib_path)
from tools.text2words import text_to_words

from collections import defaultdict

def print_words_freqs(filename):
    #count each word in abstract and title:
    words = defaultdict(lambda: 0)
    all_w=0
    with open(filename) as f:
        for line in f:
            words_l = text_to_words(line)
            for c in words_l:
                words[c]+=1
                all_w+=1
    print "count of all words:", all_w
    print "words found:"
    w_sorted = sorted(list(words.iteritems()), key=lambda x:x[1], reverse=True)
    for k, v in w_sorted:
        print k, ":", v
    
if __name__=="__main__":
    print_words_freqs(sys.argv[1])