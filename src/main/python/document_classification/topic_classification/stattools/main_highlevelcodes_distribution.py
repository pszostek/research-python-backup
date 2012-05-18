'''
Created on Nov 17, 2011

@author: mlukasik

Display high levelcodes distribution
'''
from collections import defaultdict
import sys
sys.path.append(r'../') 
from zbl2py import record_read

def print_dict_content(d):
    for k, v in sorted(d.iteritems(), key=lambda x: x[1], reverse=True):
        print "|", k, "||", v
        print "|-"
    
def print_highlevelcodes_distribution(records):
    lowlv = defaultdict(lambda: 0)
    midlv = defaultdict(lambda: 0)
    highlv = defaultdict(lambda: 0)
    for rec in records:
        for c in rec['categories']:
            lowlv[c]+=1
            midlv[c[:3]]+=1
            highlv[c[:2]]+=1
    
    print "high level:"
    print_dict_content(highlv)
    print "mid level:"
    print_dict_content(midlv)
    print "low level:"
    print_dict_content(lowlv)


if __name__=="__main__":
    records = record_read.read_list_records(sys.argv[1])
    print_highlevelcodes_distribution(records)