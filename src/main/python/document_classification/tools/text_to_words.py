#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 14, 2011

@author: mlukasik
@author: tkusm
'''

import string
from stop_words_list import STOP_WORDS_LIST


def text_filter(text, replace_with = ''):
    """Removes punctuation, digits, specific characters..."""
    #print type(text), text
    text_nopunct = str(text)
    #text_nopunct = str(text).translate(string.maketrans("",""), string.punctuation)
    for c in string.punctuation:
        text_nopunct = text_nopunct.replace(c, replace_with)
    #text_nopunct = text_nopunct.translate(string.maketrans("",""), string.digits)
    for c in string.digits:
        text_nopunct = text_nopunct.replace(c, replace_with)        
    text_nopunct = text_nopunct.replace('”', replace_with)
    text_nopunct = text_nopunct.replace('“', replace_with)
    text_nopunct = text_nopunct.replace('‘', replace_with)
    text_nopunct = text_nopunct.replace('’', replace_with)
    text_nopunct = text_nopunct.replace('\'', replace_with)
    text_nopunct = text_nopunct.replace('  ', replace_with)
    return text_nopunct 


def text_filter_lower(text, replace_with_str = ''):
    """Returns lower case of text_filter."""
    #print ("[text_filter_lower] text="+str(text)+" replace_with_str=["+str(replace_with_str)+"]")
    return text_filter(text, replace_with = replace_with_str).lower()



def text_to_words(text):
    """
    Extract words from a text. 
    Replace specific characters, delete digits, ignore words of length 1.
    
    """
    text_nopunct = text_filter(text)
    return map(string.lower, filter(lambda x: len(x)>1, unicode(text_nopunct, errors='ignore').split()))




def default_word_predicate(word, stoplist = STOP_WORDS_LIST):
    """Returns true if word length > 1 and word is not on the stoplist."""
    return len(word)>1 and not word in stoplist


def words_filter(text, word_predicate=default_word_predicate):
    """Removes from text words for which word_predicate returns false."""
    words = text.split()
    try:
        return reduce(lambda w1,w2: w1+" "+w2, (w for w in words if word_predicate(w)) )
    except:
        return ""



