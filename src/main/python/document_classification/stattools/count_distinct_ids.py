'''
Created on May 4, 2012

@author: mlukasik
'''
#from __future__ import absolute_import
import sys
sys.path.append(r'../')
from data_io.zbl_io import read_zbl_records

def count_ids(fin):
    """
    Counts how many records there are with each fields list of given list of field lists
    """
    id_vals = {}
    au_vals = 0
    all = 0
    records = list(read_zbl_records(fin))
    for ind, r in enumerate(records):
        all+=1
        au_vals += 'au' in r
        
        if r['an'] not in id_vals:
            id_vals[r['an']] = [ind]
        else:
            pass
            '''
            print "-------------------------------"
            print "Powtorzenie id an!", r['an']
            id_vals[r['an']] += [ind]
            for i in id_vals[r['an']]:
                print records[i]
            print "-------------------------------"
            '''
    return all, len(id_vals), au_vals

if __name__ == "__main__":
    try:
        fin = open(sys.argv[1], 'r')
    except:
        fin = sys.stdin
        #print "Specify file name as argument"
        #sys.exit(1)
    print "all, len(id_vals):", count_ids(fin)