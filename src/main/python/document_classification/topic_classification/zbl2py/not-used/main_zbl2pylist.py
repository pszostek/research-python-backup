'''
Created on Nov 3, 2011

@author: mlukasik

TODO: pomyslec, jak picklowac po kolei a nie wszystko na raz: to nie jest efektywne.
'''
#from collections import defaultdict
from zbl_line_splitter import ZblLineSplitter
from record_convert import filer_record, process_record
from record_store import store_py_records, store_txt_records
import sys
sys.path.append(r'../') 
from stattools import filter_rare_codes

def read_zbl_records(iname, thresh_categs_count=0):
    """Read records, convert them to a list of dictionaries and pickle it"""
    records = []
    cnt_all=0
    with open(iname) as f:
        rec = {}#defaultdict(lambda: None)
        for l in f:
            (l1, l2) = ZblLineSplitter.split_line(l)
            rec[l1]=l2
            if l1=='ti':#it is known to be the last record
                #print rec
                cnt_all+=1
                if filer_record(rec):
                    new_rec = process_record(rec)
                    records.append(new_rec)
                rec = {}
    print "Records filtered:", len(records)
    print "When all records:", cnt_all
    if thresh_categs_count>0:
        filter_rare_codes.filter_out_rare_codes_records(records, thresh_categs_count)
    
    print "After filtering the rare codes, number of records:", len(records)
    return records
    
if __name__ == '__main__':
    print "reading and processing"
    records = read_zbl_records(sys.argv[1], int(sys.argv[4]))
    store_py_records(records, sys.argv[2])
    store_txt_records(records, sys.argv[3])