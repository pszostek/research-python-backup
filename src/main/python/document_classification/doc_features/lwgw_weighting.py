"""LWxGW (TFxIDF like) weighting methods."""
from __future__ import division

import sys, pickle
import tempfile                 

sys.path.append(r'../')
sys.path.append(r'../../')
import data_io
from data_io import *
from data_io import zbl_io
import math

import logging


#########################################################################

log2    = lambda v: math.log(v, 2)
log     = lambda v: math.log(v)

#########################################################################

def tf(doc_wordid2count, wordid):
    return doc_wordid2count.get(wordid,0) / sum(doc_wordid2count.values())

def wf(doc_wordid2count, wordid):
    tfval = tf(doc_wordid2count, wordid)
    if tfval > 0.0:
        return 1.0 + log2(1.0+tfval)  #???
    return 0.0

#########################################################################

def idf(wordsmodel, wordid):  
    return log2( wordsmodel.N() / wordsmodel.df(wordid) )

def _pcalc_wfgf_(wordsmodel, doc_wordid2count, wordid):
    return  wf(doc_wordid2count, wordid) / wordsmodel.gf(wordid) 

def _pcalc_tfgf_(wordsmodel, doc_wordid2count, wordid):
    return  tf(doc_wordid2count, wordid) / wordsmodel.gf(wordid) 

def ent(wordsmodel, wordid):
    """Returns entropy precalculated in wordsmodel."""
    val = wordsmodel.wordid2entropy.get(wordid, 1.0)
    #logging.info("[ent] "+str(wordid)+" -> "+str(val))
    return val

def entropy(wordsmodel, wordid, pcalc = _pcalc_tfgf_):
    """Calculates entropy using only information about counts."""
    s = 0.0
    for doc_wordid2count in wordsmodel.docs_wordid2count:
        p = pcalc(wordsmodel, doc_wordid2count, wordid)
        if p>0.0:
            s = s + p*log2(p)
    return 1.0 + s / log2(wordsmodel.N())
     
#########################################################################     
     
class WordsModel:
    def __init__(self):
        self.wordid2count = {} #{wordid: number-of-ocurrences-in-corpora}
        self.wordid2nonzerodocs = {} #{wordid: number-of-docs-that-have-word}
        self.docs_wordid2count = [] #list of documents, where document is represented as {wordid: number-of-ocurrences-in-document}
        #self.docs_wordidpair2count = [] #list of documents, where document is represented as {(wordid1,wordid2): number-of-ocurrences-in-document}
        self.wordidpair2nonzerodocs = {} #{(wordid1,wordid2): number-of-docs-that-have-pair-of-words}
        
        self.wordid2entropy = {}
        self.numwords = 0
        
    def report(self):
        print self,"--------"
        print "wordid2count=",str(self.wordid2count)[:150] 
        print "wordid2nonzerodocs=",str(self.wordid2nonzerodocs)[:150]
        print "docs_wordid2count=",str(self.docs_wordid2count)[:150]
        print "wordid2entropy=",str(self.wordid2entropy)[:250]
        print "self.numwords=",str(self.numwords)
        print "-------------"
        
    def update(self, doc_wordid2count):
        doc_wordid2count_list = list( doc_wordid2count.iteritems() )
        
        self.docs_wordid2count.append(doc_wordid2count) #pojedyncze slowa
        
        #wordidpair2count = {} #pary slow
        #for wordid1,count1 in doc_wordid2count_list:
        #    for wordid2,count2 in doc_wordid2count.iteritems():
        #        wordidpair2count[(wordid1, wordid2)] = min(count1, count2)
        #self.docs_wordidpair2count.append(wordidpair2count)
        
        for i in xrange(0, len(doc_wordid2count_list)):
            wordid1 = doc_wordid2count_list[i][0]
            for j in xrange(i, len(doc_wordid2count_list)):
                wordid2 = doc_wordid2count_list[j][0]                
                self.wordidpair2nonzerodocs[(wordid1, wordid2)] = self.wordidpair2nonzerodocs.get((wordid1, wordid2),0)+1 
                self.wordidpair2nonzerodocs[(wordid2, wordid1)] = self.wordidpair2nonzerodocs.get((wordid2, wordid1),0)+1

        for wordid,count in doc_wordid2count_list: #slowa i dokumenty ze slowami w korpusie 
            self.wordid2count[wordid]       = self.wordid2count.get(wordid,0) + count
            self.wordid2nonzerodocs[wordid] = self.wordid2nonzerodocs.get(wordid,0) + 1
                                
            
    def finish_updates(self):
        logging.info("[WordsModel.finish_updates] calculating numwords")    
        self.numwords = sum(self.wordid2count.values())
        logging.info("[WordsModel.finish_updates] calculating entropies")
        for i, (wordid, count) in enumerate(self.wordid2count.iteritems()):
            if i%1000==0: logging.info("[WordsModel.finish_updates] entropies "+str(i)+"/"+str(len(self.wordid2count)))
            self.wordid2entropy[wordid] = entropy(self, wordid, pcalc = _pcalc_tfgf_)
            
    def N(self): #numdocs
        return len(self.docs_wordid2count)
    
    def df(self, wordid):
        return self.wordid2nonzerodocs.get(wordid, 0)
    
    def gf(self, wordid): #???
        return float(self.wordid2count.get(wordid, 0)) / self.numwords

