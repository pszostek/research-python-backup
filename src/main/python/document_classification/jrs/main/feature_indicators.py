

import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io
from itertools import izip

def classifier_gtz(feature_vector):
    return [v>0.0 for v in feature_vector] 

def classifier_ez(feature_vector):
    return [v==0.0 for v in feature_vector] 

def fmeasure_calc(label_occurrences_vector, feature_vector, classifier = classifier_ez):
    label_pred_vector = classifier(feature_vector)
    TP = FP = TN = FN = 0
    for oracle, predicted in izip(label_occurrences_vector, label_pred_vector):
        if oracle:
            if predicted:
                TP = TP + 1 
            else:
                FN = FN + 1  
        else:
            if predicted:
                FP = FP + 1  
            else:
                TN = TN + 1
    try:
        precision   = float(TP) / (TP+FP)
    except:
        precision   = 0.0
    try:
        recall      = float(TP) / (TP+FN)
    except:
        precision   = 0.0
    try:
        f1          = 2.0*precision*recall / (precision+recall)
    except:
        f1          = 0.0
    return f1,precision,recall


def label_ocur(labels, label):
    """Returns bool vector of occurrences of label."""
    return [label in ll for ll in labels]         

def extract_col(matrix, col_ix):
    return [ row[col_ix] for row in matrix ]    


LOAD_MAX_ROWS = 10000
INDICATOR = fmeasure_calc

if __name__=="__main__":
    print "The program calculates values of features' indicators (f1 of a single-feature-classifier)."
    print "LOAD_MAX_ROWS=",LOAD_MAX_ROWS
    print "INDICATOR=",INDICATOR
    try:
        features_matrix_path = sys.argv[1]
    except:
        print "First argument expected: path to a features matrix."
        sys.exit(-1)
    try:
        labels_path = sys.argv[2]
    except:
        print "Second argument expected: path to a labels' file."
        sys.exit(-1)
    try:
        out_path = sys.argv[3]
    except:
        print "Third argument expected: output-report file."
        sys.exit(-1)        
    #try:
    #    training_size = int(sys.argv[3])
    #except:
    #    print "Third argument expected: how many samples should be used for training."
    #    sys.exit(-1) 
        
        
    print "Loading labels' file:",  labels_path
    labels = jrs_io.load_labels(open(labels_path))
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))
    #training_labels = labels[:training_size]
    n = len(labels)    
    print n," multi-labels sets loaded (",len(single_labels),"single labels:",single_labels,")..."
    print "Sample five labels:", labels[:5]
    print "------------------------------------------"
    
    print "Extracting label occurrence vectors"
    label2occurrences = dict( (label,label_ocur(labels, label)) for label in single_labels )
    #print label2occurrences    
    print "------------------------------------------"
    
    print "Loading features from file:",  features_matrix_path
    f = open(features_matrix_path)
    features = jrs_io.load_data(f, cast_method = float, numrows = LOAD_MAX_ROWS)
    print "","loaded", len(features),"x",len(features[0])
    print "------------------------------------------"

    print "Calculating and reporting to:", out_path
    fout = open(out_path, "w")
    for label in single_labels:
        print "","considering label:",label
        label_occurrences_vector = label2occurrences[label]
        
        indval_colix = [] 
        for colix in xrange(len(features[0])):             
            indval,precision,recall = INDICATOR(label_occurrences_vector, extract_col(features, colix))
            indval_colix.append( (indval,colix,precision,recall) )
                    
        fout.write(str(label)+";\t")
        for indval,colix,precision,recall in sorted(indval_colix,reverse = True):
            #fout.write(str(colix)+":"+str(int(indval*10000000000.0))+"\t")            
            fout.write(str(colix)+":"+str(indval)+"-"+str(precision)+"-"+str(recall)+"\t")
        fout.write("\n")    
        
                