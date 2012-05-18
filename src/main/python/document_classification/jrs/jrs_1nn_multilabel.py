

def nn1_multilabel(peer_distances, peer_labels):
    """Returns list of labels of its' closest neighbour."""
    return peer_labels[peer_distances.index(min(peer_distances))]