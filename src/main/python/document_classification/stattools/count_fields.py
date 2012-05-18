'''
Created on Dec 7, 2011

@author: mlukasik

Functions for calculating the statistics on how often which tags occur in the zbl database.
'''
from __future__ import absolute_import
import os, sys
lib_path = os.path.abspath(os.path.sep.join(['..', '..', 'document_classification']))
sys.path.append(lib_path)
from tools import subsets
from data_io.zbl_io import read_zbl_records

def count_records_with_fields(fname, fields):
    """
    Counts how many records there are with given fields
    """
    
    all = 0
    cnt = 0
    for r in read_zbl_records( open(fname, 'r')):
        all+=1
        if fields:
            #check if this fields occur
            if reduce(lambda x, y: x and y, map(lambda f: f in r and r[f].strip()<>'null', fields)):
                cnt+=1
    return all, cnt

def count_records_with_various_fields(fname, lfields):
    """
    Counts how many records there are with each fields list of given list of field lists
    """
    
    all = 0
    counts = len(lfields)*[0]
    for r in read_zbl_records( open(fname, 'r')):
        all+=1
        for i, fields in enumerate(lfields):
            #check if this fields occur
            if reduce(lambda x, y: x and y, map(lambda f: f in r and r[f].strip()<>'null', fields)):
                counts[i] += 1
    return all, counts

def count_feature_subset_statistics(fname, fields):
    """
    Main function, which prints the statistics of occurence of fields in records from fname
    """
    
    print "findsubsets(fields,len(fields)):", subsets.findsubsets(fields,len(fields))
    lfields = sorted(map(lambda x: sorted(x), subsets.findallsubsets(fields)), key=lambda x: (100*len(x),x))
    print "lfields:"
    for f in lfields:
        print f
    all, counts = count_records_with_various_fields(fname, lfields)
    
    print "All elements:", all
    for i, fields in enumerate(lfields):
        print fields, ":", counts[i]