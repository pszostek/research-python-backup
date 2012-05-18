
import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io

if __name__ == "__main__":       
    print "The program takes JRS trainingLabels file and splits according to labels (single file for each label)." 

    try:
        labels_path = sys.argv[1]
    except:
        print "Argument expected: path to a labels' file."
        sys.exit(-1)
    try:
        out_path_prefix = sys.argv[2]
    except:
        print "Argument expected: output file prefix."
        sys.exit(-1)        
                
    print "Loading labels' file:",  labels_path
    labels = jrs_io.load_labels(open(labels_path))
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))
    #training_labels = labels[:training_size]
    n = len(labels)    
    print n," multi-labels sets loaded (",len(single_labels),"single labels:",single_labels,")..."
    print "Sample five labels:", labels[:5]
    print "------------------------------------------"
    
    for label in single_labels:
        occurrence = [label in ll for ll in labels]
        out_path = out_path_prefix + str(label)
        print "Writing output to:",out_path
        fout = open(out_path, "w")
        for ocur in occurrence:
            if ocur:
                fout.write(str(label)+"\n")
            else:
                fout.write("\n")
                
