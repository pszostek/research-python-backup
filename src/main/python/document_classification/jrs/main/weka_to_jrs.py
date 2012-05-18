
import sys
import itertools
from itertools import izip

sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io

if __name__=="__main__":
    
    try:
        aux_file = sys.argv[1]
    except:
        print "Argument expected: weka-csv (inst#,actual,predicted,error,prediction) (with header) file with labels"
        sys.exit(-1)
    try:
        label_no = int(sys.argv[2])
    except:
        print "Argument expected: label to be overwritten no."
        sys.exit(-1)
 

    print "Loading labels' (weka-csv) file:",  aux_file
    #inst#,actual,predicted,error,prediction
    lines = open(aux_file).readlines()
    labels2bool = list( line.split(",")[2].find("present")>=0 for line in lines[1:] if len(line.strip())>0 )
    print "",len(labels2bool),"rows loaded"
    #print labels2bool
    
    labels = []
    for ocur in labels2bool:
        if ocur:
            labels.append([label_no])
        else:
            labels.append([])

    aux_file = aux_file + "_jrs.txt"
    print "Writing to file:", aux_file
    jrs_io.store_labels(open(aux_file,"w"), labels)
    