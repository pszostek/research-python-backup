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

def find_fields(fname):
    """
    Counts how many records there are with given fields
    """
    
    all = 0
    fields = set()
    for r in read_zbl_records( open(fname, 'r')):
        all+=1
        for field in r.iterkeys():
            fields.add(field)
    return all, fields

if __name__ == '__main__':
    fname = sys.argv[1]
    print "fname:", fname
    all, fields = find_fields(fname)
    
    print "all:", all
    print "fields:", fields
