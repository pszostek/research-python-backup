"""
Losuje z pliku z rekordami ZBL k losowych rekordow i zapisuje do drugiego pliku.

TODO: english comments.
"""

import sys
import os
import io
import random

if __name__ == "__main__":
    
    try:
        zblpath = sys.argv[1]
    except:
        print "First argument expected: source-file"        
        sys.exit(-1)
    try:
        outpath = sys.argv[2]
    except:
        print "Second argument expected: output-tile"        
        sys.exit(-1)     
    try:
        k = int(sys.argv[3])
    except:
        print "Third argument expected: sample-size (number)"        
        sys.exit(-1)     
    
    #count records
    numrecords  = sum( 1 for record in io.read_zbl_records(open(zblpath)) ) 

    #select indexes:
    ixs         = set()
    while len(ixs) < k:
        ixs.add( random.randrange(0, numrecords, 1) )

    #select records:
    selected    = []
    ix          = 0
    for record in io.read_zbl_records(open(zblpath)):
        if ixs.issuperset(set([ix])):
            selected.append(record)
        ix = ix + 1

    #write output
    io.write_zbl_records(open(outpath, "w"), selected)    


