
import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io
from itertools import izip
import jrs_evaluation


def label_ocur(labels, label):
    """Returns bool vector of occurrences of label."""
    return [label in ll for ll in labels]         

MIN_FRACTION_OF_VOTES = 0.03
FEATURES_NUM = 500
LOAD_MAX_ROWS = 2000

if __name__=="__main__":
    print "The program reads JRS features (data) file and aggregate by voting answers of single features used as classifiers."
    print "LOAD_MAX_ROWS=",LOAD_MAX_ROWS
    print "FEATURES_NUM=",FEATURES_NUM
    print "MIN_FRACTION_OF_VOTES=",MIN_FRACTION_OF_VOTES    
    try:
        features_matrix_path = sys.argv[1]
    except:
        print "First argument expected: path to a features matrix."
        sys.exit(-1)        

    try:
        featuresind_path = sys.argv[2]
    except:
        print "Next argument expected: path to a features-ind file."
        sys.exit(-1)
            
    try:
        out_path = sys.argv[3]
    except:
        print "Next argument expected: output-labels file."
        sys.exit(-1)  
        
    try:
        labels_path = sys.argv[4]
    except:
        print "Next argument expected: path to a labels' file."
        sys.exit(-1)        
      
        
    print "Loading features-ind file",featuresind_path
    label2feature_ixs = {}
    for line in open(featuresind_path).xreadlines():
        label = int(line.split(";")[0])
        print "","loading label",label
        feature_ixs = [int(entry.strip().split(":")[0]) for entry in line.split(";")[1].split("\t") if len(entry.strip())>0]
        feature_ixs = feature_ixs[:FEATURES_NUM]
        label2feature_ixs[label] = feature_ixs 
    #print label2feature_ixs
    
    print "Loading labels' file:",  labels_path
    labels = jrs_io.load_labels(open(labels_path))
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))
    n = len(labels)    
    print n," multi-labels sets loaded (",len(single_labels),"single labels:",single_labels,")..."
    print "------------------------------------------"
            
    print "Classifying file:",  features_matrix_path
    f = open(features_matrix_path)
    predicted_labels = []
    for i,line in enumerate(f.xreadlines()):
        if i%1000==0: print "",i,"..."
        
        row = [int(x) for x in line.split()]
        ll = []
        for label,feature_ixs in label2feature_ixs.iteritems():
            says_yes = sum(row[ix]>0 for ix in feature_ixs)
            if says_yes >= len(feature_ixs)*MIN_FRACTION_OF_VOTES:
                ll.append(label)        
        ll = sorted(ll)
        
        predicted_labels.append(ll)
                
        print "",i," oracle",labels[i]," pred",ll
        print "","len=",len(labels[:(i+1)]), len(predicted_labels)
        accuracy, precision, recall, hammingloss, subset01loss, fmeasure =  jrs_evaluation.jrs_evaluate(labels[:(i+1)], predicted_labels)
        print "\t\t\t\t\t","%.2f" %precision,"%.2f" %recall,"%.2f" %fmeasure
    print "------------------------------------------"
    
    accuracy, precision, recall, hammingloss, subset01loss, fmeasure =  jrs_evaluation.jrs_evaluate(labels, predicted_labels)
    print "\t\t\t\t\t","%.2f" %precision,"%.2f" %recall,"%.2f" %fmeasure
    
    print "Wrining results to", out_path 
    jrs_io.store_labels(open(out_path,"w"), predicted_labels)
    
    