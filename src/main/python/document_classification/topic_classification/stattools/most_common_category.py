'''
Created on Nov 24, 2011

@author: mlukasik
'''
from collections import defaultdict

def extract_most_common_categ(frecords):
    """
    Finds most common category code amongst frecords
    
    frecords - iterable, where each element is a 2-element tuple:
            -first element is a numerical feature vector
            -second element is a list of labels
    """
    d = defaultdict(lambda: 0)
    for rec in frecords:
        for cat in rec[1]:
            d[cat]+=1

    return max(d.iteritems(), key=lambda x: x[1])

