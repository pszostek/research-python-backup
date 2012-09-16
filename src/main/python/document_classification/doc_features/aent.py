from __future__ import division
import math
import sys, pickle
from itertools import izip

sys.path.append(r'../')
sys.path.append(r'../../')
from data_io import zbl_io

log2    = lambda v: math.log(v, 2)
log     = lambda v: math.log(v)

##########################################################################################

def build_ngrams(words, n = 2, ngram_separator = '-'):
    """Converts single words into n-grams by merging words."""
    ngrams = [ reduce(lambda w1,w2: w1+ngram_separator+w2, words[i:i+n]) for i in xrange(len(words)-n+1) ]
    return ngrams 

def build_mgrams(words, maxn, ngram_separator = '-'):
    """Converts single words into list of [single-words+bigrams+3-grams+...+N-grams]."""
    mgrams = list(words)
    for n in xrange(2, min(maxn, len(words)+1)) :
         mgrams.extend( build_ngrams(words, n, ngram_separator) )
    return mgrams

##########################################################################################

def entropy(wordsmodel, wordid):
    """Calculates entropy using only information about counts."""
    s = 0.0
    for doc_wordid2count in wordsmodel.docs_wordid2count:
        p = tf(doc_wordid2count, wordid) / wordsmodel.gf(wordid) 
        if p>0.0:
            s = s + p*log2(p)
    return 1.0 + s / log2(wordsmodel.N())


if __name__=="__main__":

    maxn = 4 
    list_of_fields = ['ti', 'ut', 'ab']
    try:
        fin = sys.argv[1]
    except:
        print "Argument expected: src-Zbl-file path"
        sys.exit(-1)
    print "src=", fin
        
    try:
        if sys.argv[1]==sys.argv[2]:
            system.exit(-1)
            print "Paths must be different!"
        fout = open(sys.argv[2], "w")
    except:
        print "Argument expected: output-Zbl-file path"
        sys.exit(-1)
    print "dst=", fout    
    
    print "LOADING"
    docs = []        
    for N, record in enumerate(zbl_io.read_zbl_records(open(fin))):
        if N%500==0: print N, "read"
        doc = []
        for field in list_of_fields:
            if not record.has_key(field): continue
            words = record[field].split()
            modified_words = build_mgrams(words, maxn)
            doc.extend(modified_words)
        if len(doc)>0: docs.append(doc)

    print "CALC terms vs counts"
    term2count = {}
    docs_term2count = []    
    docs_len = []    
    for doc in docs:
        doc_term2count = {}
        for term in doc:
            term2count[term]        = term2count.get(term, 0) + 1
            doc_term2count[term]    = doc_term2count.get(term, 0) + 1
        docs_term2count.append(doc_term2count)
        docs_len.append(len(doc))
    
    numdocs = len(docs_term2count)
    numwords = sum(term2count.values())
    print "numdocs=",  numdocs      
    print "term2count=",str(list(term2count.iteritems())[:10])[:300]
    print "numwords=",numwords
    print "docs_term2count=",str(docs_term2count)[:300]
    print "docs_len=",str(docs_len)[:300]
                    
    print "GROUPING ngrams"
    n2terms = {}
    for term in term2count:
        n = term.count("-")+1
        terms = n2terms.get(n, set())
        terms.add(term)
        n2terms[n] = terms
    print "n2terms=",str(list(n2terms.iteritems())[:10])[:300]
    print "len(n2terms[1])=",len(n2terms.get(1, [])),"->", str(n2terms.get(1, []))[:300]
    print "len(n2terms[2])=",len(n2terms.get(2, [])), "->", str(n2terms.get(2, []))[:300]
    print "len(n2terms[3])=",len(n2terms.get(3, [])),"->", str(n2terms.get(3, []))[:300]        
    

    print "CALC term vs. entropy"    
    term2ent = {}
    for i,term in enumerate(term2count):
        if i%500 == 0: print i,"out of", len(term2count)
         
        s = 0.0 #evaluate entropy for term 
        for doc_term2count, doc_len in izip(docs_term2count, docs_len): #over all documents
            tf = doc_term2count.get(term, 0) / doc_len
            gf = term2count.get(term, 0) / numwords
            p = tf / gf
            if p>0.0:
                s = s + p*log2(p)
                
        term2ent[term] = 1.0 + s / log2(numdocs)
        #print term, " -> ", term2ent[term]

    selected = set()
    for term3 in n2terms[3]:
        terms1 = term3.split("-") 
        if len(terms1)>3:
            print "Problem here:", terms1 
            sys.exit(-3)       
        terms2 = [terms1[0]+"-"+terms1[1], terms1[1]+"-"+terms1[2]]        
        
        ent0 = term2ent[ term3 ]
        ent1 = term2ent[ terms1[0] ]+term2ent[ terms1[1] ]+term2ent[ terms1[2] ]
        ent2 = term2ent[ terms2[0] ]+term2ent[ terms1[2] ]
        ent3 = term2ent[ terms1[0] ]+term2ent[ terms2[1] ]
    
        entmax = max([ent0, ent1, ent2, ent3])
        if ent0 == entmax:
            selected.update( term3 )
        elif ent1 == entmax:
             selected.update( terms1 )
        elif ent2 == entmax:
             selected.update( [terms2[0], terms1[2]] )
        elif ent3 == entmax:
             selected.update([ terms1[0], terms2[1] ] )
        else:
            print "ent wtf?"
            sys.exit(-1)
            
    print "selected=", str(list(selected)[:30])[:300]
    print "len(selected)=",len(selected)
    
    print "GROUPING ngrams"
    n2terms = {}
    for term in selected:
        n = term.count("-")+1
        terms = n2terms.get(n, set())
        terms.add(term)
        n2terms[n] = terms
    print "n2terms=",str(list(n2terms.iteritems())[:10])[:500]
    print "len(n2terms[1])=",len(n2terms.get(1, [])),"->", str(n2terms.get(1, []))[:500]
    print "len(n2terms[2])=",len(n2terms.get(2, [])), "->", str(n2terms.get(2, []))[:500]
    print "len(n2terms[3])=",len(n2terms.get(3, [])),"->", str(n2terms.get(3, []))[:500]
    
    print "REPROCESSING src file"            
    for N, record in enumerate(zbl_io.read_zbl_records(open(fin))):
        if N%500==0: print N, "read"
        doc = []
        for field in list_of_fields:
            if not record.has_key(field): continue
            words = record[field].split()
            
            selected_words = []
            prohibited = set()
            mgrams = []
            for n in xrange(min(maxn, len(words)+1), 1, -1):
                ngrams = build_ngrams(words, n, ngram_separator)
                ngrams = [w for w in ngrams if w in selected]
                                
                mgrams.extend( ngrams )
                
            modified_words = build_mgrams(words, maxn)
                        
            selected_words = [w for w in modified_words if w in selected]
            try:
                record[field] = reduce(lambda w1,w2: (w1)+' '+(w2), selected_words)
            except:
                print "ERR:", modified_words," -> ",selected_words
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
        