"""Functions useful for different processings of vectors and dictionaries of MSC codes.

@author: tkusm
@author: mlukasik
"""
import sys
sys.path.append(r'../')
from data_io import zbl_io
import re
import logging
from randomized import sample_cartesian_product
from stats import *

MSC_LEAF_PATTERN = "\d\d.\d\d"
MSC_ORDINARY_LEAF_PATTERN = "\d\d[A-Za-z]\d\d"
MSC_SPECIAL_LEAF_PATTERN = "\d\d-\d\d"

MSC_SECOND_LEVEL = '\d\d.[x-xX-X][x-xX-X]'
MSC_ORDINARY_SECOND_LEVEL = '\d\d[A-Za-z][x-xX-X][x-xX-X]'
MSC_SPECIAL_SECOND_LEVEL = '\d\d-[x-xX-X][x-xX-X]'


MSC_LEAF_PATTERN_RE = re.compile(MSC_LEAF_PATTERN)
MSC_ORDINARY_LEAF_PATTERN_RE = re.compile(MSC_ORDINARY_LEAF_PATTERN)
MSC_SPECIAL_LEAF_PATTERN_RE = re.compile(MSC_SPECIAL_LEAF_PATTERN)

MSC_SECOND_LEVEL_RE = re.compile(MSC_SECOND_LEVEL)
MSC_ORDINARY_SECOND_LEVEL_RE = re.compile(MSC_ORDINARY_SECOND_LEVEL)
MSC_SPECIAL_SECOND_LEVEL_RE = re.compile(MSC_SPECIAL_SECOND_LEVEL)

                
def group_zbl_by_msc(zbl_generator, \
                     msc_primary_predicate = lambda mscprim: MSC_ORDINARY_LEAF_PATTERN_RE.match(mscprim), \
                     zbl_extract = lambda zbl: zbl[zbl_io.ZBL_ID_FIELD]):
    """Returns dictionary{msc-primary-code: list-of-extracted-by-zbl_extract(zbl)-values}.
    
    When msc_primary_predicate(msc_primary_code)==False record will be skipped.    
    """
    msc2zbllist = {}
    for zbl in zbl_generator:
        msc_primary_code = zbl_io.unpack_multivalue_field(zbl['mc'])[0]
        if not msc_primary_predicate(msc_primary_code): continue
        zbllist = msc2zbllist.get(msc_primary_code, [])
        zbllist.append( zbl_extract(zbl) )
        msc2zbllist[msc_primary_code] = zbllist
    return msc2zbllist


def count_msc_occurences(file, records_filter = lambda x: True, field_name = "mc"):
    """Counts number of occurrences of MSC codes in ZBL file.
        
    Returns dictionary{code_name: count}"""
    counts = {}
    for record in zbl_io.read_zbl_records(file):
        if not records_filter(record) or not record.has_key(field_name):
            continue 
        codes = zbl_io.unpack_multivalue_field(record[field_name])
        for code in codes:
            counts[code] = counts.get(code, 0) + 1    
    return counts



def count_unique_prefixes(labels, prefix_len = 3):
    """In list of strings counts unique prefixes of given length.
    
    Sample use:
    >>> count_unique_prefixes(['abcd', 'babe', 'abce', 'babi', 'xxxz'], 2) == { 'xx': 1, 'ab': 2, 'ba': 2}
    True
    """
    count = {}
    for l in range(0, len(labels)):
        prefix = labels[l][0:prefix_len]
        try:
            count[prefix] = count[prefix] + 1
        except:
            count[prefix] = 1
    return count

def find_ixs_of_val(vec, val):
    """Finds indexes of elements equal to value val in vector vec.

    Sample use:
    >>> find_ixs_of_val([1,2,3,1,2,3,1,2,3,3], 3)
    [2, 5, 8, 9]
    """
    return [ix for ix in range(0, len(vec)) if vec[ix] == val] #selected indexes

