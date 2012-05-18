'''
Created on Jan 5, 2012

@author: mlukasik
'''
from __future__ import division
import numpy, math
def cosine_distance(u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """
    return 1 - (numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v))))