

import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io

if __name__ == "__main__":       
    print "The program takes two JRS label'-files and merges into single file."

    try:
        labels1_path = sys.argv[1]
    except:
        print "Argument expected: path to a labels' file."
        sys.exit(-1)
    try:
        labels2_path = sys.argv[2]
    except:
        print "Argument expected: path to a second labels' file."
        sys.exit(-1)        
    try:
        out_path = sys.argv[3]
    except:
        print "Argument expected: output labels' file."
        sys.exit(-1)      
                        
    print "Loading labels' 1 file:",  labels1_path
    labels1 = jrs_io.load_labels(open(labels1_path))
    
    try:
        print "Loading labels' 2 file:",  labels2_path
        labels2 = jrs_io.load_labels(open(labels2_path))
    except:
        print "Failed loading file", labels2_path
        print "Using empty file"
        labels2 = [[] for i in xrange(len(labels1))]
    
    labels12 = []
    for i in xrange(len(labels1)):
         labels12.append( sorted(set(labels1[i]+labels2[i])) )
         
         
    print "Writing to 1+2 file:", out_path
    jrs_io.store_labels(open(out_path,"w"), labels12)

     
         
        
        