'''
Created on Nov 14, 2011

@author: mlukasik

Convert record into a vector of counts of given words
'''
import sys
sys.path.append(r'../')
from tools import text2words
from wordsfreq import select_descriptive_words
from zbl2py import record_read

def calc_word_feats(s, words):
    """Calculate number of occurences of words in s"""
    occurences = {}
    for w in words:
        occurences[w] = 0
    
    for w in text2words.text_to_words(s):
        if w in occurences:
            occurences[w] += 1
            
    return [occurences[w] for w in words]

def convert_records_to_words(records, words):
    """Convert list of records into list of words counts"""
    for rec in records:
        try:
            title = rec['ti']
            descr = rec['descr']
            kw = " ".join(rec['kw'])
    
            feats = calc_word_feats(" ".join([title, descr, kw]), words)
            yield (feats, rec['categories'])
        except:
            continue
        

if __name__ == '__main__':
    words = select_descriptive_words.select_descriptive_words_quotientmethod(sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]))
    for i in convert_records_to_words(record_read.read_list_records(sys.argv[4]), words):
        print i