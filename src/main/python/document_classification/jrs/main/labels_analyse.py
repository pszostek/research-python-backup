import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io
import numpy 
from numpy import matrix
import logging
import jrs_results_stats



if __name__ == "__main__":
    print "The program loads JRS labels' file and prints several counts."    

    try:
        labels_path = sys.argv[1]
    except:
        print "Argument expected: path to a labels' file."
        sys.exit(-1)
    print "labels_path:",labels_path        
    
            
    print "Loading labels' file:",  labels_path
    labels = jrs_io.load_labels(open(labels_path))
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))
    n = len(labels)    
    print "",n," multi-labels sets loaded (",len(single_labels),"single labels:",single_labels,")..."
    print " sample five labels:", labels[:5]
    print "------------------------------------------"
    
        
    avg_label_count = float(sum(len(l) for l in labels)) / len(labels)
    print "Avg labels per object:",avg_label_count
    
            
    print "Counting labels (on whole data!)..."
    label2count, label2size, pairlabel2count = jrs_results_stats.labels_stats(labels)
    print " sample counts:", sorted(list(label2count.iteritems())) 
    print " sample `friend`-labels:", sorted(list(label2size.iteritems()))
    print " sample pairlabel2count:",sorted(list(pairlabel2count.iteritems())) 
    print "------------------------------------------"