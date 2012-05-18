'''
Created on Nov 3, 2011

@author: mlukasik
'''
from __future__ import division
from itertools import izip

import sys
sys.path.append(r'../')
from tools.stop_words_list import STOP_WORDS_LIST
from tools.text_to_words import text_to_words

class JaccardDistance(object):
    """
    Encapsulates distance calculations between Zbl records.
    
    Calculates a jaccard index between texts representing the 2 documents.
    
    The texts are built by merging the: abstracts, titles and keywords.
    
    ------------
    Old comment:
    A propo problemu dopasowywania autorow:
    Problem grafowy: lepiej zrobic tak, ze wybieramy minimalny blad dopasowujac autorow 
    - do tego moze lepiej poczytac Cormena. Moze tez algorytm wegierski, biorac pierwszych min, 
    ale to bedzie troszke gorsze niz wczesniejszy pomysl.
    
    """
    def __init__(self, frecords, frecords_size, training_turns, 
                 stopwords = STOP_WORDS_LIST):
        """
        Train weights and shifts.
        
        """
        self.stopwords = stopwords
        
    def dist_txt(self, x, y):
        """
        Calculates distance between 2 given texts.
        
        It calculates more or less 1 - (set(x)&set(y) / set(x)|set(y)).
        More or less, because the repetitions indicate the similarity as well.
        
        TESTED.
        """
        #x_s = set(text_to_words(x))
        #y_s = set(text_to_words(y))
        #return len(x_s & y_s)/len(x_s | y_s)
        x_words = sorted( filter(lambda x: x not in self.stopwords ,text_to_words(x)))
        y_words = sorted( filter(lambda x: x not in self.stopwords ,text_to_words(y)))
        
        x_ind = 0
        y_ind = 0
        
        diff = 0
        while x_ind < len(x_words) or y_ind < len(y_words):
            if x_ind==len(x_words):
                diff+=len(y_words)-y_ind
                break
            elif y_ind==len(y_words):
                diff+=len(x_words)-x_ind
                break
            else:
                if x_words[x_ind] > y_words[y_ind]:
                    y_ind+=1
                    diff+=1
                elif x_words[x_ind] < y_words[y_ind]:
                    x_ind+=1
                    diff+=1
                else:
                    x_ind+=1
                    y_ind+=1
        
        return diff/(len(x_words)+len(y_words))
    
    def distance(self, x, y):
        """
        Calculates distance between records: x and y.
        
        TESTED.
        
        """
        return self.dist_txt(" ".join([x['ab'], x['ti'], x['ut']]), 
                                  " ".join([y['ab'], y['ti'], y['ut']]))