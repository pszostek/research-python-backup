'''
Created on Jan 11, 2012

@author: mlukasik
'''

def find_closest_points_gensim(sample, records, excluding, k, gensimdata):
    """
    Find k closest records and return them. Wrapper for gensim library.
    
    sample - record that we are looking neighbours of
    records - a function returning a generator of records 
    excluding - list of records not to consider
    k - number of closest points to find
    gensimdata - data about the transform: 
                transformation method of queries from gensim library (lsi, lda, tfidf...)
                index for queries from gensim library (lsi, lda, tfidf...)
                
    """
    #vec_bow = dictionary.doc2bow(doc.lower().split())
    #vec_lsi = lsi[vec_bow] # convert the query to LSI space
    vec_representation = gensimdata.transform(sample)
    sims = gensimdata.index[vec_representation] # perform a similarity query against the corpus
    sims = sorted(enumerate(sims), key=lambda item: -item[1])