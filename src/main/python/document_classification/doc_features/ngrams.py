"""N-grams calculation."""

import sys, pickle
import tempfile                 

sys.path.append(r'../')
sys.path.append(r'../../')
import data_io
from data_io import *
from data_io import zbl_io

import logging

##########################################################################################################################################    

def build_ngrams(words, n = 2, ngram_separator = '-'):
    """Converts single words into n-grams by merging words."""
    ngrams = [ reduce(lambda w1,w2: w1+ngram_separator+w2, words[i:i+n]) for i in xrange(len(words)-n+1) ]
    return ngrams 
    
def build_ngrams_with_endings(words, n = 2, ngram_separator = '-'):
    """Converts single words into n-grams by merging words.

    Keeps shorter n-grams at the ending.
    """
    ngrams = [ reduce(lambda w1,w2: w1+ngram_separator+w2, words[i:i+n]) for i in xrange(len(words)) ]
    return ngrams 

def build_mgrams(words, maxn, ngram_separator = '-'):
    """Converts single words into list of [single-words+bigrams+3-grams+...+N-grams]."""
    mgrams = list(words)
    for n in xrange(2, min(maxn, len(words)+1)) :
         mgrams.extend( build_ngrams(words, n, ngram_separator) )
    return mgrams
    
##########################################################################################################################################    

def modify_wordslist_file(fin, fout, list_of_fields, wordslist_modifier):
    """Converts single words in selected fields into n-grams by merging words.
    
    wordslist_modifier(words list) -> modified_words list
    """
    for record in zbl_io.read_zbl_records(fin):
        for field in list_of_fields:
            if not record.has_key(field): continue
            words = record[field].split()
            modified_words = wordslist_modifier(words)
            if len(modified_words) <= 0: 
                logging.warn("Error in an="+str(record[zbl_io.ZBL_ID_FIELD])+" in field "+ str(field)+ "="+str(record[field])+". Using single words instead.")
                modified_words = words
            record[field] = reduce(lambda w1,w2: (w1)+' '+(w2), modified_words)
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
                
def build_ngrams_file(fin, fout, list_of_fields, n = 2, ngram_separator = '-', keep_endings = False):
    """Converts single words in selected fields into n-grams by merging words."""
    if keep_endings:
        ngram_calculator = lambda words: build_ngrams_with_endings(words, n, ngram_separator)
    else:
        ngram_calculator = lambda words: build_ngrams(words, n, ngram_separator)
    #print "[build_ngrams_file] ngram_calculator =",ngram_calculator    
    modify_wordslist_file(fin, fout, list_of_fields, ngram_calculator)
    
def build_mgrams_file(fin, fout,  list_of_fields, maxn = 2, ngram_separator = '-'):
    """Converts single words into list of [single-words+bigrams+3-grams+...+N-grams]."""    
    mgram_calculator = lambda words: build_mgrams(words, maxn, ngram_separator)
    modify_wordslist_file(fin, fout, list_of_fields, mgram_calculator)
    
    
