"""Framework that reconstructs msc-tree."""
import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')
sys.path.append(r'../../../')

import random
import logging
import pickle
from math import sqrt 
import numpy
import time
import os.path
import base64


from tools import msc_processing
from tools.msc_processing import *
from tools import randomized
from tools.stats import *
from tools.randomized import *
from tools import cpp_wrapper
from tools import aux

from data_io import zbl_io
from data_io import matrix_io

import sim_matrix
from sim_aggregation import *
from sim_matrix import build_sparse_similiarity_matrix

import clustering 
from clustering import kmedoids
from clustering import upgma
from clustering import silhouettes
from clustering.silhouettes import *

import tree
from tree import trees
from trees import *
from tree import tree_distance
from tree.tree_distance import *
from tree import random_tree

import tree_clustering

from cfg import *

##############################################################################
##############################################################################
##############################################################################


def _get_zbl_generator_(zbl_path, must_have_field = 'mc'):
    """Returns zbl-records generator that has guaranteed presence of must_have_field field."""
    UNI = True #unic
    f = zbl_io.open_file(zbl_path, UNI)
    #return (zbl for zbl in zbl_io.read_zbl_records(f, UNI) if must_have_field in zbl)
    for ix,zbl in enumerate(zbl_io.read_zbl_records(f, UNI)): 
        if must_have_field in zbl:
            #zbl[zbl_io.ZBL_ID_FIELD] = ix #replacing ids with numbers for faster processing
            yield zbl
            
##############################################################################
##############################################################################
##############################################################################

                                        
def __report_simmatrix_routine__(name, matrix):
    if len(sim_matrix.validate_similarity_matrix(matrix))>0: print "[build_msc_tree] ERROR. invalid similarity values in ",name,"!"; sys.exit(-2)
    print "[build_msc_tree] ",name," of size ",len(matrix),"x",len(matrix[0])
    print str(numpy.array(matrix))[:500]
    
    


##############################################################################
##############################################################################
##############################################################################
    
def get_msc2wids_list_primarymsc(msc2ix, mscmodel):
    """Returns list of pairs (msc-code, list-of-weighted-ids-of-elements (pairs (ix,weight) ) )"""
    ix2msc   = dict((ix,msc) for msc,ix in msc2ix.iteritems())
    msc2wids_list = []
    for ix in xrange(len(ix2msc)):
        msc     = ix2msc[ix]
        wids    = list( (id,1.0) for id in mscmodel.mscprim2zblidlist[msc] )
        msc2wids_list.append( (msc, wids) )
    return msc2wids_list 

def ____validate_cpp_output____(msc2ix, rows):
    #validate output:
    ix2msc = dict( (ix,msc) for msc,ix in msc2ix.iteritems() )
    for ix,row in enumerate(rows):
        if not ix2msc[ix] == row:
            print "[build_msc_tree] [ERROR] aggregate_simmatrix invalid output!"
            sys.exit(-2)
        

def __cpp_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix):
    msc2wids_list = get_msc2wids_list_primarymsc(msc2ix, mscmodel)
    dstmatrixpath = TMPDIR+"/mlevel_similarity_matrix_"+similarity_aggregation_method_l+"_"+base64.b16encode(aux.quick_md5(sim_matrix_path+similarity_aggregation_method_l+str(MIN_COUNT_MSCPRIM)))
    if not aux.exists(dstmatrixpath):
        cpp_wrapper.aggregate_simmatrix(sim_matrix_path, dstmatrixpath, msc2wids_list, method=similarity_aggregation_method_l)
    logging.info("[build_msc_tree] Loading simmatrix from: "+str(dstmatrixpath))            
    (rows, cols, sim_matrix_l) = matrix_io.fread_smatrix(dstmatrixpath)
    ____validate_cpp_output____(msc2ix, rows)    
    return sim_matrix_l

##############################################################################
##############################################################################
##############################################################################

def _get_lm_for_max_simixs(lmclusters2ixs, simixno):
    maxval = max(simixs[simixno] for lm, simixs in lmclusters2ixs.iteritems())
    for lm, simixs in lmclusters2ixs.iteritems():
        if simixs[simixno] == maxval:
            return lm, simixs        
    return None

def _fo_(obj):
    return str(obj).replace(",","\t").replace(" ","")

        
