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
    if len(sim_matrix.validate_similarity_matrix(matrix))>0: print "ERROR. invalid similarity values in ",name,"!"; sys.exit(-2)
    print "",name," of size ",len(matrix),"x",len(matrix[0])
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
            print "[ERROR] aggregate_simmatrix invalid output!"
            sys.exit(-2)
        

def __cpp_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix):
    msc2wids_list = get_msc2wids_list_primarymsc(msc2ix, mscmodel)
    dstmatrixpath = "/tmp/bmt_"+base64.b16encode(aux.quick_md5(sim_matrix_path+similarity_aggregator_method_l+str(MIN_COUNT_MSCPRIM)))
    if not aux.exists(dstmatrixpath):
        cpp_wrapper.aggregate_simmatrix(sim_matrix_path, dstmatrixpath, msc2wids_list, method=similarity_aggregator_method_l)
    logging.info("Loading simmatrix from "+str(dstmatrixpath))            
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

                
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    try:
        zbl_path = sys.argv[1]
    except:
        print "Argument expected: zbl-file-path."
        sys.exit(-1)
    try:
        sim_matrix_path = sys.argv[2]
    except:
        print "Argument exepected: similarity-matrix"
        sys.exit(-1)
        
    print "Framework that reconstructs msc-tree."
        
    print "--------------------------------------------------------"           
    print "Loading ZBL records from zbl_path=",zbl_path    
    zblid2zbl = dict( (zbl[zbl_io.ZBL_ID_FIELD],zbl) for zbl in _get_zbl_generator_(zbl_path) )
    print " zblid2zbl [",len(zblid2zbl),"docs loaded] =",str(list(zblid2zbl.iteritems()))[:100]
    
    print "--------------------------------------------------------"
    print "Building model MSC codes counts..."
    mscmodel = msc_processing.MscModel( zblid2zbl.values() )
    
    print "--------------------------------------------------------"
    print "Filtering msccodes with MIN_COUNT_MSC=",MIN_COUNT_MSC," MIN_COUNT_MSCPRIM=",MIN_COUNT_MSCPRIM," MIN_COUNT_MSCSEC=",MIN_COUNT_MSCSEC
    mscmodel.keep_msc_mincount(MIN_COUNT_MSC, MIN_COUNT_MSCPRIM, MIN_COUNT_MSCSEC)
    mscmodel.report()
    #store_mscgroups_primary(open("msc_groups.txt", "w"), mscmodel.mscprim2zblidlist)
    
    print "--------------------------------------------------------"
    print "Calculating msc2ix mapping..."
    msc2ix = dict((msc,ix) for ix,msc in enumerate(sorted(mscmodel.allcodes())))
    ix2msc = dict((ix,msc) for msc,ix in msc2ix.iteritems())
    msc_list = list( sorted(mscmodel.allcodes()) )    
    print " msc2ix=",str(list(msc2ix.iteritems()))[:100]             
            
    print "--------------------------------------------------------"
    print "Preparing similarity matrix on L-level..."
    #sim_matrix_l = __python_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix)
    sim_matrix_l = __cpp_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix)     
    __report_simmatrix_routine__("sim_matrix_l", sim_matrix_l)
    
    #if 1==1:
    #    if 1==1:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARN)
    lmclusters2ixs = {}
    for num_m_clusters in clusters_m_kvalues(len(msc2ix)):
        for num_l_clusters in clusters_l_kvalues(len(msc2ix)):
            if num_l_clusters<num_m_clusters: continue                    
            print "#############################################################################"
            print "CONSIDERING num_l_clusters=",num_l_clusters," num_m_clusters=",num_m_clusters
            clustering_l = lambda sim: clustering_l_k(sim, num_l_clusters) 
            clustering_m = lambda sim: clustering_m_k(sim, num_m_clusters)

            print "--------------------------------------------------------"    
            print "Building MSC tree out of", len(set(msc2ix.keys())), "leaves..."    
            msc_leaf2clusters, msc_tree = trees.build_msctree_leaf2clusters(msc2ix, msc2ix)
            
            #MSC
            #new_leaf2clusters, new_tree = msc_leaf2clusters, msc_tree
            
            #RAND
            #new_leaf2clusters, new_tree = random_tree.get_random_tree_leaf2clusters(msc2ix.values())
        
            #3level-tree
            new_leaf2clusters, new_tree = tree_clustering.generate_3level_tree(sim_matrix_l, clustering_l, similarity_aggregator_m, clustering_m)                 
                
            #UPGMA
            #new_tree = tree_clustering.generate_upgma_tree(sim_matrix_l, agreggation_method = 's')     
            #new_leaf2clusters = trees.bottomup2topdown_tree_converter(new_tree)
            
            print " new tree=",str(trees.map_tree_leaves(new_tree, ix2msc))[:400]
            
            print "--------------------------------------------------------"
            print "--------------------------------------------------------"
            print "Calculating similarity indexes..."
            comparision_result = tree_distance.get_indexes_dict(msc_leaf2clusters, new_leaf2clusters, \
                                                    bonding_calc, membership_calc, membership_bonding,\
                                                    only_fast_sim_calculations)
            print " *******************************************"
            print " comparision results=",comparision_result
            print _fo_(comparision_result.values())
            lmclusters2ixs[(num_l_clusters, num_m_clusters)] = comparision_result.values()
            
            #print "--------------------------------------------------------"
            #print "Calculating boding out of new tree..."
            #new_B = B_using_tree_l2c(new_leaf2clusters, bonding_calc)    
            #print "bonding=",str(new_B)[:200]
            #print " storing new_tree bonding matrix to",NEWTREE_BONDING_PATH
            #matrix_io.fwrite_smatrix(new_B, msc_list, msc_list, NEWTREE_BONDING_PATH)        

    print "############################################################################"
    print "Best configuration for simindex=0:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 0))
    print "Best configuration for simindex=1:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 1))
    print "Best configuration for simindex=2:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 2))
    print "Best configuration for simindex=3:",_fo_(_get_lm_for_max_simixs(lmclusters2ixs, 3))
 
    