
import time
import os,sys
sys.path.append(r'../')
sys.path.append(r'../../')
import jrs_io
import jrs_evaluation
import jrs_knn_multilabel
import jrs_mostpopular_multilabel
import jrs_random_multilabel
import jrs_1nn_multilabel
import jrs_results_stats
import jrs_multilabel_classifier
import jrs_adjust_trainingset
import jrs_mlknn_adapted
import jrs_fraction_knn_trained    
import getopt
import numpy

def labels_stats(labels):
    label2count = jrs_results_stats.calc_count(labels)   
     
    label2size = {}
    for ll in labels:
        for l in ll:
            label2size[l] = label2size.get(l,0) + len(ll)            
    for l in label2size:
        label2size[l] = float(label2size[l])/label2count[l]
                
    pairlabel2count = {}    
    for ll in labels:
        for i in xrange(0, len(ll)):
            for j in xrange(i+1, len(ll)):
                k1 = (ll[i],ll[j])
                k2 = (ll[j],ll[i])                
                pairlabel2count[k1] = pairlabel2count.get(k1,0)+1
                pairlabel2count[k2] = pairlabel2count.get(k2,0)+1

    return label2count, label2size, pairlabel2count

def min_matrix(dmatrix):
    minval = 10000000000000
    for row in dmatrix:
        for e in row:
            if (e!=0):
                minval = min(e,minval)
    return minval

def max_matrix(dmatrix):
    maxval = -10000000
    for row in dmatrix:
        for e in row:
            maxval = max(e,maxval)
    return maxval

