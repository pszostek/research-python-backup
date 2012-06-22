""" Indexes designed to measure similarity."""

import trees
import logging
import itertools
from itertools import izip

from tree_distance_common import * 
from tree_distance_Brouwer_membership import *
from tree_distance_Brouwer_treestructure import *    
from tree_distance_Campello_membership import * 


#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#Hullermeier:

def H_distance(B1,B2):
    """H [Eyke Hullermeier] distance."""
    n = len(B1)    
    Theta = pairwise_aggregation(B1,B2,lambda b1,b2: abs(b1-b2))    
    return float( h(Theta) ) / ( n*(n-1)/2.0 )
        
def HRI(leaf2clusters_1, leaf2clusters_2, \
        bonding_calc = lambda common_levels: common_levels):
    """H [Eyke Hullermeier] Rand Index."""    
    B1 = B_using_tree_l2c(leaf2clusters_1, bonding_calc)
    B2 = B_using_tree_l2c(leaf2clusters_2, bonding_calc)
    return 1.0 - H_distance(B1,B2) 
    
def HRI_membership(leaf2clusters_1, leaf2clusters_2, \
                   membership_calc = lambda common_levels: common_levels, \
                   membership_bonding = angular_bonding):
    """H [Eyke Hullermeier] Rand Index.""" 
    B1,B2, leaf2ix = Brouwer_membership_B1B2(leaf2clusters_1, leaf2clusters_2, \
                                    membership_calc, membership_bonding)                                                                
    return 1.0 - H_distance(B1,B2)
    #return 1.0     

#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
        
def Brouwer_abcd(B1, B2, \
                 complement_calc = complement, \
                 aggregation_calc = pairwise_aggregation, \
                 matrix2scalar_calc = h):
    """Calculates tuple (a,b,c,d) using Brouwer[2009] formulas.
    
    B1,B2 - two bonding matrices (lists of lists).
    Matrices' size is NxN where N = number of samples.
    """    
    
    cB1 = complement_calc(B1)
    cB2 = complement_calc(B2)
    
    M1 = aggregation_calc(B1, B2)
    M2 = aggregation_calc(cB1, B2)
    M3 = aggregation_calc(B1, cB2)
    M4 = aggregation_calc(cB1, cB2)
        
    a = matrix2scalar_calc( M1 )
    b = matrix2scalar_calc( M2 )
    c = matrix2scalar_calc( M3 )
    d = matrix2scalar_calc( M4 )
    logging.info("[Brouwer_abcd] a="+str(a)+" b="+str(b)+" c="+str(c)+" d="+str(d))    
    return (a,b,c,d)

def Campello_abcd(V,X,Y,Z, \
                  aggregation_calc = lambda A,B: pairwise_aggregation(A,B,min),\
                  matrix2scalar_calc = h):
    """Calculates tuple (a,b,c,d) using Campello[2006] formulas.
    
    V,X,Y,Z - matrices describing bonding.
    Matrices' size is NxN where N = number of samples.
    """
    a = matrix2scalar_calc( aggregation_calc(V, Y) )
    b = matrix2scalar_calc( aggregation_calc(X, Y) )
    c = matrix2scalar_calc( aggregation_calc(V, Z) )
    d = matrix2scalar_calc( aggregation_calc(X, Z) )
    logging.info("[Campello_abcd] a="+str(a)+" b="+str(b)+" c="+str(c)+" d="+str(d))
    return (a,b,c,d)


#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################




def RandIndex(a,b,c,d):
    """Calculates Rand Index."""
    return float(a+d)/(a+b+c+d)

def JaccardIndex(a,b,c,d=0):
    """Calculates Jaccard coefficient."""
    return float(a)/(a+b+c)

def ARI(a,b,c,d):
    """Calculates Adjusted Rand Index using formula [Brouwer 2009]:
    
    $$ ARI2 = \frac{2(ad-bc)}{c^2+b^2+2ad+(a+d)(c+b)} \in [-1,1] $$
    $$ ARI(C,C') = \frac{ARI2+1}{2} \in [0,1] $$ 
    """    
    ARI2 = 2.0*(a*d - b*c) / (c*c + b*b + 2.0*a*d + (a+d)*(c+b))
    return (ARI2+1.0)/2.0

def ARI_Campello(a,b,c,d): 
    """Calculates Adjusted Rand Index using formula from [Campello 2006].
    
    """
    top = a-(float(a+c)*(a+b))/d
    bottom = ((a+c)+(a+b))/2.0 - (float(a+c)*(a+b))/d
    return top/bottom

def report_indexes(a,b,c,d):
    """Prints out values of several indexes."""
    print "RI:", "%.3f" % RandIndex(a,b,c,d)
    print "ARI:", "%.3f" % ARI(a,b,c,d)
    print "JI:", "%.3f" % JaccardIndex(a,b,c,d)
    #print "ARI_Campello:", "%.3f" % ARI_Campello(a,b,c,d)

def calc_base_indexes(a,b,c,d):
    """Returns touple that contains values of several indexes."""
    return RandIndex(a,b,c,d), ARI(a,b,c,d), JaccardIndex(a,b,c,d)

