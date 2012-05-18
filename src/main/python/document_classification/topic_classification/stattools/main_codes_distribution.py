'''
Created on Nov 9, 2011

@author: mlukasik

Display distributions of codes and documents
'''
from collections import defaultdict
import sys
sys.path.append(r'../') 
from zbl2py import record_read

def print_codes_distribution(records):
    categs = defaultdict(lambda: 0)
    for rec in records:
        for c in rec['categories']:
            categs[c]+=1
    #print sorted categories:
    
    categs_occurences = defaultdict(lambda: 0)
    for _, v in categs.iteritems():
        categs_occurences[v]+=1
    
    msc_codes = sorted(list(categs_occurences.iteritems()), key=lambda x:x[1])
    for cd in msc_codes:
        print "|", cd[0], "||", cd[1]
        print "|-"

def print_docs_distribution(records):
    docs = defaultdict(lambda: 0)
    for rec in records:
        docs[len(rec['categories'])]+=1
    #print sorted categories:
    doc_distr = sorted(list(docs.iteritems()), key=lambda x:x[1])
    for cd in doc_distr:
        print "|", cd[0], "||", cd[1]
        print "|-"
    
    
if __name__=="__main__":
    records = record_read.read_list_records(sys.argv[1])
    print_codes_distribution(records)
    print_docs_distribution(records)