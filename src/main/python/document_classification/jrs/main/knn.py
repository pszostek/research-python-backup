
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

TO_BE_REMOVED = [31, 35, 49, 21, 11, 10, 77, 6]
def filter_out_labels(labels):
    return [[l for l in ll if not l in TO_BE_REMOVED ] for ll in labels]

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

def pairwisecount_tree(label2count, pairlabel2count, outpath = "/tmp/pairlabel2dist_avg_tree"):
    import jrs_labels_tree 
    print "","calculating pairwise distances using counts of pairs:"
    
    def pairwise_dist_calc(l1,l2, count):
        sim1 = float(count)/label2count[l1]
        sim2 = float(count)/label2count[l2]
        sim_avg = (sim1+sim2)/2.0 
        return  1.0 / sim_avg
    
    pairlabel2dist = dict( ((l1,l2),pairwise_dist_calc(l1,l2,count)) for (l1,l2),count in pairlabel2count.iteritems() )
    maxdist = max(pairlabel2dist.values())
    print "","pairlabel2dist=", sorted(list(pairlabel2dist.iteritems()))[:20]
    print ""," maxdist=",maxdist, " => default dist =",2.0*maxdist
    print ""," mindist=",min(pairlabel2dist.values())
            
    dmatrix = jrs_labels_tree.build_sim_matrix_labcount(pairlabel2dist, labels, maxdist*2.0)
    print numpy.array(dmatrix)
    
    treelabels = [str(i+1) for i in range(len(single_labels))]
    
    def gen_tree(outph, hd):
        phylo_tree = jrs_labels_tree.upgma(treelabels, dmatrix, agreggation_method = 'a', anonclades = hd)        
        print "","writing tree to:",outph
        jrs_labels_tree.write_tree(phylo_tree, outph)    
        print "","dict_tree=",jrs_labels_tree.phylotree2dicttree(phylo_tree)
    
    gen_tree(outpath, False)
    gen_tree(outpath+"_hd", True)

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

