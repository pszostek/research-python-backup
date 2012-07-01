

import sys,os
from data_maketable import *


sys.path.append(r'../')
sys.path.append(r'../../')
sys.path.append(r'../../../')

from tools.stats import *

def extract_prefix(colvalue):
    i = -1
    for i in xrange(len(colvalue)-1, 0, -1):
        if not str.isdigit(colvalue[i]): break
    return colvalue[:i+1]


def extract_agg_table(lines, skip_header=True, separator="\t"):
    agg_table = {}
    for lineno, line in enumerate(lines):
        line = line.strip()
        if line == "": continue
        if skip_header and lineno==0: 
            print "[extract_agg_table] Skipping header:",line
            continue
        cols    = line.split(separator)

        agg_key     = extract_prefix(cols[agg_col])
        keys        = reduce(lambda l1,l2: l1+separator+l2, (cols[colno] for colno in row_label_cols) )        
        full_key    = (keys, agg_key)

        table_row   = agg_table.get(full_key, {} )        
        for colno in val_cols:
            try:
                table_row[colno] = table_row.get(colno, []) + [ float(cols[colno].replace(",", ".")) ]
            except:
                pass            
        agg_table[full_key] = table_row            
    return agg_table

def _safe_aggregator_(col_vals, aggregator):
    try:
        return str(aggregator(col_vals))
    except:
        return "?"
    

def calc_aggregation(agg_table, separator="\t", aggregator = max):
    table = {}
    for (rowkey1,rowkey2), col_data in agg_table.iteritems():        
        #print "------->", col_data["agg"]
        print (rowkey1,rowkey2), max(col_data["agg"])
    return table


if __name__=="__main__":
    fin = sys.stdin
    fout = sys.stdout
    sys.stdout = sys.stderr
    print "Reads table from file table (every line is in format: col1[tab]col2[tab]...[tab]colN) and prints out table with some columns aggregated." 

    try:
        row_label_cols = list(int(c) for c in sys.argv[1].split(',') )
        print "Numbers of columns to be interpreted as row labels:",row_label_cols
    except:        
        print "Numbers of columns to be interpreted as row labels (apart from aggrgation column) expected as an argument of the program."
        sys.exit(-1)      

    try:
        agg_col = int(sys.argv[2])
        print "The column to be aggregated:", agg_col
    except:
        print "The column to be aggregated expected as an argument of the program."
        sys.exit(-1)  

    try:
        val_cols = list(int(c) for c in sys.argv[3].split(',') )
        print "Numbers of columns to be interpreted as values:",val_cols
    except:        
        print "Numbers of columns to be interpreted as values expected as an argument of the program."
        sys.exit(-1)        

    try:
        aggregation_name = sys.argv[4]
        if aggregation_name == "max": 
            aggregator = max
        elif aggregation_name == "min": 
            aggregator = min
        elif  aggregation_name == "avg": 
            aggregator = avg
        print "Aggregator =",aggregator
    except:
        print "Aggregation name (max/min/avg) expected as an argument."
        sys.exit(-1)

    skip_header = 1
    try:
        skip_header = int(sys.argv[5])
    except:
        pass
    skip_header = skip_header!=0
    print "Skip_header = ", skip_header 
    
    #################################################################################################

    agg_table = extract_agg_table(fin.xreadlines(), skip_header, SEPARATOR)
    table = calc_aggregation(agg_table, SEPARATOR, aggregator)
    
    print table
    print_table(fout, table, val_cols)
        