def get_prefixes(labels, prefix_len):
    """Returns set of prefixes of labels where length = prefix_len.

    Sample use:
    >>> get_prefixes(['abcd', 'babe', 'abce', 'babi', 'xxxz'], 3) == set(['abc', 'bab', 'xxx'])
    True
    """
    return set(label[0:prefix_len] for label in labels)

def get_prefix2codes(codes, prefix_len):
    """Returns dictionary{prefix-of-prefix_len: list-of-codes-with-this-prefix}."""
    prefix2codes = {}
    for code in codes:
        prefix = code[:prefix_len]
        prefix2codes[prefix] = prefix2codes.get(prefix,[]) + [code]
    return prefix2codes 

def number_of_child_codes_stats(msccodes, prefix_len = 5):
    """Returns (average,standard-deviation,min,max) number of codes with common prefix of length = prefix_len."""
    counts = list( len(codes) for prefix,codes in get_prefix2codes(msccodes, prefix_len).iteritems() )
    return avg(counts), std(counts), min(counts), max(counts)

def number_of_child_docs_stats(msc2zblidlist, prefix_len = 5):
    """Returns (average,standard-deviation,min,max) number of documents belonging to common code."""    
    msc2count = dict( (msc,len(zbliidlist)) for msc, zbliidlist in msc2zblidlist.iteritems() )
    prefix2count = {}
    for msccode,count in msc2count.iteritems():
        prefix = msccode[:prefix_len]
        prefix2count[prefix] = prefix2count.get(prefix, 0) + count
    counts = prefix2count.values()
    return avg(counts), std(counts), min(counts), max(counts)         
        

def get_elements_of_ixs(vec, ixs):
    """Retrieves elements of indexes ixs from list (vector) vec.
    
    Sample use:
    >>> get_elements_of_ixs(["a","b","c","d","e"], [0, 2, 4])
    ['a', 'c', 'e']
    """
    return [vec[ix] for ix in ixs]

def count_msc_occurences_codegenerator(code_generator):
    """
    Counts number of occurrences of MSC codes in code_generator.
        
    Returns dictionary{code_name: count}
    
    TESTED.
    """
    counts = {}
    for codes in code_generator():
        for code in codes:
            counts[code] = counts.get(code, 0) + 1 
    return counts

def get_labels_min_occurence(code_generator, min_occurences):
    """    
    Returns list of labels, each of which occurs at least min_occurences times.
    Returns number of elements in of such labels as well.
    
    TESTED.
    """
    counts = count_msc_occurences_codegenerator(code_generator)
    filtered_pairs = filter(lambda x: x[1]>=min_occurences, counts.iteritems())
    #print filtered_pairs
    return map(lambda x: x[0], filtered_pairs)

def get_labels_counts(code_generator, min_occurences):
    """    
    Returns list of labels, each of which occur at least min_occurences times.
    Returns number of elements in of such labels as well.
    
    TESTED.
    """
    counts = count_msc_occurences_codegenerator(code_generator)
    return filter(lambda x: x[1]>=min_occurences, counts.iteritems())

def get_prefixes_list(labels, prefix_len):
    """Returns list of prefixes of labels where length = prefix_len.

    Sample use:
    >>> get_prefixes(['abcd', 'babe', 'abce', 'babi', 'xxxz'], 3) == ['abc', 'bab', 'abc', 'bab', 'xxx']
    True
    """
    return [label[0:prefix_len] for label in labels]

def get_labelperdocuments_counts(gen_lmc):
    """Returns a dictionary with counts labelperdocuments <-> counts.

    """
    counts = {}
    for codes in gen_lmc():
        counts[len(codes)] = counts.get(len(codes), 0) + 1 
    return counts

def zblrecord_deep_copy(record, fields2constructors = {'DEFAULT':str}):
    """Return a deep copy of record in zbl format (which is a dictionary).
    
    {Created on 13.02.12 for copying records in ml_hierarchical so that classifiers with prefixed
    msc codes can be trained.}
    
    """
    record_new = dict()
    for key, val in record.iteritems():
        if key in fields2constructors:
            record_new[key] = fields2constructors[key](val)
        else:
            record_new[key] = fields2constructors['DEFAULT'](val)
    return record_new




