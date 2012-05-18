
import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io
from itertools import izip



if __name__=="__main__":    
    print "The program reads file with values of features' indicators and prints several statistics."
    try:
        featuresind_path = sys.argv[1]
    except:
        print "Next argument expected: path to a features-ind file."
        sys.exit(-1)            
    try:
        feature_no = int(sys.argv[2])
    except:
        print "Next argument expected: feature number (for example: 1)"
        sys.exit(-1)                        
        
    print "Loading features-ind file",featuresind_path
    for line in open(featuresind_path).xreadlines():
        if line.startswith(str(feature_no)):
            break    
    print line[:100]
    feature_ixs = [( (entry.strip().split(":")[0]),(entry.strip().split(":")[1]) ) for entry in line.split(";")[1].split("\t") if len(entry.strip())>0]
    
    print "Features analysis...."
    print "10th pos -> f1=",feature_ixs[10][1]
    print "25th pos -> f1=",feature_ixs[25][1]
    print "50th pos -> f1=",feature_ixs[50][1]
    print "100th pos -> f1=",feature_ixs[100][1]
    print "250th pos -> f1=",feature_ixs[250][1]
    print "500th pos -> f1=",feature_ixs[500][1]
    print "1000th pos -> f1=",feature_ixs[1000][1]
    print "2500th pos -> f1=",feature_ixs[2500][1]
    print "5000th pos -> f1=",feature_ixs[5000][1]
    print "10000th pos -> f1=",feature_ixs[10000][1]
    
