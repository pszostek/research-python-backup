
import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io
from itertools import izip


def label_ocur(labels, label):
    """Returns bool vector of occurrences of label."""
    return [label in ll for ll in labels]         

def extract_features_ind(line):
    feature_ixs = []
    for entry in line.split(";")[1].split("\t"):
        if len(entry.strip())>0:
            ix = int(entry.strip().split(":")[0])
            ind = float(entry.strip().split(":")[1].split("-")[0])
            if ind>1.0:
                ind = ind / 10000000000.0                
            feature_ixs.append( (ix,ind) )
    return feature_ixs

def filter_features_ind(features_ixs, ind_minval):
    return [ (ix,ind) for ix,ind in features_ixs if ind>=ind_minval ]

#write_csv("tmp.txt",[[1,2,3],[3,2,1],[4,5,6]],3,[True,False])
def write_csv(out_path, filtered_features, feature_no, sel_occurrences):
    f = open(out_path,"w")
    
    #write header
    for j,v in enumerate(filtered_features[0]):
        f.write("f"+str(j)+",")
    f.write("c"+str(feature_no)+"\n")    
    
    #write features
    for i,row in enumerate(filtered_features):
        if i>=len(sel_occurrences):
            break
        for j,v in enumerate(row):
            #f.write("a_"+str(j)+"_"+str(int(v>0))+",")
            f.write(str(v)+",")
        if sel_occurrences[i]:            
            f.write("c"+str(feature_no)+"present\n")
        else:
            f.write("c"+str(feature_no)+"absent\n")
    f.close()
    
    if i>=len(sel_occurrences):
        f = open(out_path+"_testset","w")
        
        #write header
        for j,v in enumerate(filtered_features[0]):
            f.write("f"+str(j)+",")
        f.write("c"+str(feature_no)+"\n")    
                
         #write features
        for i in xrange(len(sel_occurrences), len(filtered_features)):
            row = filtered_features[i]
            for j,v in enumerate(row):
                #f.write("a_"+str(j)+"_"+str(int(v>0))+",")
                f.write(str(v)+",")
            if i%2==0:            
                f.write("c"+str(feature_no)+"present\n")
            else:
                f.write("c"+str(feature_no)+"absent\n")
            
            

def write_txt(out_path, filtered_features):
    f = open(out_path,"w")
    for i,row in enumerate(filtered_features):
        for j,v in enumerate(row):
            f.write(str(v))
            if j<len(row)-1:
                f.write("\t")
        f.write("\n")

LOAD_MAX_ROWS = 40000
            
MAX_POSITIVE_FEATURES = 500
MAX_NEGATIVE_FEATURES = 100
IND_MINVAL = 0.05

if __name__=="__main__":
    print "The program extracts JRS features according to feature-indicators (e.g. fmeasure) file."
    print "MAX_NEGATIVE_FEATURES =", MAX_NEGATIVE_FEATURES
    print "MAX_POSITIVE_FEATURES =", MAX_POSITIVE_FEATURES
    print "IND_MINVAL =", IND_MINVAL
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
        print "Next argument expected: path to a pos-features-ind file."
        sys.exit(-1)
    try:
        negfeaturesind_path = sys.argv[4]
    except:
        print "Next argument expected: path to a neg-features-ind file."
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
    #print label2occurrences    
    print "------------------------------------------"

    print "Loading features from file:",  features_matrix_path
    f = open(features_matrix_path)
    features = jrs_io.load_data(f, cast_method = int, numrows = LOAD_MAX_ROWS)
    print "","loaded", len(features),"x",len(features[0])
    print "------------------------------------------"
    
    
    print "Loading features-ind file",featuresind_path
    print "Loading negfeaturesind_path file",negfeaturesind_path
    f1 = open(featuresind_path)
    f2 = open(negfeaturesind_path)
    f1lines = f1.readlines()
    f2lines = f2.readlines()
    if len(f1lines)!=len(f2lines):
        print "ERROR. len IND != len NEG-IND"
        sys.exit(-1)
    for i, (line, line2) in enumerate(izip(f1lines, f2lines)):
        label = str(i+1)       
        feature_ixs = extract_features_ind(line) 
        feature_ixs2 = extract_features_ind(line2)
        feature_ixs = filter_features_ind(feature_ixs, IND_MINVAL)[:MAX_POSITIVE_FEATURES]
        feature_ixs2 = filter_features_ind(feature_ixs2, IND_MINVAL)[:MAX_NEGATIVE_FEATURES]
        print " label=",label," pos-features:",len(feature_ixs)," neg-features:",len(feature_ixs2) 
        
        selected_features_ixs = feature_ixs+feature_ixs2
        selected_features_ixs = [ix for ix,ind in selected_features_ixs]
        print "","selected_features_ixs=",selected_features_ixs
        selected_features_ixs = set(selected_features_ixs)
        
        print "Filtering out data...."
        filtered_features = []
        for row in features:
            filtered_row = [row[ix] for ix in selected_features_ixs]
            filtered_features.append(filtered_row)    
        print "",len(filtered_features),"x",len(filtered_features[0])
        
        label_out_path = out_path+"_label"+label+"_minf"+str(IND_MINVAL)+"_pf"+str(len(feature_ixs))+"_nf"+str(len(feature_ixs2))
        print "Storing to file",label_out_path
        write_csv(label_out_path+".csv", filtered_features, label, label2occurrences[int(label)])
        write_txt(label_out_path+".txt", filtered_features)
        print "----------------------------------------"
