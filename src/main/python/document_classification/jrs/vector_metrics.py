from itertools import izip
from math import sqrt

def dot_product(x,y):
    return sum(xi*yi for xi,yi in izip(x,y))

def vector_len(x):
    return sqrt(sum(xi*xi for xi in x))

def cosine_dist(x,y):
    return 1.0 - dot_product(x,y) / ( vector_len(x) * vector_len(y) )

def euclid2_dist(x,y):
    return sum((xi-yi)*(xi-yi) for xi,yi in izip(x,y))