def dist_tree(training_distances, training_labels, outpath = "/tmp/training_distances_avg_tree"):
    import jrs_labels_tree
    print "","building label vs label distance matrix using averaging..."
    
    #dmatrix = jrs_io.load_data(open("/tmp/dist_tree_dmatrix.txt"), cast_method=float)
    #print "","loaded matrix =",len(dmatrix),"x",len(dmatrix[0]),"..."
    #import numpy
    #print numpy.array(dmatrix)
    
    print "","training on matrix =",len(training_distances),"x",len(training_distances[0]),"/",len(training_labels)," labels' sets..."
    dmatrix = jrs_labels_tree.build_sim_matrix_labels(training_distances, training_labels)
    print "","clearing diagonal..."
    for i in xrange(len(dmatrix)):
        dmatrix[i][i] = 0.0
    minval = min_matrix(dmatrix)
    maxval = max_matrix(dmatrix)
    print numpy.array(dmatrix)    
    print "","minval:",minval
    print "","maxval:",maxval
    jrs_io.store_data(open("/tmp/dist_tree_dmatrix.txt","w"), dmatrix)
        
    
    print "","transforming dmatrix by substracting minval"
    dmatrix_t = [[(e-minval) for e in row ] for row in dmatrix ]
    dmatrix = dmatrix_t         
    minval = min_matrix(dmatrix)
    maxval = max_matrix(dmatrix)
    print numpy.array(dmatrix)
    print "","minval:",minval
    print "","maxval:",maxval
    jrs_io.store_data(open("/tmp/dist_tree_dmatrix_t.txt","w"), dmatrix)
    
    #dmatrix = jrs_io.load_data(open("/tmp/dist_tree_dmatrix_t.txt"), cast_method=float)
    #print "","loaded matrix =",len(dmatrix),"x",len(dmatrix[0]),"..."
    #import numpy
    #print numpy.array(dmatrix)
    
    treelabels = [str(i+1) for i in range(len(single_labels))]
    print "","treelabels:", treelabels            
    def gen_tree(outph, hd):
        phylo_tree = jrs_labels_tree.upgma(treelabels, dmatrix, agreggation_method = 'a', anonclades = hd)    
        print "","writing tree to:",outph
        jrs_labels_tree.write_tree(phylo_tree, outph)
        print "","dict_tree=",jrs_labels_tree.phylotree2dicttree(phylo_tree)
        
    gen_tree(outpath, False)
    gen_tree(outpath+"_hd", True)



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
    
    #print "Building tree using pairlabel2count & label2count"
    #outpath = "/tmp/pairlabel2dist_avg_tree"
    #pairwisecount_tree(label2count, pairlabel2count, outpath)
    #print "------------------------------------------"

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
    
    #print "Building tree on sample vs. sample distances avg"
    #outpath = "training_distances_avg_tree"
    #print " extracting submatrix..."
    #training_distances = jrs_io.extract_submatrix(distances, training_range[0], training_range[1], training_range[0], training_range[1])
    #dist_tree(training_distances, training_labels, outpath)    
    #dist_tree(distances, labels, outpath)
    #print "------------------------------------------"
    #print "------------------------------------------"
    #print "------------------------------------------"
    
      
    #print "Building mlknn..."
    #training_single_labels = list(set( reduce(lambda l1,l2: l1+l2, (ll for ll in training_labels)) ))
    #print " training labels:", training_single_labels
    #print " extracting submatrix..."
    #training_distances = jrs_io.extract_submatrix(distances, training_range[0], training_range[1], training_range[0], training_range[1])
    #print " training on matrix =",len(training_distances),"x",len(training_distances[0]),"/",len(training_labels)," labels' sets..."
    #mlknn = jrs_mlknn_adapted.MlKnnJrs(training_distances, training_labels, k, training_single_labels)
    #print "------------------------------------------"
    
    """
    print "Building FractionKNN..."
    training_single_labels = list(set( reduce(lambda l1,l2: l1+l2, (ll for ll in training_labels)) ))
    print " training labels:", training_single_labels
    print " extracting submatrix..."
    training_distances = jrs_io.extract_submatrix(distances, training_range[0], training_range[1], training_range[0], training_range[1])
    print " training on matrix =",len(training_distances),"x",len(training_distances[0]),"/",len(training_labels)," labels' sets..."
    fknn = jrs_fraction_knn_trained.FractionKnnJrsTrained(training_distances, range(len(training_distances)), training_labels, k, training_single_labels)
    print "------------------------------------------"
    """
    
    print "Building Hierarchical FractionKNN..."
    training_single_labels = list(set( reduce(lambda l1,l2: l1+l2, (ll for ll in training_labels)) ))
    print " training labels:", training_single_labels
    print " extracting submatrix..."
    training_distances = jrs_io.extract_submatrix(distances, training_range[0], training_range[1], training_range[0], training_range[1])
    print " training on matrix =",len(training_distances),"x",len(training_distances[0]),"/",len(training_labels)," labels' sets..."
    
    #base_dict = {'a80': {'a79': {'a76': {'59': {}, '51': {}}, 'a74': {'27': {}, 'a70': {'62': {}, 'a69': {'a38': {'68': {}, '53': {}}, 'a67': {'a59': {'a55': {'a50': {'56': {}, '28': {}}, 'a54': {'44': {}, '13': {}}}, 'a49': {'a47': {'a39': {'a33': {'5': {}, '14': {}}, '61': {}}, '4': {}}, '43': {}}}, 'a65': {'a57': {'25': {}, '63': {}}, '34': {}}}}}}}, 'a78': {'a77': {'a75': {'a72': {'a68': {'82': {}, '41': {}}, 'a71': {'a64': {'73': {}, 'a56': {'19': {}, '52': {}}}, 'a66': {'a58': {'69': {}, 'a53': {'a43': {'32': {}, 'a31': {'a23': {'77': {}, 'a4': {'72': {}, '22': {}}}, '17': {}}}, '70': {}}}, 'a61': {'a44': {'76': {}, 'a42': {'18': {}, 'a41': {'75': {}, 'a40': {'a37': {'39': {}, 'a35': {'a32': {'a28': {'26': {}, 'a25': {'a15': {'a13': {'a9': {'33': {}, '36': {}}, 'a11': {'a8': {'1': {}, 'a6': {'a3': {'a2': {'a1': {'a0': {'3': {}, '45': {}}, '29': {}}, '54': {}}, '37': {}}, '16': {}}}, '6': {}}}, 'a12': {'a7': {'2': {}, '66': {}}, '23': {}}}, '20': {}}}, 'a29': {'8': {}, 'a27': {'a22': {'a20': {'a17': {'a14': {'46': {}, '50': {}}, 'a10': {'9': {}, 'a5': {'47': {}, '42': {}}}}, '64': {}}, 'a19': {'31': {}, '58': {}}}, '67': {}}}}, 'a34': {'a30': {'15': {}, 'a26': {'a21': {'11': {}, 'a16': {'10': {}, '49': {}}}, 'a18': {'79': {}, '35': {}}}}, '38': {}}}}, '65': {}}}}}, '21': {}}}}}, 'a63': {'55': {}, 'a60': {'a51': {'a45': {'24': {}, '48': {}}, 'a36': {'74': {}, 'a24': {'71': {}, '78': {}}}}, 'a52': {'a46': {'80': {}, '40': {}}, 'a48': {'60': {}, '57': {}}}}}}, '7': {}}, 'a73': {'12': {}, '81': {}}}}, 'a62': {'83': {}, '30': {}}}
    #base_dict = {'a79': {'25': {}, '13': {}, '27': {}, '59': {}, '14': {}, '51': {}, '44': {}, '56': {}, '28': {}, '43': {}, '53': {}, '34': {}, '61': {}, '62': {}, '63': {}, '5': {}, '4': {}, '68': {}}, 'a78': {'58': {}, '60': {}, '64': {}, '65': {}, '66': {}, '67': {}, '82': {}, '69': {}, '80': {}, '81': {}, '24': {}, '26': {}, '20': {}, '21': {}, '48': {}, '49': {}, '46': {}, '47': {}, '45': {}, '42': {}, '29': {}, '40': {}, '41': {}, '1': {}, '3': {}, '2': {}, '7': {}, '6': {}, '9': {}, '8': {}, '18': {}, '77': {}, '76': {}, '75': {}, '74': {}, '73': {}, '72': {}, '71': {}, '70': {}, '79': {}, '78': {}, '11': {}, '10': {}, '39': {}, '38': {}, '15': {}, '22': {}, '17': {}, '16': {}, '19': {}, '54': {}, '31': {}, '23': {}, '37': {}, '36': {}, '35': {}, '52': {}, '33': {}, '55': {}, '32': {}, '12': {}, '57': {}, '50': {}}}
    base_dict = { '31':{},
  'z1':{ '35':{}, 'q12':{'49':{},'21':{},'11':{},'10':{}} },
  'z2':{ '48':{}, '24':{}, '78':{}, '79':{}, '71':{}, '74':{}, '57':{}, '80':{}, '60':{} },
  'z3':{ 'q31':{'55':{}, '43':{}, '15':{}, '82':{}}, 'q32':{'72':{}, '22':{}, '47':{}, '58':{}, '75':{}, '65':{}, '39':{}, '42':{}, '41':{}, '9':{}}, 'q33':{'19':{}, '67':{}, '64':{}, '50':{}, '46':{}, '38':{}, '8':{}} },
  'z4':{ 'q41':{'59':{}, '63':{}, '34':{}, '25':{}, '14':{}}, 'q42':{'76':{}, '62':{}, '51':{}, '5':{}}, 'q43':{'56':{}, '73':{}, '52':{}, '27':{}, '61':{}, '44':{}, '40':{}, '13':{}, '4':{}}, 'q44':{'28':{}, '68':{}, '53':{}} },
  'z5':{ 'q51':{'30':{}, '32':{}, '83':{}, '17':{}}, 'q52':{'81':{}, '69':{}, '12':{}} },
  'z6':{ '77':{}, '6':{}},
  'z7':{ 'q71':{'36':{}, '20':{}, '33':{}, '7':{}}, 'q72':{'70':{}, '18':{}, '2':{}}, 'q73':{'26':{}, '16':{}, '37':{}, '29':{}, '54':{}, '23':{}, '45':{}}, 'q74':{'66':{}, '3':{}, '1':{}} }
}
    #print label_mapping_list
    import find_structure_in_label_tree
    label_mapping_list, not_continue_deepening_elements, leaves = find_structure_in_label_tree.get_labeltree_data(base_dict)
    continue_deepening = lambda x: x not in not_continue_deepening_elements
    is_leaf_node = lambda x: x in leaves
    
    import jrs_hierarchical_fractional_knn_trained
    fknn = jrs_hierarchical_fractional_knn_trained.HierarchicalFractionalJrsClassifier(training_distances, training_labels, k, label_mapping_list, continue_deepening, is_leaf_node)
    print "------------------------------------------"
    
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
            try:
                print testing_labels[:10],"\n", predicted_labels[:10]                                    
                accuracy, precision, recall, hammingloss, subset01loss, fmeasure =  jrs_evaluation.jrs_evaluate(testing_labels, predicted_labels)
            except:
                print "[knn] Error in jrs_evaluation.jrs_evaluate(testing_labels, predicted_labels):",testing_labels, predicted_labels
            print " accuracy:", accuracy,"\n precision:", precision,"\n recall:", recall,"\n fmeasure:", fmeasure                
            lcount = [len(ll) for ll in predicted_labels]
            #print " avg labels in predicted:", float(sum(lcount))/(len(lcount))            
            #accuracy, precision, recall, hammingloss, subset01loss, fmeasure =  jrs_evaluation.jrs_evaluate(filter_out_labels(testing_labels), filter_out_labels(predicted_labels))
            #print " postfiltering-accuracy:", accuracy,"\n postfiltering-precision:", precision,"\n postfiltering-recall:", recall,"\n postfiltering-fmeasure:", fmeasure
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
        print " ml_stats\nlabel\toracle,\tpred,\tmissed,\tredun,\tTP,\tFP,\tTN,\tFN\tprc\trcl\tf1"            
        for  l,(o, p, m, r, tp,fp,tn,fn,precision,recall,f1) in mlstats.iteritems():
            print l,"\t",o,"\t",p,"\t",m,"\t",r,"\t",tp,"\t",fp,"\t",tn,"\t",fn,"\t","%.2f" %precision,"\t","%.2f" %recall,"\t","%.2f" %f1                        
        print "------------------------------------------"

