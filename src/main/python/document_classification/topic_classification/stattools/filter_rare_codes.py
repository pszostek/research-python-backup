'''
Created on Nov 9, 2011

@author: mlukasik
'''
from collections import defaultdict

def filter_out_rare_codes_records(records, thresh_categs_count, category_field_name='categories'):
    """Filter out codes which counts are smaller then thresh_categs_count; 
    Afterwards, filter out records that have no codes at all.
    Assumes, that in records there is a key named"""
    #count each category:
    categs = defaultdict(lambda: 0)
    for rec in records:
        for c in rec[category_field_name]:
            categs[c]+=1
    print "len of categs before filtering rare ones:", len(categs)
    #delete rare ones:
    to_del = []
    for c, v in categs.iteritems():
        if v<thresh_categs_count:
            to_del.append(c)
    for c in to_del:
        categs.pop(c)
    print "len of categs after filtering rare ones:", len(categs)
    #delete rare categories from records:
    r_to_del = []    
    for rec in records:
        to_del = []
        for c in rec[category_field_name]:
            if c not in categs:
                to_del.append(c)
        for c in to_del:
            rec[category_field_name].remove(c)
        if len(rec[category_field_name])==0:
            r_to_del.append(rec)
    #delete rare records:
    print "len of records before filtering those without codes:", len(records)
    for rec in r_to_del:
        records.remove(rec)
    print "len of records after filtering those without codes:", len(records)
    return records

if __name__=="__main__":
    import sys
    sys.path.append(r'../') 
    from zbl2py import record_read, record_store
    
    records = filter_out_rare_codes_records(record_read.read_list_records(sys.argv[1]), int(sys.argv[3]))
    record_store.store_py_records(records, sys.argv[2])