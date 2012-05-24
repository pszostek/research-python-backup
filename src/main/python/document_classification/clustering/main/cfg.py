
import sys,os
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
mscmsc_calculate_sample_size = lambda n: 100000 #ile par dokument x dokument dla kazdego z msc x msc    

#CLUSTERING:
similarity_aggregator_method_l = "avg" #cpp version: avg/sl/avgw
similarity_aggregator_m = matrix_avg_U #should work on matrix
#clustering_l = lambda sim: kmedoids.kmedoids_clustering(sim, 30, 10000) 
#clustering_m = lambda sim: kmedoids.kmedoids_clustering(sim, 10, 10000) 
#clustering_l = lambda sim: upgma.upgma_clustering(sim, sqrt((len(sim)/2+1)), agreggation_method = 'a') 
#clustering_m = lambda sim: upgma.upgma_clustering(sim, sqrt((len(sim)/2+1)), agreggation_method = 'a') 
clustering_l = lambda sim: upgma.upgma_clustering(sim, 30, agreggation_method = 'a') 
clustering_m = lambda sim: upgma.upgma_clustering(sim, 50, agreggation_method = 'a') 
#SIMILARITY CACLULATIONS:    
bonding_calc = lambda common_levels: common_levels
membership_calc = lambda common_levels: common_levels/2.0
membership_bonding = angular_bonding
only_fast_sim_calculations = True 


NEWTREE_BONDING_PATH = "/tmp/newtree_bonding.txt"


            