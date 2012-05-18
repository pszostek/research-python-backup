'''
Created on Dec 13, 2011

@author: mlukasik
'''
from tfidf import TfIdf
import os, sys
lib_path = os.path.abspath(os.path.sep.join(['..', '..', '..', 'document_classification']))
sys.path.append(lib_path)
from data_io.zbl_record_generators import gen_text, gen_text_mc
        
#needed by lsa
import numpy as np
from scipy.linalg import svd
import scipy.sparse
from sparsesvd import sparsesvd

def tfidf_matrix(text_generator):
    """Builds tf-idf matrix from records from fname, using fields to create a text describing them
    
    """
    
    ti = TfIdf()
    #print "building tfidf indices"
    for i in text_generator:
        ti.add_input_document(i)
        
    A = np.zeros([ti.num_docs, len(ti.term_num_docs)])
    
    for i_ind, i in enumerate(text_generator):
        #print "-i_ind, i:", i_ind, i
        for j_ind, j in enumerate(ti.get_tfidf(i)):
            #print "-----j_ind, j:", j_ind, j
            A[i_ind, j_ind] = j
    #print ti.term_num_docs
    return A, ti
        
def find_concept_space(A, num_of_concepts = 0):
    """Convert A into a concept space matrix, reducing the dimensionality (result no 1); 
    return a matrix allowing mapping of new vertices representing documents into the concept space (result no 2);
    
    A.rows - documents
    A.cols - terms
    elements of A - numerical
    
    Sparse matrix assumed.
    
    """
    if not num_of_concepts:
        num_of_concepts = min(int(A.shape[1]/3), 100)#maximum 100 concepts
        num_of_concepts = max(num_of_concepts, 10)#minimum 10 concepts
    
    smat = scipy.sparse.csc_matrix(A) # convert to sparse CSC format
    ut, s, vt = sparsesvd(smat, num_of_concepts) # do SVD
    
    return np.transpose(ut), np.transpose(vt)
        
if __name__ == '__main__':
    #fname = sys.argv[1]
    #fields = sys.argv[2:]
    #text_generator = lambda: gen_text(fname, fields)
    #print "fname:", fname
    
    doc1 = "mama ma kota a kot ma krowe"
    doc2 = "tata ma psa a pies ma kota"
    doc3 = "osiol osiol ma lalalala"
    doc4 = "tata ma tata"
    doc5 = "michal mateusz maciej"
    doc6 = "michal mateusz maciej"
    f = [doc1, doc2, doc3, doc4, doc5, doc6]
    
    
    A, ti = tfidf_matrix(f)
    Aconcept, all2concept = find_concept_space(A, num_of_concepts = 0)
    
    for query in ["michal", "mateusz", "tata", "ma", "osiol", "kota"]:
        print "query:", query
        vquery = ti.get_tfidf(query)
        print np.dot(vquery, all2concept)
    
    """titles =[
    "The Neatest Little Guide to Stock Market Investing",
    "Investing For Dummies, 4th Edition",
    "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
    "The Little Book of Value Investing",
    "Value Investing: From Graham to Buffett and Beyond",
    "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
    "Investing in Real Estate, 5th Edition",
    "Stock Investing For Dummies",
    "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"
    ] """
    #f=titles
    
    """"A = tfidf_matrix(f)
    
    
    import numpy, scipy.sparse
    from sparsesvd import sparsesvd
    #mat = numpy.random.rand(200, 10) # create a random matrix
    smat = scipy.sparse.csc_matrix(A) # convert to sparse CSC format
    ut, s, vt = sparsesvd(smat, 3) # do SVD, asking for 100 factors
    #assert numpy.allclose(mat, numpy.dot(ut.T, numpy.dot(numpy.diag(s), vt)))
    print "ut:"
    print ut
    print "s:"
    print s
    print "vt:"
    print vt
    print "U.shape, s.shape, vt.shape:", ut.shape, s.shape, vt.shape
    """
    
    """"U, s, V = np.linalg.svd(A, full_matrices=True)
    S = np.zeros((A.shape[0], A.shape[1]), dtype=complex)
    print "U.shape, V.shape, s.shape, S.shape:", U.shape, V.shape, s.shape, S.shape
    S[:A.shape[0], :A.shape[0]] = np.diag(s)
    print np.allclose(A, np.dot(U, np.dot(S, V)))
    #print np.dot(U, np.dot(S, V))
    #print "A:"
    #print A
    #print "------------------"
    #print "U:", U
    #print "------------------"
    #print "s:", s
    #print "------------------"
    #print "V:", V
    #print "------------------"
    #print "------------------"
    #print np.dot(np.dot(np.transpose(V), np.transpose(S)), np.dot(S, V))
    print "U"
    print U
    print "------------------"
    print "S"
    print S
    print "------------------"
    print "V"
    print V
    print "------------------"
    #print "A"
    #print A
    #print dot(dot(U, diag(S)), Vt)"""