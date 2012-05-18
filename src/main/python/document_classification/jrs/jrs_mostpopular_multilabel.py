

def mostpopular_multilabel(label2count, k):
    """Returns list of k most popular labels.
    
    label2count - dictionary {label:count}
    """
    return dict(sorted((v,k) for k,v in label2count.iteritems())[-k:]).values()