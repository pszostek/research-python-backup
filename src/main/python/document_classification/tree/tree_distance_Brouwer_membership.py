"""Brouwer 2009 membership methods."""
import trees
import logging
import itertools
from itertools import izip
import logging
from math import sqrt
from math import acos
from math import pi

from tree_distance_common import *
from tree_membership import * 

#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#Brouwer 2009:

def norm(v):
    return sqrt( sum(e*e for e in v) )

def cos(vi,vj):
    num = sum(ei*ej for ei,ej in izip(vi,vj)) 
    den = norm(vi) * norm(vj)
    #return (float(num)/den+1.0)/2.0
    return float(num)/den

def angular_distance(vi,vj):
    cosv = cos(vi,vj)
    if cosv>1.0 and cosv<1.00001: cosv = 1.0 #because of numeric stability        
    return 2.0 * acos(cosv) / pi
          
def angular_bonding(vi,vj):
    return 1.0 - angular_distance(vi,vj)


#####################################################################################
#####################################################################################
        

def B_using_membership(M, membership_bonding = angular_bonding ):
    """Calculates bonding matrix B using membership matrix M .
    
    n - number of elements
    m - number of clusters
    M - nxm matrix (list of lists) i-th (i \in [0,n-1]) 
        row is interpreted as membership vector 
        (how much i-th element belong to every cluster)        
    B - nxn matrix (list of lists) that says how much two elements are bonded
    membership_bonding(vi,vj) - takes two membership vectors (lists) and returns bonding value  
    """
    B = []
    for rowix,vi in enumerate(M):
        #print "[B_using_membership] row:",rowix,"/",len(M)
        B.append( list( membership_bonding(vi,vj) for vj in M ) )         
    return B

#####################################################################################


def Brouwer_membership_B1B2(leaf2clusters_1, leaf2clusters_2, \
                            membership_calc = lambda common_levels: common_levels, \
                            membership_bonding = angular_bonding): 
    """Returns tuple B1,B2,leaf2ix where: B1,B2 - bonding matrices for two trees, leaf2ix - dictionary{leaf: index}.
    
    Trees are converted to fuzzy clusters using membership_calc and then bonding is calculated using b.
    Trees are given as a dictionary {leaf: descending-list-of-clusters}.
    For details of:
     membership_calc - see: M_dictionary_l2c
     membership_bonding - see: B_using_membership
    """    
    leaf2clusters_1, leaf2clusters_2, leaf2ix  = trees_prefiltering(leaf2clusters_1, leaf2clusters_2)
    logging.info("[Brouwer_membership_B1B2] leaf2ix = "+str(leaf2ix)[:200])
        
    def calc_bonding(leaf2clusters):
        
        #print "[Brouwer_membership_B1B2] calc M_dict"
        M_dict  = M_dictionary_l2c(leaf2clusters, membership_calc)
        logging.info("[Brouwer_membership_B1B2] M_dict = "+str(M_dict)[:200])

        #print "[Brouwer_membership_B1B2] convert M_dict to M"                    
        M       = M_dictionary2matrix(M_dict, leaf2ix)    
        
        #print "[Brouwer_membership_B1B2] calc B using M = ",len(M),"x",len(M[0])
        B       = B_using_membership(M, membership_bonding)
        return B
    
    #print "[Brouwer_membership_B1B2] calc B1 bonding"
    B1 = calc_bonding(leaf2clusters_1)
    logging.info("[Brouwer_membership_B1B2] B1 = "+str(B1)[:200])
    
    #print "[Brouwer_membership_B1B2] calc B2 bonding"
    B2 = calc_bonding(leaf2clusters_2)
    logging.info("[Brouwer_membership_B1B2] B2 = "+str(B2)[:200])
    
    return B1,B2, leaf2ix
            
if __name__=="__main__":
      
    import doctest
    doctest.testmod()    