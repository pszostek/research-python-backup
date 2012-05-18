
import itertools
from itertools import izip

def labels_stats(labels):
    label2count = calc_count(labels)   
     
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

def calc_count(labels):
    """Takes labels (list of lists) and returns dictionary {label: count}."""
    label2count = {}
    for lvec in labels:
        for l in lvec:
            label2count[l] = label2count.get(l,0)+1
    return label2count
         

def error_counts(predicted_labels, oracle_labels):
    """Returns two dictionaries that contain error counts for labels.
    
    Returns: 
     error_missed = dictionary {label: number of times when label should be used but was not used}
     error_redundant = dictionary {label: number of times when label should not be used but was used }    
    """
    error_missed = {}
    error_redundant = {}
    for plabels, olabels in izip(predicted_labels, oracle_labels):
        for plabel in plabels:
            if not plabel in olabels:
                error_redundant[plabel] = error_redundant.get(plabel, 0) + 1
        for olabel in olabels:
            if not olabel in plabels:
                error_missed[olabel] = error_missed.get(olabel, 0) + 1
    return error_missed, error_redundant


def prediction_stats(predicted_labels, testing_labels):
    error_missed, error_redundant = error_counts(predicted_labels, testing_labels)
    olabel2count = calc_count(testing_labels)
    plabel2count = calc_count(predicted_labels)
    #print " used by oracle:", olabel2count #print " predicted:", plabel2count #print " missed:", error_missed #print " redundant:", error_redundant          
    stats = dict((label, (olabel2count.get(label, 0), plabel2count.get(label, 0), error_missed.get(label, 0), error_redundant.get(label, 0)) ) for label in olabel2count)
    #print " stats{label: oracle, predicted, missed, redundant}:", stats   
    testing_size = len(testing_labels)        
    mlstats = dict((label, (o, p, m, r, o-m, r, testing_size-o-r, m) ) for label,(o,p,m,r) in stats.iteritems())
    
    mlstats2 = {}
    for  l,(o, p, m, r, tp,fp,tn,fn) in mlstats.iteritems():               
        try:
            precision   = float(tp) / (tp+fp)
        except:
            precision   = 0.0
        try:
            recall      = float(tp) / (tp+fn)
        except:
            precision   = 0.0
        try:
            f1          = 2.0*precision*recall / (precision+recall)
        except:
            f1          = 0.0
        mlstats2[l] = (o, p, m, r, tp,fp,tn,fn,precision,recall,f1)
    return mlstats2    