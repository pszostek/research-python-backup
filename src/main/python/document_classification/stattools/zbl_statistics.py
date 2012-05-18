'''
Created on Dec 17, 2011

@author: mlukasik

'''
from __future__ import division 
import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import gen_lmc
from tools import msc_processing
from tools.msc_processing import count_msc_occurences

def contains2of_same_prefix(lmc, num):
    """
    Checks if in lmc there are 2 elements of the same prefix of length num.
    
    """
    lmc_sorted = sorted(lmc)
    prev = lmc_sorted[0][:num]
    for curr in lmc[1:]:
        if curr[:num]==prev:
            return True
        
        prev = curr[:num]
    return False

def contains2of_diff_prefix(lmc, num):
    """
    Checks if in lmc there are 2 elements of the different prefixes of length num.
    
    """
    pattern = lmc[0][:num]
    for compared in lmc[1:]:
        if compared[:num]<>pattern:
            return True
    return False

def count_label_statistics(fname, fields):
    """
    Counts the following statistics and prints them. 
    D is the dataset filtered by the condition to contain all of the fields
    L is number of distinct labels in D.
    
    -Label cardinality:  the average number of labels of the examples in D
    -Label density: the average number of labels of the examples in D divided by |L|
    -Bolo11: the percentage of documents that contain at least 2 labels of the same 2 code prefix 
    -Bolo12: the percentage of documents that contain at least 2 labels of the same 3 code prefix 
    -Bolo21: the percentage of documents that contain at least 2 labels of different 2 code prefix 
    -Bolo22: the percentage of documents that contain at least 2 labels of different 3 code prefix 

    """
    
    
    all = 0
    labels = set()
    lc = 0
    ld = 0
    bolo11 = 0
    bolo12 = 0
    bolo21 = 0
    bolo22 = 0
    #count statistics
    for lmc in gen_lmc(fname, fields):
        all+=1
        for mc in lmc:
            labels.add(mc)
        lc += len(lmc)
        ld += len(lmc)
        if contains2of_same_prefix(lmc, 2):
            bolo11 += 1
        if contains2of_same_prefix(lmc, 3):
            bolo12 += 1
        if contains2of_diff_prefix(lmc, 2):
            bolo21 += 1
        if contains2of_diff_prefix(lmc, 3):
            bolo22 += 1
        
    #print statistics
    print "lc:", lc/all
    print "ld:", ld/(all*len(labels))
    
    print "bolo11 contain at least 2 of same 2 code prefix:", bolo11/all
    print "bolo12 contain at least 2 of same 3 code prefix:", bolo12/all
    print "bolo21 contain at least 2 of diff 2 code prefix:", bolo21/all
    print "bolo22 contain at least 2 of diff 3 code prefix:", bolo22/all
    
    #print "First 100 labels:", list(labels)[:100]
    
    

if __name__ == '__main__':
    fname = sys.argv[1]
    fields = sys.argv[2:]
    print "fname:", fname
    print "fields:", fields
    count_label_statistics(fname, fields)