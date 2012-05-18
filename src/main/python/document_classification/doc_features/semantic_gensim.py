"""Text features: LSA, LDA, RP Projections built basing on GENSIM framework."""
import sys, os, time
sys.path.append(r'../')

from gensim import corpora, models, similarities
from tools.stop_words_list import STOP_WORDS_LIST
from tools.text_to_words import text_filter_lower
from data_io import zbl_record_generators

from semantic_gensim_readers import zbl_generator 
from semantic_gensim_readers import zbl_generator_q

import logging

#########################################################################################
#CONVERSION TO ID + COUNTS

def build_dictionary(wordslist_generator, stoplist = STOP_WORDS_LIST, min_freq=2):
    """Builds dictionary {word:id} of words from wordslist_generator (e.g. list of lists of words). 
    
    Words that are on the stoplist or have frequency less than min_freq are not included.
    """
    # collect statistics about all tokens:
    dictionary = corpora.Dictionary(wordslist_generator)
    # remove stop words and words that appear just several times
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < min_freq]        
    logging.info("removing stopwords and words with that occurr < min_freq. Before dictionary="+str(dictionary))
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear just few times
    logging.info("removing stopwords and words with that occurr < min_freq. After dictionary="+str(dictionary))
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    return dictionary

def build_dictionary_q(wordslist_generator):
    """Builds dictionary {word:id} of words from wordslist_generator (e.g. list of lists of words). """
    # collect statistics about all tokens:
    dictionary = corpora.Dictionary(wordslist_generator)
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    return dictionary

def line_to_bag_of_ids(line, dictionary, line_filter=text_filter_lower):
    """Returns new representation (list of pairs (word_id:count) ) of a line using ids from dictionary.    
    
    Words not included in dictionary are omitted."""
    list_of_words = line_filter(line).split()
    return dictionary.doc2bow(list_of_words)

def corpora_to_bag_of_ids_generator(wordslist_generator, dictionary):
    """Returns generator that takes documents from wordslist_generator 
    (e.g. list of lists of words, single list of words = single document) and
    generates lists of pairs (word_id:count).
    
    Words not included in dictionary are omitted.
    """
    return ( dictionary.doc2bow(list_of_words) for list_of_words in wordslist_generator )


#########################################################################################
#TFIDF:

def build_tfidf_model(bag_of_ids_generator):
    """Builds TFIDF model out of corpus (generator of lists of pairs (word_id:count))."""
    return models.TfidfModel(bag_of_ids_generator)

def bag_of_ids_tfidf(bag_of_ids, tfidf):
    """Takes list of pairs (word_id:count) and convert to (word:tfidf value) using tfidf model."""
    return tfidf[bag_of_ids]

def bag_of_ids_tfidf_generator(bag_of_ids_generator, tfidf):
    """Reads from corpora (generator of lists of pairs (word_id:count)) and
    generates lists of pairs (word_id: tfidf value) using tfidf model."""
    return tfidf[bag_of_ids_generator]

#########################################################################################
#LSI, LDA, RP PROJECTIONS:

def build_lsi_model(bag_of_ids_vals_generator, dictionary, number_of_topics):
    """Reads from generator of lists of pairs (word_id: value) and builds
    LSI model for given number_of_topics."""
    return models.LsiModel(bag_of_ids_vals_generator, id2word=dictionary, num_topics=number_of_topics)
    
def build_lda_model(bag_of_ids_vals_generator, dictionary, number_of_topics):
    """Reads from generator of lists of pairs (word_id: value) and builds
    LDA model for given number_of_topics."""
    return models.LdaModel(bag_of_ids_vals_generator, id2word=dictionary, num_topics=number_of_topics)

def build_rp_model(bag_of_ids_vals_generator, dictionary, number_of_topics):
    """Reads from generator of lists of pairs (word_id: value) and builds
    RP Projections model for given number_of_topics."""
    return models.RpModel(bag_of_ids_vals_generator, id2word=dictionary, num_topics=number_of_topics)


#########################################################################################
#########################################################################################
#########################################################################################

    
if __name__ == "__main__":
    print "Builds TFIDF, LSI, LDA models for corpus."
    try:
        zbl_corpora_path = sys.argv[1]
        number_of_topics = int(sys.argv[2])
    except: 
        print "Two arguments expected: zbl-file number-of-topics"
        exit(-1)
        
    print "zbl_corpora_path =", zbl_corpora_path
    print "number_of_topics =", number_of_topics
    
    #zbl_reader = zbl_generator  #for not filtered data
    zbl_reader = zbl_generator_q #for already filtered data

    #Dictionary:
    start = time.clock()
    dictionary = build_dictionary( zbl_reader(zbl_corpora_path, ['ab'], ['mc']) )
    print dictionary
    print "Building dictionary:", time.clock()-start
    
    #TFIDF model + corpus:
    start = time.clock()
    corpus = corpora_to_bag_of_ids_generator( zbl_reader(zbl_corpora_path, ['ab'], ['mc']), dictionary)
    tfidf = build_tfidf_model(corpus)    
    corpus = corpora_to_bag_of_ids_generator( zbl_reader(zbl_corpora_path, ['ab'], ['mc']), dictionary)
    corpus_tfidf = bag_of_ids_tfidf_generator(corpus, tfidf)
    print "Building TFIDF:", time.clock()-start

    #LDA model + corpus:
    start = time.clock()
    lda = build_lda_model(corpus_tfidf, dictionary, number_of_topics)
    corpus = corpora_to_bag_of_ids_generator( zbl_reader(zbl_corpora_path, ['ab'], ['mc']), dictionary)
    corpus_tfidf = bag_of_ids_tfidf_generator(corpus, tfidf)
    corpus_lda = lda[corpus_tfidf]
    print "Building LDA:", time.clock()-start
        
    #LSI model + corpus:
    start = time.clock()
    lsi = build_lsi_model(corpus_tfidf, dictionary, number_of_topics)
    corpus = corpora_to_bag_of_ids_generator( zbl_reader(zbl_corpora_path, ['ab'], ['mc']), dictionary)
    corpus_tfidf = bag_of_ids_tfidf_generator(corpus, tfidf)
    corpus_lsi = lsi[corpus_tfidf]
    print "Building LSI:", time.clock()-start
    
    print "Reconstructing:"
    for rec in zbl_generator(zbl_corpora_path, ['ab'], ['mc']):
        print "---"
        print rec
        print line_to_bag_of_ids(' '.join(rec), dictionary)
        print tfidf[line_to_bag_of_ids(' '.join(rec), dictionary)]
        print lda[tfidf[line_to_bag_of_ids(' '.join(rec), dictionary)]]
