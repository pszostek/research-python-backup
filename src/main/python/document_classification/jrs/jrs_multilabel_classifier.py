     
       
def classify_multilabel(testing2training_distances, training_labels, multilabel_classifier):      
    """Predicts multi-labels for testing objects.
    
    testing2training_distances - matrix (list of lists) of distances: rows - testing objects, cols - training objects
    training_labels - multi-labels (list of lists) of training objects
    multilabel_classifier(peer_distances, peer_labels) - returns list of labels assigned to element for which 
        peer_distances is a vector of distances to training samples and peer_labels are multi-labels (list of lists) of training objects
        
    Returns multi-labels (list of lists) assigned to testing objects.
    """   
    predicted_labels = []
    for i,sample_ix in enumerate(xrange(0, len(testing2training_distances))):
        peer_distances = testing2training_distances[sample_ix]
        peer_labels = training_labels
        lvec = multilabel_classifier(peer_distances, peer_labels)
        #print sample_ix, " -> predicted:", lvec, " oracle:", oracle_labels[i]        
        predicted_labels.append(lvec)
    return predicted_labels