#########################################################################


def _di_(dictionary):
    return dict((int(k),int(v)) for k,v in dictionary.iteritems()) 

def build_wordsmodel(fin, fout, src_field = "g0"):
    """Returns ({wordid:number-of-occurrences-in-whole-corpus}, {wordid:number-of-docs-that-contain-this-word}, numdocs)."""
    wordsmodel = WordsModel()        
    for i,record in enumerate(zbl_io.read_zbl_records(fin)):                            
        if i%500 == 0: logging.info("[build_wordsmodel] "+str(i)+" records processed")
        if src_field in record: 
            doc_wordid2count = _di_( zbl_io.unpack_dictionary_field(record[src_field]) )    
            wordsmodel.update(doc_wordid2count)
    wordsmodel.finish_updates()    
    return wordsmodel


def map_wordsmodel_overall_weighting(fin, fout, wordsmodel, src_field="g0", dst_field="g1",\
                                     weight = lambda wordsmodel,doc_wordid2count,wordid: tf(doc_wordid2count, wordid)*idf(wordsmodel, wordid) ):
    """Maps value of src_field using wordsmodel and weigting function. Results stores to dst_field."""
    counter = 0    
    for i,record in enumerate(zbl_io.read_zbl_records(fin)):                            
        if i%100 == 0: logging.info("[map_wordsmodel_overall_weighting] "+str(i)+" records processed."+str(counter)+"enriched.")
        if src_field in record:                
            doc_wordid2count    = _di_( zbl_io.unpack_dictionary_field(record[src_field]) )
            doc_wordid2weight   = [( wordid,weight(wordsmodel,doc_wordid2count,wordid) ) for wordid,count in doc_wordid2count.iteritems() ]
            record[dst_field]   = zbl_io.pack_listpairs_field( sorted( doc_wordid2weight ) )
            counter = counter + 1 
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
    return counter

def map_wordsmodel(fin, fout, wordsmodel, src_field="g0", dst_field="g1", localweigting=tf, globalweigting=idf):
    """Maps value of src_field using wordsmodel and local*global weigting functions. Results stores to dst_field."""
    weight = lambda wordsmodel,doc_wordid2count,wordid: localweigting(doc_wordid2count, wordid)*globalweigting(wordsmodel, wordid) 
    return map_wordsmodel_overall_weighting(fin, fout, wordsmodel, src_field, dst_field, weight)