##############################################################################
##############################################################################
##############################################################################        
                
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    try:
        zbl_path = sys.argv[1]
    except:
        print "[build_msc_tree] Argument expected: zbl-file-path."
        sys.exit(-1)
    try:
        sim_matrix_path = sys.argv[2]
    except:
        print "[build_msc_tree] Argument exepected: similarity-matrix"
        sys.exit(-1)
                 
    try:
        method = sys.argv[3]
        method_parts = method.split('-')
        tree_method = method_parts[0]
        
        try:
            similarity_aggregation_method_l = method_parts[1]
            similarity_aggregation_method_m = method_parts[2]
        except:
            pass        
    except:
        print "[build_msc_tree] Argument expected: method name"
        sys.exit(-1)
        
    #unify c==m
    if similarity_aggregation_method_l == 'c': similarity_aggregation_method_l = 'm'
    if similarity_aggregation_method_m == 'c': similarity_aggregation_method_m = 'm'
                    
    if      similarity_aggregation_method_m == 's':   similarity_aggregator_m = matrix_max
    elif    similarity_aggregation_method_m == 'm':   similarity_aggregator_m = matrix_min
    elif    similarity_aggregation_method_m == 'a':   similarity_aggregator_m = matrix_avg_U
    else:
        print "[build_msc_tree][Error] Uknown similarity_aggregator_m method!"
        sys.exit(-2)
          
    if similarity_aggregation_method_l!='s' and\
       similarity_aggregation_method_l!='a' and\
       similarity_aggregation_method_l!='m':
        print "[build_msc_tree][Error] Uknown similarity_aggregation_method_l method!"
        sys.exit(-2)              

                
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    print "[build_msc_tree] ============================================================================================================"        
    print "[build_msc_tree] Framework that reconstructs msc-tree."
    print "[build_msc_tree] *************************************"
    print "[build_msc_tree] MIN_COUNT_MSC =",MIN_COUNT_MSC
    print "[build_msc_tree] MIN_COUNT_MSCPRIM =",MIN_COUNT_MSCPRIM
    print "[build_msc_tree] MIN_COUNT_MSCSEC =",MIN_COUNT_MSCSEC
    print "[build_msc_tree] tree_method =", tree_method
    print "[build_msc_tree] similarity_aggregation_method_l =", similarity_aggregation_method_l
    print "[build_msc_tree] similarity_aggregation_method_m =", similarity_aggregation_method_m
    print "[build_msc_tree] similarity_aggregator_m =",similarity_aggregator_m    
    print "[build_msc_tree] *************************************"
        
    print "[build_msc_tree] ============================================================================================================"          
    print "[build_msc_tree] Loading ZBL records from zbl_path=",zbl_path    
    zblid2zbl = dict( (zbl[zbl_io.ZBL_ID_FIELD],zbl) for zbl in _get_zbl_generator_(zbl_path) )
    print "[build_msc_tree]  zblid2zbl [",len(zblid2zbl),"docs loaded] =",str(list(zblid2zbl.iteritems()))[:100]
    
    print "[build_msc_tree] --------------------------------------------------------"
    print "[build_msc_tree] Building model MSC codes counts..."
    mscmodel = msc_processing.MscModel( zblid2zbl.values() )
    
    print "[build_msc_tree] --------------------------------------------------------"
    print "[build_msc_tree] Filtering msccodes with MIN_COUNT_MSC=",MIN_COUNT_MSC," MIN_COUNT_MSCPRIM=",MIN_COUNT_MSCPRIM," MIN_COUNT_MSCSEC=",MIN_COUNT_MSCSEC
    mscmodel.keep_msc_mincount(MIN_COUNT_MSC, MIN_COUNT_MSCPRIM, MIN_COUNT_MSCSEC)
    mscmodel.report()
    #store_mscgroups_primary(open("msc_groups.txt", "w"), mscmodel.mscprim2zblidlist)
    
    print "[build_msc_tree] --------------------------------------------------------"
    print "[build_msc_tree] Calculating msc2ix mapping..."
    msc2ix = dict((msc,ix) for ix,msc in enumerate(sorted(mscmodel.allcodes())))
    ix2msc = dict((ix,msc) for msc,ix in msc2ix.iteritems())
    msc_list = list( sorted(mscmodel.allcodes()) )    
    print "[build_msc_tree]  msc2ix=",str(list(msc2ix.iteritems()))[:100]             
            
    print "[build_msc_tree] ============================================================================================================"
    print "[build_msc_tree] Preparing similarity matrix on L-level..."
    #sim_matrix_l = __python_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix)
    sim_matrix_l = __cpp_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix)     
    __report_simmatrix_routine__("sim_matrix_l", sim_matrix_l)
    
    print "[build_msc_tree] ============================================================================================================"
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARN)
    lmclusters2ixs = {}
    for num_m_clusters in clusters_m_kvalues(len(msc2ix)):
        for num_l_clusters in clusters_l_kvalues(len(msc2ix)):
            if num_l_clusters<num_m_clusters: continue                    
            print "[build_msc_tree] #############################################################################"
            print "[build_msc_tree] Considering num_l_clusters=",num_l_clusters," num_m_clusters=",num_m_clusters

            print "[build_msc_tree] --------------------------------------------------------"    
            print "[build_msc_tree] Building MSC tree out of", len(set(msc2ix.keys())), "leaves using tree_method=",tree_method    
            msc_leaf2clusters, msc_tree = trees.build_msctree_leaf2clusters(msc2ix, msc2ix)            
            if tree_method == "msc":
                new_leaf2clusters, new_tree = msc_leaf2clusters, msc_tree
            elif tree_method == "rand":            
                new_leaf2clusters, new_tree = random_tree.get_random_tree_leaf2clusters(msc2ix.values())
            elif tree_method == "3lupgma":
                clustering_l = lambda sim: upgma.upgma_clustering(sim, num_l_clusters, similarity_aggregation_method_m) 
                clustering_m = lambda sim: upgma.upgma_clustering(sim, num_m_clusters, similarity_aggregation_method_m)          
                new_leaf2clusters, new_tree = tree_clustering.generate_3level_tree(sim_matrix_l, clustering_l, similarity_aggregator_m, clustering_m)
            elif tree_method == "3lkmedoids":             
                clustering_l = lambda sim: kmedoids.kmedoids_clustering(sim, num_l_clusters)
                clustering_m = lambda sim: kmedoids.kmedoids_clustering(sim, num_m_clusters)
                new_leaf2clusters, new_tree = tree_clustering.generate_3level_tree(sim_matrix_l, clustering_l, similarity_aggregator_m, clustering_m)
            elif tree_method == "upgma":
                new_tree = tree_clustering.generate_upgma_tree(sim_matrix_l, similarity_aggregation_method_m)     
                new_leaf2clusters = trees.bottomup2topdown_tree_converter(new_tree)
            else:
                print "[build_msc_tree] [ERROR] Unknown method of building tree!"
                sys.exit(-4)            
            #print "[build_msc_tree]  new tree=",str(trees.map_tree_leaves(new_tree, ix2msc))
            
            print "[build_msc_tree] --------------------------------------------------------"
            print "[build_msc_tree] Calculating similarity indexes..."
            comparision_result = tree_distance.get_indexes_dict(msc_leaf2clusters, new_leaf2clusters, \
                                                    bonding_calc, membership_calc, membership_bonding,\
                                                    only_fast_sim_calculations)
            print "[build_msc_tree]  *******************************************"
            print "[build_msc_tree]  comparision results=",comparision_result
            print _fo_(comparision_result.values())
            lmclusters2ixs[(num_l_clusters, num_m_clusters)] = comparision_result.values()
            

    print "[build_msc_tree] ############################################################################"
    print "[build_msc_tree] Best configuration for simindex=0:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 0))
    print "[build_msc_tree] Best configuration for simindex=1:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 1))
    print "[build_msc_tree] Best configuration for simindex=2:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 2))
    print "[build_msc_tree] Best configuration for simindex=3:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 3))
            
    print "[build_msc_tree] ============================================================================================================"
    
    #print "[build_msc_tree] --------------------------------------------------------"
    #print "[build_msc_tree] Calculating boding out of new tree..."
    #new_B = B_using_tree_l2c(new_leaf2clusters, bonding_calc)    
    #print "[build_msc_tree] bonding=",str(new_B)[:200]
    #print "[build_msc_tree]  storing new_tree bonding matrix to",NEWTREE_BONDING_PATH
    #matrix_io.fwrite_smatrix(new_B, msc_list, msc_list, NEWTREE_BONDING_PATH)        
    