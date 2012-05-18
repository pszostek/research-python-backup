
import sys
import itertools
from itertools import izip
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io

DEFAULT_FMEASURE_PATH = "cfg/default_fmeasure.txt"

if __name__=="__main__":
    print "The program aggregates (by voting) list of labels using many files (JRS labels files)."
    
    try:
        paths = sys.argv[1]
        paths = paths.split(',')
    except:
        print "First argument expected: list of jrs-output-files separated with <,> (comma)"
        sys.exit(-1)
        
    try:
        out_path = sys.argv[2]
    except:
        print "Second argument expected: output file"
        sys.exit(-1)
        
    try:
        fmeasure_paths = sys.argv[3]
        fmeasure_paths = fmeasure_paths.split(',') 
    except:
        print "Third argument expected: list of fmeasure files separated with <,> (comma)"
        print "Argument not given using default..."
        fmeasure_paths = [DEFAULT_FMEASURE_PATH for path in paths]        
     
                   
    print "LOADING JRS-OUTPUT-FILES:",paths         
    files_labels = [] #at position list of lists of labels
    for path in paths:
        print "","loading:", path
        multilabels = jrs_io.load_labels(open(path), cast_method = int, separator=',')
        print "","sample:",multilabels[:5]
        files_labels.append( multilabels )
    
    print "LOADING FMEASURE-FILES:",fmeasure_paths         
    files_fmeasures = [] #at position dictionary{label_no: fmeasure}
    for path in fmeasure_paths:
        print "","loading:", path
        label2fmeasure = {}
        for line in open(path).xreadlines():
            #print "","line:",line
            if len(line.strip()) == 0: break
            label_no = int(line.split()[0])
            f1 = float(line.split()[1])    
            label2fmeasure[label_no] = f1
        print "","sample:",list(label2fmeasure.iteritems())[:5]
        files_fmeasures.append(label2fmeasure)    
                         
    num_classifiers = len(files_labels)
    print "NUM CLASSIFIERS:",num_classifiers
    num_samples = len(files_labels[0])
    print "NUM SAMPLES:", num_samples
                     
    print "VOTING of",num_classifiers,"classifiers"   
    predicted_labels = []     
    for sample_no in xrange(num_samples):
                        
        all_sample_labels = [] #wszystkie proponowane etykiety dla danego sampla                
        for classifier_no in xrange(num_classifiers):  
            #print classifier_no, sample_no
            all_sample_labels.extend(files_labels[classifier_no][sample_no]) 
            
        selected_sample_labels = [] #wybrane dla danego sampla
        for label in sorted(set(all_sample_labels)):            
            votes_for_yes = []
            votes_for_no = [] 
            for classifier_no in xrange(num_classifiers):                
                if label in files_labels[classifier_no][sample_no]:
                    votes_for_yes.append(files_fmeasures[classifier_no][label])
                else:
                    votes_for_no.append(files_fmeasures[classifier_no][label])
                    
            #votes = sorted(votes_for_yes + votes_for_no)                    
            print "","sample_no:",sample_no," label:",label,"votes_for_yes:",votes_for_yes,"votes_for_no:",votes_for_no            
            #diff = min(votes[2]-votes[1], votes[1]-votes[0])
            #print "","diff=",diff
            #subs = max(votes[0] - diff,0.0)
            #print "","subs=",subs
            #votes_for_yes = [v-subs for v in votes_for_yes]
            #votes_for_no = [v-subs for v in votes_for_no]
            #print "","sample_no:",sample_no," label:",label,"votes_for_yes:",votes_for_yes,"votes_for_no:",votes_for_no
            
            try:      
                #yes = float(sum(votes_for_yes))/len(votes_for_yes)
                yes = sum(votes_for_yes)
            except:
                yes = 0.0
            try:
                #no = float(sum(votes_for_no))/len(votes_for_no)
                no = sum(votes_for_no)
            except:
                no = 0.0
                   
            if yes > no:
                selected_sample_labels.append(label)
                                                                    
        predicted_labels.append(sorted(selected_sample_labels))        
        print "","all labels:",all_sample_labels," -> sel:",sorted(selected_sample_labels),"\n"
              
              
    print "STORING TO FILE:", out_path
    import sys
    sys.path.append(r'../')
    sys.path.append(r'../../')
    import jrs_io
    jrs_io.store_labels(open(out_path, "w"), predicted_labels)
                
    