'''
Created on Dec 01, 2011

@author: mlukasik

Counts how often fields occur amongst the records.
'''
import sys
from count_fields import count_feature_subset_statistics

if __name__ == '__main__':
    fname = sys.argv[1]
    fields = sys.argv[2:]
    print "fname:", fname
    print "fields:", fields
    count_feature_subset_statistics(fname, fields)