def mscmsc2sampleids_generator(msclist, msc2zblidlist, calculate_sample_size = 1000000):
    """Generates pairs ( (msc1,msc2), list-of-pairs-of-documents-ids ).
    
    msclist - list of msc-codes
    msc2zblidlist - dictionary{msc-code: list of documents-ids.}
    calculate_sample_size(number-of-possible-pairs-of-documents) returns how many pairs should be calculated.
    If (msc1,msc2) occurs than (msc2,msc1) won't occur.
    """
    for msc_i in xrange(len(msclist)): #wszystkie pary kodow msc
        for msc_j in xrange(msc_i+1, len(msclist)):
            msc1,msc2 = msclist[msc_i],msclist[msc_j]
            zblidlist1,zblidlist2 = msc2zblidlist[msc1],msc2zblidlist[msc2]             
            #sampleids = randomized.sample_cartesian_product(zblidlist1, zblidlist2, calculate_sample_size)
            sampleids = sample_cartesian_product(zblidlist1, zblidlist2, calculate_sample_size)
            logging.debug("[mscmsc2sampleids_generator]["+str(msc_i*len(msclist)+msc_j)+"/"+str(len(msclist)*len(msclist)/2)+"]"+str((msc1,msc2))+" -> "+str(sampleids))          
            yield (msc1,msc2), sampleids



###################################################################################################
###################################################################################################
###################################################################################################
###################################################################################################



def _u_(msc2zblcodes, msc_codes, zbl_code, msc_predicate):
    for msc_code in msc_codes:
        if msc_predicate(msc_code):
            msc2zblcodes[msc_code] = msc2zblcodes.get(msc_code, []) + [zbl_code]
            
def _keep_msc_(msc2sthing, keep_msccodes):
    return dict((msc,sthing) for msc,sthing in msc2sthing.iteritems() if msc in keep_msccodes)
    #return dict((msc,msc2sthing[msc]) for msc in keep_msccodes)            
            
def _msc2zblidlist_to_msc2count_(msc2zblidlist):
    return dict( (msc,len(zbllist)) for msc,zbllist in msc2zblidlist.iteritems() )            

def msc2count_filter(msc2count, min_count):
    """Returns list of msc codes with count>=min_count."""
    return [msc for msc,count in msc2count.iteritems() if count>=min_count] 

