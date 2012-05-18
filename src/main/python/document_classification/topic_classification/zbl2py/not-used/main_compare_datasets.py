'''
Created on Dec 1, 2011

@author: mlukasik

Find out the differences between 2 data sets
'''
from record_store import store_py_records, store_txt_records
from zbl_io import load_zbl_file, read_zbl_records
import sys
from collections import defaultdict

fname1 = sys.argv[1]
fname2 = sys.argv[2]
print "loading records1"

records1 = defaultdict(lambda: {})
records1_cnt = 0
for rec1 in read_zbl_records(open(fname1, 'r')):
    try:
        records1[rec1['an']][rec1['ti']] = rec1
        records1_cnt+=1
    except:
        pass
    
print "loaded records1", len(records1), "all of them:", records1_cnt

print "going through records2"
not_in_rec1 = 0
records2_len = 0
for rec2 in read_zbl_records(open(fname2, 'r')):
    if rec2['an'] not in records1 or rec2['ti'] not in records1[rec2['an']]:
        #print "record not in records1!"
        print rec2
        not_in_rec1+=1
    records2_len+=1
    
print "not_in_rec1:", not_in_rec1
print "all of records2:", records2_len