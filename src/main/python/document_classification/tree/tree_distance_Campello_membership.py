"""Campello 2006 methods"""

import trees
import logging
import itertools
from itertools import izip
import logging

from tree_distance_common import *
from tree_membership import *

#####################################################################################
#####################################################################################
#####################################################################################
#####################################################################################
#Campello 2007:

def _Campello_simmatrix(M, cotau, tau2):
    simmatrix = []
    for vi in M:
        row = []        
        for vj in M:
            row.append( cotau( tau2(vi_k, vj_k) for vi_k, vj_k in izip(vi, vj) ) )
        simmatrix.append(row)
    return simmatrix

def _Campello_dissimmatrix(M, cotau, tau2):
    numclusters = len(M[0])
    clusters = range(numclusters)
    
    dismatrix = []    
    for vi in M:
        row = []        
        for vj in M:
            
            pairs_tau2 = []
            for k in clusters:
                for n in clusters:
                    if n == k: continue
                    pairs_tau2.append( tau2(vi[k], vj[n]) )
            row.append( cotau(pairs_tau2) )
                    
        dismatrix.append(row)            
    return dismatrix

def Campello_membership_VXYZ(M1, M2, cotau = max, tau2 = min):
    """Calculates Campello2007 V,X,Y,Z using membership matricies M1, M2."""
    #print "[Campello_membership_VXYZ] calculating V"
    V = _Campello_simmatrix(M1, cotau, tau2)
    #print "[Campello_membership_VXYZ] calculating X"
    X = _Campello_dissimmatrix(M1, cotau, tau2)
    #print "[Campello_membership_VXYZ] calculating Y"
    Y = _Campello_simmatrix(M2, cotau, tau2)
    #print "[Campello_membership_VXYZ] calculating Z"
    Z = _Campello_dissimmatrix(M2, cotau, tau2)       
    return V,X,Y,Z    
    

def Campello_VXYZ(leaf2clusters_1, leaf2clusters_2, \
                  membership_calc = lambda common_levels: common_levels, \
                  cotau = max, tau2 = min): 
    """Calculates Campello2007 V,X,Y,Z for trees."""
    leaf2clusters_1, leaf2clusters_2, leaf2ix  = trees_prefiltering(leaf2clusters_1, leaf2clusters_2)
        
    M_dict          = M_dictionary_l2c(leaf2clusters_1, membership_calc)
    M1              = M_dictionary2matrix(M_dict, leaf2ix)    
    M_dict          = M_dictionary_l2c(leaf2clusters_2, membership_calc)
    M2              = M_dictionary2matrix(M_dict, leaf2ix)

    V,X,Y,Z = Campello_membership_VXYZ(M1, M2, cotau, tau2)

    #import numpy
    #print "[Campello_VXYZ] M1:\n",numpy.array(M1)
    #print "[Campello_VXYZ] M2:\n",numpy.array(M2)
    #print "[Campello_VXYZ] V:\n",numpy.array(V)
    #print "[Campello_VXYZ] X:\n",numpy.array(X)
    #print "[Campello_VXYZ] Y:\n",numpy.array(Y)
    #print "[Campello_VXYZ] Z:\n",numpy.array(Z)

    return (V,X,Y,Z), leaf2ix

