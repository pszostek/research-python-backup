
import sys
import itertools
from itertools import izip

if __name__=="__main__":
    print "The program fills in empty lines in main file using lines from auxiliary file."
    
    try:
        main_file = sys.argv[1]
    except:
        print "First argument expected: main file with labels"
        sys.exit(-1)
        
    try:
        aux_file = sys.argv[2]
    except:
        print "Second argument expected: auxiliary file with labels"
        sys.exit(-1)
        
    try:
        out_file = sys.argv[3]
    except:
        print "Third argument expected: output file"
        sys.exit(-1)
        
    fmain = open(main_file)
    faux = open(aux_file)
    fout = open(out_file, "w")
        
    replaced = 0
    for l1,l2 in izip(fmain.xreadlines(), faux.xreadlines()):
        l1 = l1.strip()
        l2 = l2.strip()
        if len(l1) <= 0:
            l1 = l2 #"1,2,3,4"
            replaced = replaced + 1
        fout.write(l1+"\n")
        
    print replaced," lines replaced."
    
    #nl = [len(line.strip().split(',')) for line in open(main_file).xreadlines()]
    #print sum(nl)/float(len(nl))
        