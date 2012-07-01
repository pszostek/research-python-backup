

import sys,os
from data_maketable import *

def split(colvalue):
    i = -1
    for i in xrange(len(colvalue)-1, 0, -1):
        if not str.isdigit(colvalue[i]): break
    return colvalue[:i+1], colvalue[i+1:]

if __name__=="__main__":
    fin = sys.stdin
    fout = sys.stdout
    sys.stdout = sys.stderr
    print "Reads table from input (every line is in format: col1[tab]col2[tab]...[tab]colN) and prints out table with column split." 

    try:
        split_col = int(sys.argv[1])
        print "The column to be split:", split_col
    except:
        print "The column to be split expected as an argument of the program."
        sys.exit(-1)  
    
    lines = fin.xreadlines()
    for line in lines:
        line = line.strip()
        if line == "": continue
        cols = line.split(SEPARATOR)
        prefix,suffix = split(cols[split_col])
        cols[split_col] = prefix
        cols.append(suffix)

        cols_data = reduce(lambda c1,c2: c1+SEPARATOR+c2,  (str(c) for c in cols) )
        fout.write(cols_data+"\n")

    
