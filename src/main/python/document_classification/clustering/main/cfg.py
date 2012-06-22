"""Configuration file for build_nsc_tree script."""

import sys,os
import tempfile   
sys.path.append(r'../')
sys.path.append(r'../../')
sys.path.append(r'../../../')

import trees
from sim_aggregation import *
from tree import trees
from trees import *
from tree import tree_distance
from tree.tree_distance import *

import upgma
import kmedoids


##Tree levels: l - low level, m - medium level, h - highest level of MSC tree

#CODES PREFILTERING:
MIN_COUNT_MSC = 0 #ile minimalnie dokumentow zeby zachowac klase
MIN_COUNT_MSCPRIM = 10
MIN_COUNT_MSCSEC = 0

#SAMPLING OF CODES REPRESENTATIONS:    
mscmsc_calculate_sample_size = lambda n: 100000 #ile maksymalnie par dokument x dokument dla kazdego z msc x msc    

#CLUSTERING:
clustering_method = "3lupgma"
similarity_aggregation_method_l = "a"   #cpp version: a/s/avgw/m
secondary_codes_weight = 0.0            #weight for secondary codes: default no secondary codes
secondary_weight_method = 'e'
similarity_aggregation_method_m = "a" 

numiterations = 3
#m_clusters_range = [4,10,100,150,300,400]  
#l_clusters_range = [4,10,100,150,300,400] 
m_clusters_range = [2]#range(10,10000,10)
l_clusters_range = [4]#range(10,10000,10)

#SIMILARITY CACLULATIONS:    
bonding_calc = lambda common_levels_fraction: common_levels_fraction
membership_calc = lambda common_levels: common_levels/2.0
membership_bonding = angular_bonding
similarity_indexes = ["Hf-ARI"] 


TMPDIR = tempfile.gettempdir();
NEWTREE_BONDING_PATH = TMPDIR+"/newtree_bonding.txt"


