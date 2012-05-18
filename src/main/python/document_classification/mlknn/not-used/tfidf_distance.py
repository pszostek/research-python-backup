'''
Created on Jan 11, 2012

@author: mlukasik
'''
from __future__ import division
from intersection_distance import IntersectionDistance

import sys, os
lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
sys.path.append(lib_path)

#from tools.cosine_similarity import cosine_distance
from tools.stop_words_list import STOP_WORDS_LIST
from doc_features.semantic_gensim import build_dictionary, line_to_bag_of_ids, corpora_to_bag_of_ids_generator, build_tfidf_model, bag_of_ids_tfidf_generator, build_lsi_model

class TdifdfDistance(IntersectionDistance):
    """
    Encapsulates distance calculations between Zbl records.
    
    """
    def __init__(self, frecords, frecords_size, training_turns, stopwords = STOP_WORDS_LIST, number_of_topics = 100):
        """
        Build LSI model.
        Train weights and shifts.
        
        """
        self.number_of_topics = number_of_topics

        self.dictionary = build_dictionary( frecords())

        self.corpus = corpora_to_bag_of_ids_generator( frecords(), self.dictionary)
        self.tfidf = build_tfidf_model(self.corpus)    
        self.corpus = corpora_to_bag_of_ids_generator( frecords(), self.dictionary)
        self.corpus_tfidf = bag_of_ids_tfidf_generator(self.corpus, self.tfidf)
            
        self.lsi = build_lsi_model(self.corpus_tfidf, self.dictionary, self.number_of_topics)
        
        self.stopwords = stopwords
        self.weights, self.shifts = self.calc_weights(frecords, frecords_size, training_turns)
        
    def dist_txt(self, x, y):
        """
        Calculates distance between 2 given texts.
        
        """
        