if __name__ == "__main__":    
    print "Arguments: distance-matrix labels-file [configuration-file-without.py]"
            
    try:
        distance_matrix_path = sys.argv[1]
    except:
        print "First argument expected: path to a distance matrix."
        sys.exit(-1)        
    print "distance_matrix_path:", distance_matrix_path
    
    try:
        labels_path = sys.argv[2]
    except:
        print "Second argument expected: path to a labels' file."
        sys.exit(-1)
    print "labels_path:",labels_path        
    
    try:        
        sys.argv[3] = sys.argv[3].replace('.py', '')
        import_string = "from "+sys.argv[3]+" import *"
        exec import_string      
        print "Configuration loaded from file:",sys.argv[3]      
    except:
        print "Using default configuration file: cfg.py"
        from cfg import *    

    print "------------------------------------------"                        
        
    print "k:",k
    print "LOAD_ROWS_FROM_FILE:", LOAD_ROWS_FROM_FILE
    print "CAST_METHOD:",CAST_METHOD
    if CAST_METHOD == 'int':
        cast_method = lambda x: int(float(x))
    else:
        cast_method = lambda x: float(x)
    print "REDUCE_DATA_TO_SIZE:", REDUCE_DATA_TO_SIZE
    print "DEV_FRACTION:", DEV_FRACTION
    print "TRAINING_FRACTION:", TRAINING_FRACTION
    print "ADJUSTING:", ADJUSTING
    print "ADJ_DEFAULT_REMOVE:",ADJ_DEFAULT_REMOVE
    print "FINALTEST:", FINALTEST
    print "FINALTEST_START:", FINALTEST_START
    print "FINALTEST_END:", FINALTEST_END        
    print "FINAL_RESULT_PATH:",FINAL_RESULT_PATH
    print "------------------------------------------"
    
    print "------------------------------------------"
    print "------------------------------------------"
                
        
    print "Loading labels' file:",  labels_path
    labels = jrs_io.load_labels(open(labels_path))
    single_labels = list(set(reduce(lambda l1,l2: l1+l2, (ll for ll in labels))))
    labels = labels[:REDUCE_DATA_TO_SIZE]
    n = len(labels)    
    print "",n," multi-labels sets loaded (",len(single_labels),"single labels:",single_labels,")..."
    print " sample five labels:", labels[:5]
    print "------------------------------------------"
        
    training_size = int(n*TRAINING_FRACTION)    
    dev_size = int(n*DEV_FRACTION)
    testing_size = n - training_size - dev_size
    
    testing_range = (0,testing_size)
    dev_range = (testing_size, testing_size+dev_size)
    training_range = (testing_size+dev_size, n)
    
    testing_labels = labels[testing_range[0]: testing_range[1]] 
    training_labels = labels[training_range[0]: training_range[1]]
    dev_labels = labels[dev_range[0]: dev_range[1]]    
    
    print "Testing sample size:",testing_size, " in range:",testing_range
    print "Dev sample size:",dev_size, " in range:", dev_range
    print "Training sample size:",training_size, " in range:", training_range    
    print "------------------------------------------"
        
    print "Counting labels (on whole data!)..."
    label2count, label2size, pairlabel2count = labels_stats(labels)
    print " sample counts:", sorted(list(label2count.iteritems()))[:10]   
    print " sample `friend`-labels:", sorted(list(label2size.iteritems()))[:10]
    print " sample pairlabel2count:",sorted(list(pairlabel2count.iteritems()))[:50] 
    print "------------------------------------------"
    

    print "------------------------------------------"
    print "------------------------------------------"
    
    avg_label_count = float(sum(len(l) for l in labels)) / len(labels)
    print "Avg labels per object:",avg_label_count
    print "------------------------------------------"                 
        
    print "Loading distances' file:",  distance_matrix_path
    distances = jrs_io.load_data(open(distance_matrix_path), cast_method, numrows = LOAD_ROWS_FROM_FILE)
    try: print "",len(distances), "x",len(distances[0])
    except: pass
    #print "Sample distances:", distances[:5][:5]    
    print "------------------------------------------"
    
    
    #KLASYFIKATOR Ensembled Strongest Fractional Knn
    print "Building Ensembled Strongest FractionKNN..."
    training_single_labels = list(set( reduce(lambda l1,l2: l1+l2, (ll for ll in training_labels)) ))
    print " training labels:", training_single_labels
    print " extracting submatrix..."
    training_distances = jrs_io.extract_submatrix(distances, training_range[0], training_range[1], training_range[0], training_range[1])
    print " training on matrix =",len(training_distances),"x",len(training_distances[0]),"/",len(training_labels)," labels' sets..."
    
    from jrs_fraction_knn_trained_semi_ensembled_strongest_wins import FractionKnnJrsTrainedSemiEnsembledStrongestWins
    
    fknn = FractionKnnJrsTrainedSemiEnsembledStrongestWins(training_distances, range(len(training_distances)), training_labels, k_list, training_single_labels)
    #print "------------------------------------------"

    
    #############################################################################################################################
    #############################################################################################################################
    
    #multilabel_classifier = lambda dists, labels: jrs_knn_multilabel.knn_multilabel(dists, labels, k, int(round(avg_label_count))) # k =7 , 12
    #multilabel_classifier = lambda dists, labels: jrs_knn_multilabel.knn_multilabel_halfbayesian(dists, labels, k, int(round(avg_label_count)), label2count)    
    #multilabel_classifier = lambda dists, labels: jrs_knn_multilabel.knn_fraction_multilabel(dists, labels, k, k/2+1) 
    #multilabel_classifier = lambda dists, labels: jrs_1nn_multilabel.nn1_multilabel(dists, labels)
    #multilabel_classifier = lambda dists, labels: mlknn.classify(dists)         
    multilabel_classifier = lambda dists, labels: fknn.classify(dists)
    #multilabel_classifier = lambda dists, labels: jrs_mostpopular_multilabel.mostpopular_multilabel(label2count, k)
    #multilabel_classifier = lambda dists, labels: jrs_random_multilabel.random_multilabel(label2count, k, can_repeat = False)
        
    #############################################################################################################################
    #############################################################################################################################
    
    if FINALTEST:
        start = time.clock()
        print "Final predicting..."
        print " loading from file:",distance_matrix_path," in range",FINALTEST_START,"-",FINALTEST_END 
        predicted_labels = []
        for i,line in enumerate(open(distance_matrix_path).xreadlines()):
            if i%1000 == 0: print "",i,"rows processed..."
            if i>=FINALTEST_END: break
            if i<FINALTEST_START: continue 
            row = [cast_method(x) for x in line.split()]
            final2training_distances = row[training_range[0]:training_range[1]]
            predicted_labels.append(multilabel_classifier(final2training_distances, training_labels))
        jrs_io.store_labels(open(FINAL_RESULT_PATH,"w"), predicted_labels)
        lcount = [len(ll) for ll in predicted_labels]
        print " avg labels in predicted:", float(sum(lcount))/(len(lcount))
        print " done in", (time.clock() - start), "sec..."
        print "------------------------------------------"
    else:
        def eval():
            start = time.clock()    
            print "Calculating predictions of ",len(testing_labels)," labels' sets..."
            predicted_labels = jrs_multilabel_classifier.classify_multilabel(testing2training_distances, training_labels, multilabel_classifier)            
            accuracy, precision, recall, hammingloss, subset01loss, fmeasure =  jrs_evaluation.jrs_evaluate(testing_labels, predicted_labels)
            print " accuracy:", accuracy,"\n precision:", precision,"\n recall:", recall,"\n fmeasure:", fmeasure                
            lcount = [len(ll) for ll in predicted_labels]
            print " avg labels in predicted:", float(sum(lcount))/(len(lcount))
            print " done in", (time.clock() - start), "sec..."
            return predicted_labels
        
        testing2training_distances = jrs_io.extract_submatrix(distances, testing_range[0], testing_range[1], training_range[0], training_range[1])    
        predicted_labels = eval()
        print "------------------------------------------"
        
        if ADJUSTING:        
            dev2training_distances = jrs_io.extract_submatrix(distances, dev_range[0], dev_range[1], training_range[0], training_range[1])
            removal_order = jrs_adjust_trainingset.adjust_training_set(dev2training_distances, training_labels, dev_labels, multilabel_classifier, ADJ_DEFAULT_REMOVE)    
            print "------------------------------------------"
            jrs_adjust_trainingset.remove_columns(testing2training_distances, removal_order)
            jrs_adjust_trainingset.remove_list(training_labels, removal_order)
            predicted_labels = eval()
            print "------------------------------------------"
            
        print "Errors report:"
        mlstats = jrs_results_stats.prediction_stats(predicted_labels, testing_labels)
        print " ml_stats\nlabel\toracle,\tpred,\tmissed,\tredun,\tTP,\tFP,\tTN,\tFN"    
        for  l,(o, p, m, r, tp,fp,tn,fn,precision,recall,f1) in mlstats.iteritems():
            print l,"\t",o,"\t",p,"\t",m,"\t",r,"\t",tp,"\t",fp,"\t",tn,"\t",fn,"\t",precision,"\t",recall,"\t",f1                        
        print "------------------------------------------"

