"""A bunch of functions for calculating different mathematical measures."""

import math

def avg(lst):
    """Calculates average of elements from the list."""
    return sum(lst)/float(len(lst))

def avgmin(lst, fraction=0.05):
    """Calculates average of fraction of min elements."""
    return avg( sorted(lst)[:int(round(len(lst)*fraction))] )

def avgmax(lst, fraction=0.05):
    """Calculates average of fraction of max elements."""
    return avg( sorted(lst)[-int(round(len(lst)*fraction)):] )


def std(lst):
    """Calculates standard deviation with Bessel's correction."""
    mi = avg(lst)
    return math.sqrt(1.0/(len(lst)-1.0)  * sum( (x-mi)*(x-mi) for x in lst ) )

def hist(lst):
    """Returns dictionary {value: count}"""
    h = {}
    for e in lst:
        h[e] = h.get(e, 0)+1
    return h


def wrongly_classified_fraction(count, selected_count):
    """Calculates fraction of wrongly classified in node."""
    return 1.0/sum(count) * (sum(count) - selected_count) 

def wrongly_classified_fraction_max(count):
    """Calculates fraction of wrongly classified in node.
       Assumption: label = most often represented group. 
    """
    return wrongly_classified_fraction(count, max(count))

def wrongly_classified(count, selected_count):
    """Calculates number of wrongly classified elements in a node."""
    return sum(count)-selected_count
 


def gini_index(count):
    """Calculates gini index of a node."""
    n = float(sum(count))
    return sum( (c/n*(1-c/n) for c in count) ) 

def entropy(count):
    """Calculates entropy of a node."""
    n = float(sum(count))
    return -sum( c/n * math.log(c/n,2) for c in count )  


