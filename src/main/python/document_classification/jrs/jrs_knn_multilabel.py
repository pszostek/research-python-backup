'''
Created on Mar 8, 2012

knn_multilabel is the main method here.
'''
import sys
sys.path.append(r'../')
sys.path.append(r'../../')

from mlknn import find_closest_points

def PRINTER(x):
    print x
    #pass

def jrs_find_closest_points(distances, records, k):
    """
    Returns indices of nearest neighbours.
        
    distances - vector of distances to other samples (list)
    labels - labels of other samples (list of lists)
    k - k-nn parameter
    records - which indices are to be considered from distances
    
    """ 
    
    #records = xrange(len(distances))
    excluding = []
    distance = lambda x, source: distances[x]
    return find_closest_points.find_closest_points(None, records, excluding, k, distance)
    
def knn_repetitions_multilabel(distances, records, labels, k):
    """
    Returns labels of nearest neighbours. If repetitions of labels occur, these repetitions also
    occur in the resulting list.
        
    distances - vector of distances to other samples (list)
    labels - labels of other samples (list of lists)
    k - k-nn parameter
    records - which indices are to be considered from distances
    
    """ 
    
    closest_points = jrs_find_closest_points(distances, records, k)
    #print "[knn_repetitions_multilabel] closest_points:", closest_points
    chosen_labels = reduce(lambda x, y: x+y, [labels[closest_p] for closest_p in closest_points])
    return chosen_labels
    
def count_distinct_objects(objects):
    from collections import defaultdict
    counts = defaultdict(lambda: 0)
    for label in objects:
        counts[label] += 1
    return dict(counts)
    
def knn_multilabel(distances, records, labels, k, labels_count):
    """
    Returns labels of nearest neighbours. Create a ranking of labels, according to number of their
    occurences in the neighbourhood. Take labels_count number of first labels from the ranking.
        
    distances - vector of distances to other samples (list)
    labels - labels of other samples (list of lists)
    k - k-nn parameter
    labels_count - number of labels that are to be returned.
    records - which indices are to be considered from distances
    
    """ 
    
    chosen_labels_repetitions = knn_repetitions_multilabel(distances, records, labels, k)
    #PRINTER("chosen_labels_repetitions: "+str(chosen_labels_repetitions))
    #build a counter of each label:
    counts = count_distinct_objects(chosen_labels_repetitions)
    #PRINTER("counts: "+str(counts))
    #create a sorted list labels, according to counts:
    chosen_labels_counted = sorted(counts.iteritems(), key=lambda x: x[1], reverse=True)
    #PRINTER("chosen_labels_counted: "+str(chosen_labels_counted))
    #extract the keys only
    chosen_labels = map(lambda x: x[0], chosen_labels_counted)
    #PRINTER("chosen_labels: "+str(chosen_labels))
    return chosen_labels[:labels_count]
    
def knn_fraction_multilabel(distances, records, labels, k, min_occurence):
    """
    Returns labels of nearest neighbours. Return labels that occur at least min_occurence times.
        
    distances - vector of distances to other samples (list)
    labels - labels of other samples (list of lists)
    k - k-nn parameter
    min_occurence - minimum occurence of a label to return it.
    records - which indices are to be considered from distances
    """ 
    
    chosen_labels_repetitions = knn_repetitions_multilabel(distances, records, labels, k)
    counts = count_distinct_objects(chosen_labels_repetitions)
    result = []
    for label, count in counts.iteritems():
        if count >= min_occurence:
            result.append(label)
    PRINTER("chosen_labels: "+str(result))
    return result


def get_counts2labels(counts):
    """
    Reversed the dictionary -> puts values into keys, and groups the keys into list
    """
    from collections import defaultdict
    counts2labels = defaultdict(lambda: [])
    for key, count in counts.iteritems():
        counts2labels[count].append(key)
    return counts2labels
    
def knn_multilabel_halfbayesian(distances, records, labels, k, labels_count, label_global_counts):
    """
    Returns labels of nearest neighbours. Create a ranking of labels, according to 
    the following number: 
    number of occurences in the neighbourhood * Number of occurences . Take labels_count number of first labels from the ranking.
        
    distances - vector of distances to other samples (list)
    labels - labels of other samples (list of lists)
    k - k-nn parameter
    label_global_counts - counts of labels in the training set
    labels_count - number of labels that are to be returned.
    records - which indices are to be considered from distances
    """ 
    
    chosen_labels_repetitions = knn_repetitions_multilabel(distances, records, labels, k)
    #build a counter of each label:
    counts = count_distinct_objects(chosen_labels_repetitions)
    #reverse_counts = 
    #create a sorted list labels, according to counts:
    #chosen_labels_counted = sorted(counts.iteritems(), key=lambda x: x[1], reverse=True)
    counts2labels = get_counts2labels(counts)
    chosen_labels_counted = sorted(counts2labels.iteritems(), key=lambda x: x[0], reverse=True)
    
    #print "chosen_labels_counted:", chosen_labels_counted
    result = []
    
    #for counts key:
    for sub_labels in chosen_labels_counted:
        #PRINTER("considering: "+str(sub_labels))
        #extract labels that have this count:
        curr_labels = sub_labels[1]
        #PRINTER("curr_labels: "+str(curr_labels))
        
        #sort it according to label_global_counts
        curr_labels = sorted(curr_labels, key=lambda x: label_global_counts[x], reverse=True)
        #PRINTER("curr_labels sorted: "+str(curr_labels))
        result = result+curr_labels
        #PRINTER("result: "+str(result))
    
    #extract the keys only
    return result[:labels_count]

if __name__ == "__main__":
    
    #distances = [1, 5, 3, 7, 9, 1]
    #distances2 = [5, 2, 3, 3, 1, 14]
    distances = [1, 2, 1, 2]
    distances2 = [2, 1, 2, 1]
    labels = [['A', 'B'], ['C', 'D'], ['A', 'C'], ['B', 'D']]
    frequency_dict = {'A':4, 'B':1, 'C':100, 'D':9}# 'F':3, 'H':0}
    #labels = [['A', 'B', 'D'], ['D', 'B', 'F'], ['F', 'B'], ['B'], ['H'], ['C']]
    #labels = [['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['A', 'B', 'D'], ['H'], ['A', 'B', 'D']]
    k = 2
    
    #print knn_multilabel_halfbayesian(distances, labels, k, 2, frequency_dict)
    #print knn_multilabel_halfbayesian(distances2, labels, k ,2, frequency_dict)
    print knn_fraction_multilabel(distances, xrange(len(distances)), labels, k, 2)
    print knn_fraction_multilabel(distances2, xrange(len(distances2)), labels, k, 2)
    #print knn_multilabel_halfbayesian(distances, labels, k, 3, {'A':4, 'B':1, 'C':100, 'D':9, 'F':3, 'H':0})