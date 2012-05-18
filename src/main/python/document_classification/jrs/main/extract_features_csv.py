
import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io
from itertools import izip


def label_ocur(labels, label):
    """Returns bool vector of occurrences of label."""
    return [label in ll for ll in labels]         


LOAD_MAX_ROWS = 2000
KEEP_FEATURES = 100

if __name__=="__main__":
    print "The program extracts JRS features to CSV file according to feature-indicators (e.g. fmeasure) file."
    print "LOAD_MAX_ROWS=",LOAD_MAX_ROWS    
    try:
        features_matrix_path = sys.argv[1]
    except:
        print "First argument expected: path to a features matrix."
        sys.exit(-1)        
    try:
        labels_path = sys.argv[2]
    except:
        print "Next argument expected: path to a labels' file."
        sys.exit(-1)        
    try:
        featuresind_path = sys.argv[3]
    except:
        print "Next argument expected: path to a features-ind file."
        sys.exit(-1)    
    try:
        feature_no = int(sys.argv[4])
    except:
        print "Next argument expected: feature number (for example: 1)"
        sys.exit(-1)                
    try:
        out_path = sys.argv[5]
    except:
        print "Next argument expected: output-features file."
        sys.exit(-1)        
        
        
    print "Loading labels' file:",  labels_path
    labels = jrs_io.load_labels(open(labels_path))
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))
    n = len(labels)    
    print n," multi-labels sets loaded (",len(single_labels),"single labels:",single_labels,")..."
    print "------------------------------------------"
    
    print "Extracting label occurrence vectors"
    label2occurrences = dict( (label,label_ocur(labels, label)) for label in single_labels )
    print "","filtering out for feature no",feature_no
    sel_occurrences = label2occurrences[feature_no]
    #print label2occurrences    
    print "------------------------------------------"
    
    print "Loading features from file:",  features_matrix_path
    f = open(features_matrix_path)
    features = jrs_io.load_data(f, cast_method = float, numrows = LOAD_MAX_ROWS)
    print "","loaded", len(features),"x",len(features[0])
    print "------------------------------------------"

    print "Loading features-ind file",featuresind_path
    for line in open(featuresind_path).xreadlines():
        if line.startswith(str(feature_no)):
            break    
    print line[:100]
    feature_ixs = [int(entry.strip().split(":")[0]) for entry in line.split(";")[1].split("\t") if len(entry.strip())>0]
    
    print "Features selection...."
    selected_features_ixs = feature_ixs[:KEEP_FEATURES]
    print "",KEEP_FEATURES,"features kept"
    
    print "Filtering out data...."
    filtered_features = []
    for row in features:
        filtered_row = [row[ix] for ix in selected_features_ixs]
        filtered_features.append(filtered_row)    
    print "",len(filtered_features),"x",len(filtered_features[0])
    
    print "Storing to csv-output file:",out_path
    import extract_features_posneg
    extract_features_posneg.write_csv(out_path, filtered_features, feature_no, sel_occurrences)
    
