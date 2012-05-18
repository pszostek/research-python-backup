
import sys
import itertools
from itertools import izip

sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io

if __name__=="__main__":
    print "The program replaces occurrences of some (those from aux file) labels in main file using occurrences from auxiliary file."
    
    try:
        main_file = sys.argv[1]
    except:
        print "First argument expected: main file with labels"
        sys.exit(-1)
        
    try:
        aux_file = sys.argv[2]
    except:
        print "Second argument expected: weka-csv (inst#,actual,predicted,error,prediction) (with header) file with labels"
        sys.exit(-1)
        
    try:
        out_path = sys.argv[3]
    except:
        print "Third argument expected: output file"
        sys.exit(-1)
                
    try:
        label_no = int(sys.argv[4])
    except:
        print "Argument expected: label to be overwritten no."
        sys.exit(-1)                

    print "Loading labels' 1 file:",  main_file
    labels1 = jrs_io.load_labels(open(main_file))
    print "",len(labels1),"rows loaded"
    
    print "Loading labels' (weka-csv) 2 file:",  aux_file
    #inst#,actual,predicted,error,prediction
    lines = open(aux_file).readlines()
    labels2bool = list( line.split(",")[2].find("present")>=0 for line in lines[1:] if len(line.strip())>0 )
    print "",len(labels2bool),"rows loaded"
    #print labels2bool
        
    removed = 0
    added = 0
    for i in xrange(len(labels1)):
        if labels2bool[i]:
            if not label_no in labels1[i]:
                print "adding label no",label_no,"to",i,"sample"
                #print labels1[i]
                labels1[i] = sorted(labels1[i] + [label_no])
                #print labels1[i] 
                added = added + 1
        else:
            if label_no in labels1[i]:
                print "removing label no",label_no,"in",i,"sample"
                #print labels1[i]
                labels1[i].remove(label_no)
                #print labels1[i]
                removed = removed + 1
    print "","removed",removed,"times"
    print "","added",added,"times"
                 
         
    print "Writing to 1+2 file:", out_path
    jrs_io.store_labels(open(out_path,"w"), labels1)
        