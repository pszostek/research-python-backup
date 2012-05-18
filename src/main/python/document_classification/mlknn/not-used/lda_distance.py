'''
Created on Jan 2, 2012

@author: mlukasik
'''
from __future__ import division
from intersection_distance import IntersectionDistance

#import sys, os
#lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
#sys.path.append(lib_path)

import sys
sys.path.append(r'../')

#from tools.cosine_similarity import cosine_distance
from tools.stop_words_list import STOP_WORDS_LIST
from doc_features.semantic_gensim import build_dictionary, line_to_bag_of_ids, corpora_to_bag_of_ids_generator, build_tfidf_model, bag_of_ids_tfidf_generator, build_lda_model
from itertools import izip
import math

class LdaDistance(IntersectionDistance):
    """
    Encapsulates distance calculations between Zbl records.
    
    
    Old comment:
    A propo problemu dopasowywania autorow:
    Problem grafowy: lepiej zrobic tak, ze wybieramy minimalny blad dopasowujac autorow 
    - do tego moze lepiej poczytac Cormena. Moze tez algorytm wegierski, biorac pierwszych min, 
    ale to bedzie troszke gorsze niz wczesniejszy pomysl.
    
    """
    def __init__(self, frecords, frecords_size, training_turns, stopwords = STOP_WORDS_LIST, number_of_topics = 100):
        """
        Build LDA model.
        Train weights and shifts.
        
        """
        self.number_of_topics = number_of_topics
        #zbl_reader = zbl_generator  #for not filtered data

        self.dictionary = build_dictionary( frecords())

        self.corpus = corpora_to_bag_of_ids_generator( frecords(), self.dictionary)
        self.tfidf = build_tfidf_model(self.corpus)    
        self.corpus = corpora_to_bag_of_ids_generator( frecords(), self.dictionary)
        self.corpus_tfidf = bag_of_ids_tfidf_generator(self.corpus, self.tfidf)

        self.lda = build_lda_model(self.corpus_tfidf, self.dictionary, self.number_of_topics)
        
        self.stopwords = stopwords
        self.weights, self.shifts = self.calc_weights(frecords, frecords_size, training_turns)
        
    def dist_txt(self, x, y):
        """
        Calculates distance between 2 given texts.
        
        """
        return math.sqrt(sum(pow(i-j, 2) for i, j in izip(self.lsi[self.tfidf[line_to_bag_of_ids(x, self.dictionary, lambda x: x)]], 
                               self.lsi[self.tfidf[line_to_bag_of_ids(y, self.dictionary, lambda x: x)]])))