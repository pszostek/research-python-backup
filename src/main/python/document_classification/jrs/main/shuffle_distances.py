

import sys
import itertools
from itertools import izip
import random
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io


if __name__=="__main__":
    try:
        distance_matrix_path = sys.argv[1]
    except:
        print "First argument expected: distance_matrix_path"
        sys.exit(-1)
        
    try:
        labels_path = sys.argv[2]
    except:
        print "Second argument expected: labels_path"
        sys.exit(-1)
    
    print "The program shuffles distances and trainingLabels."
    
    print "Loading labels' file:",  labels_path
    labels = jrs_io.load_labels(open(labels_path))
    n = len(labels)
    print "",n," labels' sets loaded."
    
    order = range(n)
    random.shuffle(order)
    print "Random order:", order[:30],"..."
    
    print "Shuffling labels..."
    labels_shuffled = [labels[ix] for ix in order]
    jrs_io.store_labels(open(labels_path+"_shuffled","w"), labels_shuffled)
    
    print "Loading distances' file:",  distance_matrix_path
    distances = jrs_io.load_data(open(distance_matrix_path), lambda x: x)
    try: print "",len(distances), "x",len(distances[0])
    except: pass
    
    print "Extending order..."    
    order = order + range(n, len(distances))
    print "Extended order:", order    
    
    print "Shuffling columns"
    distances_tmp = []
    for row in distances:
        new_row = [ row[ix] for ix in order ]
        distances_tmp.append(new_row)
    
    print "Shuffling rows"
    distances_shuffled = []
    for ix in order:
        distances_shuffled.append(distances_tmp[ix])
    
    fout = open(distance_matrix_path+"_shuffled","w")
    print "Storing to ",fout
    jrs_io.store_data(fout, distances_shuffled)
          
    
    
    