###################################################################################################        
###################################################################################################
class MscModel:
    def __init__(self, zbl_generator, \
                 msc_predicate = lambda msc: MSC_ORDINARY_LEAF_PATTERN_RE.match(msc)):
        self.msc2zblidlist = {}
        self.mscprim2zblidlist = {}
        self.mscsec2zblidlist = {}
        self.msc2count = {}
        self.mscprim2count = {}
        self.mscsec2count = {}
        self.update(zbl_generator, msc_predicate) 
        
    def update(self, zbl_generator, \
               msc_predicate = lambda msc: MSC_ORDINARY_LEAF_PATTERN_RE.match(msc)):
        logging.info("[MscModel.update] building msc2lists")
        for zbl in zbl_generator:############
            msc_codes = zbl_io.unpack_multivalue_field(zbl['mc'])
            zbl_id = zbl[zbl_io.ZBL_ID_FIELD]
            _u_(self.msc2zblidlist,      msc_codes, zbl_id, msc_predicate)
            _u_(self.mscprim2zblidlist,  msc_codes[0:1], zbl_id, msc_predicate)
            _u_(self.mscsec2zblidlist,   msc_codes[1:], zbl_id, msc_predicate)
        #####################################
        logging.info("[MscModel.update] calculating msc2counts")
        self.msc2count      = _msc2zblidlist_to_msc2count_(self.msc2zblidlist)
        self.mscprim2count  = _msc2zblidlist_to_msc2count_(self.mscprim2zblidlist)
        self.mscsec2count   = _msc2zblidlist_to_msc2count_(self.mscsec2zblidlist)
        
    def report(self):
        print "[MscModel] report"
        print " len(self.msc2zblidlist)=", len(self.msc2zblidlist),"->",str(list(self.msc2zblidlist.iteritems()))[:75]
        print " len(self.mscprim2zblidlist)=", len(self.mscprim2zblidlist),"->",str(list(self.mscprim2zblidlist.iteritems()))[:75]
        print " len(self.mscsec2zblidlist)=", len(self.mscsec2zblidlist),"->",str(list(self.mscsec2zblidlist.iteritems()))[:75]
        print " len(self.msc2count)=", len(self.msc2count),"->",str(list(self.msc2count.iteritems()))[:75]
        print " len(self.mscprim2count)=", len(self.mscprim2count),"->",str(list(self.mscprim2count.iteritems()))[:75]
        print " len(self.mscsec2count)=", len(self.mscsec2count),"->",str(list(self.mscsec2count.iteritems()))[:75]        
        print " self.msc2count prefix3 avg,std,min,max child codes =", number_of_child_codes_stats(self.msc2count.keys(), prefix_len = 3)
        print " self.msc2count prefix2 avg,std,min,max child codes =", number_of_child_codes_stats(self.msc2count.keys(), prefix_len = 2)
        print " self.self.msc2zblidlist prefix5 avg,std,min,max child docs =", number_of_child_docs_stats(self.msc2zblidlist, prefix_len = 5)
        print " self.self.msc2zblidlist prefix3 avg,std,min,max child docs =", number_of_child_docs_stats(self.msc2zblidlist, prefix_len = 3)
        print " self.self.msc2zblidlist prefix2 avg,std,min,max child docs =", number_of_child_docs_stats(self.msc2zblidlist, prefix_len = 2)
        print " self.self.mscprim2zblidlist prefix5 avg,std,min,max child docs =", number_of_child_docs_stats(self.mscprim2zblidlist, prefix_len = 5)
        print " self.self.mscprim2zblidlist prefix3 avg,std,min,max child docs =", number_of_child_docs_stats(self.mscprim2zblidlist, prefix_len = 3)
        print " self.self.mscprim2zblidlist prefix2 avg,std,min,max child docs =", number_of_child_docs_stats(self.mscprim2zblidlist, prefix_len = 2)
        
    def keep(self, keep_msccodes):
        #keep_msccodes = set(keep_msccodes)
        self.msc2count      = _keep_msc_(self.msc2count, keep_msccodes)
        self.mscprim2count  = _keep_msc_(self.mscprim2count, keep_msccodes)
        self.mscsec2count   = _keep_msc_(self.mscsec2count, keep_msccodes)
        self.msc2zblidlist      = _keep_msc_(self.msc2zblidlist, keep_msccodes)
        self.mscprim2zblidlist  = _keep_msc_(self.mscprim2zblidlist, keep_msccodes)
        self.mscsec2zblidlist   = _keep_msc_(self.mscsec2zblidlist, keep_msccodes)
        
    def allcodes(self):
        """Returns set of all known codes."""
        return self.msc2count.keys()
        #return set(self.msc2count).union(set(self.mscprim2count)).union(set(self.mscsec2count))
        
    def N(self):
        return len(self.allcodes())
       
    def keep_msc_mincount(self, min_count, minprim_count, minsec_count):        
        logging.info("[keep_msc_mincount] min_count="+str(min_count)+", minprim_count="+str(minprim_count)+", minsec_count="+str(minsec_count))
        all = set(self.allcodes())
        if min_count<=0:
            m1 = all
        else:
            m1 = set( msc2count_filter(self.msc2count, min_count) )
        if minprim_count<=0:
            m2 = all
        else:            
            m2 = set( msc2count_filter(self.mscprim2count, minprim_count) )
        if minsec_count<=0:
            m3 = all
        else:
            m3 = set( msc2count_filter(self.mscsec2count, minsec_count) ) 
        keep_msccodes = m1.intersection(m2).intersection(m3)
        self.keep(keep_msccodes)
###################################################################################################        
###################################################################################################







if __name__ == "__main__":
    import doctest
    doctest.testmod()
