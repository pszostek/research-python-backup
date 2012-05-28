'''
Created on May 21, 2012

@author: mlukasik
'''
from __future__ import division
from itertools import izip

import math
import sys
sys.path.append(r'../')
from tools.stop_words_list import STOP_WORDS_LIST
from tools.text_to_words import text_to_words

def get_key2vals_txt(s, fkey=int, fval=float):
    '''
    s is a string of a form: 'num1: val1      ,       num2: val2 ,       numk: valk ,       ... '
    extract a dictionary of a form: {num1:val1, ...}, mapping each value to float
    
    fkey is a function mapping string to a type of a key
    
    fval is a function mapping string to a type of a val
    
    '''
    ls = s.split(',')#List-S
    ls_pairs = [elem.split(':') for elem in ls]
    d = {}
    for k, v in ls_pairs:
        d[fkey(k)] = fval(v)
    return d

def get_dict_size(dx):
    '''
    Calculates ||dx|| for the cosine distance.
    '''
    return math.sqrt(sum([ val*val for val in dx.itervalues() ]))

def dot_product(dx, dy):
    '''
    Calculates dot product of 2 given vectors in the form of dictionaries (indices are keys).
    '''
    keys_dx = set(dx.keys())
    keys_dy = set(dy.keys())
    all_keys = keys_dx | keys_dy
    #print "[dot_product] all_keys:", all_keys
    dot_prod = 0
    for key in all_keys:
        dot_prod += dx.get(key, 0)*dy.get(key, 0)
    return dot_prod
    

class TxtCosineDistance(object):
    """
    Encapsulates distance calculations between Zbl records.
    
    Calculates a distance between 2 objects based on the counts field, 
    which reflects the number of occurences of each word in the documents.
    
    ------------
    """
    def __init__(self, fieldname):# = 'g0'):
        """
        Train weights and shifts.
        
        """
        self.fieldname = fieldname
    
    def distance(self, x, y):
        """
        Calculates distance between records: x and y.
        
        """
        #print "x[self.fieldname]:", x[self.fieldname]
        #print "y[self.fieldname]:", y[self.fieldname]
        
        dx = get_key2vals_txt(x[self.fieldname])
        dy = get_key2vals_txt(y[self.fieldname])
        
        dxSize = get_dict_size(dx)
        dySize = get_dict_size(dy)
        
        dot_prod = dot_product(dx, dy)
        
        return 1-dot_prod/(dxSize*dySize)