"""Tools that use randomization."""
import random

def yield_cartesian_product(list1, list2):
    """Yields pairs where first element is from list1 and second from list2."""
    for e1 in list1:
        for e2 in list2:
            yield (e1, e2)
            
def sample_cartesian_product(list1, list2, sample_size_calculator = lambda nd: nd/10):
    """Returns subsample of max size=sample_size_calculator(|list1xlist2|) list1xlist2"""
    pairs = list(yield_cartesian_product(list1, list2))
    random.shuffle(pairs)
    #print "[sample_cartesian_product] pairs", str(pairs)[:100] 
    return pairs[:sample_size_calculator(len(pairs))]


def sample_cartesian_product_lm(list1, list2, calculate_sample_size = lambda nd: nd/10):
    """Returns random subset (list of pairs) of size=calculate_sample_size(|list1|*|list2|) of list1 x list2.
    
    Version that uses low memory.
    """
    num_possible_pairs = len(list1) * len(list2)
    chosen_pairs_ixs = random.sample(xrange(num_possible_pairs), calculate_sample_size(num_possible_pairs))            
    chosen_pairs = list( (list1[ distance_ix/len(list2) ], list2[ distance_ix%len(list2) ]) for distance_ix in chosen_pairs_ixs)
    return chosen_pairs


def randomly_divide(how_many, test_size):
    """
    Consider random subset as training, and the rest as testing. 
    O(nlogn) time on my side, because the random.sample returns unsorted list.
    
    Manually Tested.
    """
    test = sorted(random.sample(range(how_many), test_size)) #O(nlogn)
    train = []
    #print "test:", test
    elem = 0
    tst_ind = 0
    while elem<how_many and tst_ind<len(test):#linear time
        tst_elem = test[tst_ind]
        #print "elem, tst_elem", elem, tst_elem
        tst_ind+=1
        #print "tst_elem", tst_elem
        while elem<tst_elem:
            train.append(elem)
            elem+=1    
        if elem==tst_elem:
            elem+=1
    
    while elem<how_many:
        train.append(elem)
        elem+=1
    
    return train, test 
