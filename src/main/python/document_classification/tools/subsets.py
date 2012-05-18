'''
Created on Dec 1, 2011

@author: mlukasik
'''
import itertools

def findallsubsets(S):
    """
    Finds all subsets of a given set S
    
    """
    return reduce(lambda x, y: x+y, [findsubsets(S, m) for m in xrange(1, len(S)+1)])
        
def findsubsets(S,m):
    """
    Finds all subsets of a given set S, of size m
    
    """
    s = set(itertools.combinations(S, m))
    return map(lambda x: list(x), list(s))
    
