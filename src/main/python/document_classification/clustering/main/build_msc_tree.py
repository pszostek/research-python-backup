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
    
def get_msc2wids_list(msc2ix, mscmodel, secondary_weight = 0.0, secondary_constant_weight = True):
    """Returns list of pairs (msc-code, list-of-weighted-ids-of-elements (pairs (ix,weight) ) ).
    
    Secondary codes have weight that can be either constant or .
    """
    ix2msc        = dict((ix,msc) for msc,ix in msc2ix.iteritems())    
    id2seccodes  = mscmodel.doc2seccodes()
    msc2wids_list = []
    for ix in xrange(len(ix2msc)): #sort with ix = 0,1,2...
        msc         = ix2msc[ix]
        wids_prim   = list( (id,1.0) for id in mscmodel.mscprim2zblidlist.get(msc,[]) )        
        if secondary_weight<=0.0:
            wids_sec = []
        elif secondary_constant_weight == True:
            wids_sec    = list( (id,secondary_weight) for id in mscmodel.mscsec2zblidlist.get(msc,[]) )
        else:            
            wids_sec    = list( (id,secondary_weight/len(id2seccodes[id])) for id in mscmodel.mscsec2zblidlist.get(msc,[]) )
        msc2wids_list.append( (msc, wids_prim+wids_sec) )
    return msc2wids_list 


def ____validate_cpp_output____(msc2ix, rows):
    #validate output:
    ix2msc = dict( (ix,msc) for msc,ix in msc2ix.iteritems() )
    for ix,row in enumerate(rows):
        if not ix2msc[ix] == row:
            print "[build_msc_tree] [ERROR] aggregate_simmatrix invalid output!"
            sys.exit(-2)
        

def __cpp_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix):
    #dstmatrixpath = TMPDIR+"/mlevel_similarity_matrix_"+similarity_aggregation_method_l+"_"+base64.b16encode(aux.quick_md5(sim_matrix_path+similarity_aggregation_method_l+str(MIN_COUNT_MSCPRIM)))
    dstmatrixpath = sim_matrix_path+".msc"+str(MIN_COUNT_MSCPRIM)+"_"+similarity_aggregation_method_l
    if not aux.exists(dstmatrixpath):
        msc2wids_list = get_msc2wids_list(msc2ix, mscmodel, 0.5, False)
        cpp_wrapper.aggregate_simmatrix(sim_matrix_path, dstmatrixpath, msc2wids_list, method=similarity_aggregation_method_l)
    logging.info("[build_msc_tree] Loading simmatrix from: "+str(dstmatrixpath))            
    (rows, cols, sim_matrix_l) = matrix_io.fread_smatrix(dstmatrixpath)
    ____validate_cpp_output____(msc2ix, rows)    
    return sim_matrix_l

##############################################################################
##############################################################################
##############################################################################

def _get_lm_for_max_simixs(lmclusters2ixs, simixno):
    (maxval,lm) = max( (simixs[simixno],lm) for lm, simixs in lmclusters2ixs.iteritems())
    return lm        
    

def _fo_(obj):
    return str(obj).replace(",","\t").replace(" ","")

        
##############################################################################
##############################################################################
##############################################################################        
                
    
if __name__ == "__main__":
    argv = sys.argv
    
    sys.stderr = sys.stdout
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    try:
        zbl_path = argv[1]
    except:
        print "[build_msc_tree] Argument expected: zbl-file-path."
        sys.exit(-1)
    try:
        sim_matrix_path = argv[2]
    except:
        print "[build_msc_tree] Argument exepected: similarity-matrix"
        sys.exit(-1)
                 
    try:
        method = argv[3]
        method_parts = method.split('-')
        clustering_method = method_parts[0]
        
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
    print "[build_msc_tree] clustering_method =", clustering_method
    print "[build_msc_tree] similarity_aggregation_method_l =", similarity_aggregation_method_l
    print "[build_msc_tree] similarity_aggregation_method_m =", similarity_aggregation_method_m
    print "[build_msc_tree] similarity_aggregator_m =",similarity_aggregator_m    
    print "[build_msc_tree] numiterations =",numiterations 
    print "[build_msc_tree] l_clusters_range =",str(l_clusters_range)[:100],"..."
    print "[build_msc_tree] m_clusters_range =",str(m_clusters_range)[:100],"..."
    print "[build_msc_tree] *************************************"
        
    print "[build_msc_tree] ============================================================================================================"          
    print "[build_msc_tree] Loading ZBL records from zbl_path=",zbl_path    
    zblid2zbl = dict( (zbl[zbl_io.ZBL_ID_FIELD],zbl) for zbl in _get_zbl_generator_(zbl_path) )
    print "[build_msc_tree]  zblid2zbl [",len(zblid2zbl),"docs loaded] =",str(list(zblid2zbl.iteritems()))[:100]


    print "[build_msc_tree] --------------------------------------------------------"
    print "[build_msc_tree] Building model MSC codes counts..."
    mscmodel = msc_processing.MscModel( zblid2zbl.values() )
    mscmodel.report()
    
    print "[build_msc_tree] --------------------------------------------------------"
    print "[build_msc_tree] Filtering msccodes with MIN_COUNT_MSC=",MIN_COUNT_MSC," MIN_COUNT_MSCPRIM=",MIN_COUNT_MSCPRIM," MIN_COUNT_MSCSEC=",MIN_COUNT_MSCSEC
    mscmodel.keep_msc_mincount(MIN_COUNT_MSC, MIN_COUNT_MSCPRIM, MIN_COUNT_MSCSEC)
    mscmodel.report()
    #print "[build_msc_tree] mscmodel.allcodes()=", mscmodel.allcodes() 
    #store_mscgroups_primary(open("msc_groups.txt", "w"), mscmodel.mscprim2zblidlist)
    
    print "[build_msc_tree] --------------------------------------------------------"
    print "[build_msc_tree] Calculating msc2ix mapping..."
    msc2ix = dict((msc,ix) for ix,msc in enumerate(sorted(mscmodel.allcodes())))
    ix2msc = dict((ix,msc) for msc,ix in msc2ix.iteritems())
    msc_list = list( sorted(mscmodel.allcodes()) )    
    print "[build_msc_tree]  msc2ix[of length",len(msc2ix),"]=",str(list(msc2ix.iteritems()))[:100]             
            
    print "[build_msc_tree] ============================================================================================================"
    print "[build_msc_tree] Preparing similarity matrix on L-level..."
    #sim_matrix_l = __python_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix)
    sim_matrix_l = __cpp_sim_matrix_l_generation_routine__(sim_matrix_path, mscmodel, msc2ix)     
    __report_simmatrix_routine__("sim_matrix_l", sim_matrix_l)
    
    print "[build_msc_tree] ============================================================================================================"
    print "[build_msc_tree] Building pattern-tree..."
    msc_leaf2clusters, msc_tree = trees.build_msctree_leaf2clusters(msc2ix, msc2ix)
     
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.WARN)
    if clustering_method != "3lkmedoids": numiterations = 1 #fix parameters which don't influence
    if clustering_method == "msc" or clustering_method == "rand" or clustering_method == "upgma": 
        m_clusters_range,l_clusters_range = [1],[1]        
        
    lm2avgixs,lm2stdixs = {},{}     
    for m_clusters in m_clusters_range:
        for l_clusters in l_clusters_range:
            if l_clusters<m_clusters or l_clusters>len(sim_matrix_l) or m_clusters>len(sim_matrix_l): continue
            
            iteration_results = []
            for iterno in xrange(numiterations):                                
                print "[build_msc_tree] --------------------------------------------------------"    
                print "[build_msc_tree] Building MSC tree out of", len(set(msc2ix.keys())), "leaves using clustering_method=",clustering_method
                print "[build_msc_tree] [start] iteration=",iterno," l_clusters=",l_clusters," m_clusters=",m_clusters                                   
                if clustering_method == "msc":
                    new_leaf2clusters, new_tree = msc_leaf2clusters, msc_tree
                elif clustering_method == "rand":            
                    new_leaf2clusters, new_tree = random_tree.get_random_tree_leaf2clusters(msc2ix.values())
                elif clustering_method == "3lupgma":
                    clustering_l = lambda sim: upgma.upgma_clustering(sim, l_clusters, similarity_aggregation_method_m) 
                    clustering_m = lambda sim: upgma.upgma_clustering(sim, m_clusters, similarity_aggregation_method_m)          
                    new_leaf2clusters, new_tree = tree_clustering.generate_3level_tree(sim_matrix_l, clustering_l, similarity_aggregator_m, clustering_m)
                elif clustering_method == "3lkmedoids":             
                    clustering_l = lambda sim: kmedoids.kmedoids_clustering(sim, l_clusters, 10000)
                    clustering_m = lambda sim: kmedoids.kmedoids_clustering(sim, m_clusters, 10000)
                    new_leaf2clusters, new_tree = tree_clustering.generate_3level_tree(sim_matrix_l, clustering_l, similarity_aggregator_m, clustering_m)
                elif clustering_method == "upgma":
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
                print "[build_msc_tree] [end] iteration=",iterno," l_clusters=",l_clusters," m_clusters=",m_clusters," comparision_result=",comparision_result
                iteration_results.append(comparision_result)                                
            lm2avgixs[(l_clusters, m_clusters)] = stats.avg_lstdict(iteration_results)                
            lm2stdixs[(l_clusters, m_clusters)] = stats.std_lstdict(iteration_results)   
            
    print "[build_msc_tree] ============================================================================================================"
    print "[build_msc_tree] lm2avgixs=",lm2avgixs
    print "[build_msc_tree] lm2stdixs=",lm2stdixs
    all_supported_indexes = aux.extract_keys(lm2avgixs.values())
    best_values_stats = {}
    for index_name in all_supported_indexes:             
        lm = _get_lm_for_max_simixs(lm2avgixs, index_name)
        best_values_stats[index_name] = (lm, lm2avgixs[lm][index_name], lm2stdixs[lm][index_name])
        #print "[build_msc_tree] Best configuration for simindex =",index_name,"\tlm =",lm,"\tvalue =",lm2avgixs[lm][index_name],"\tstd =",lm2stdixs[lm][index_name]
    print "[build_msc_tree] -------------------------"
    print "[build_msc_tree] [RESULTS] method =", method," zbl =",os.path.basename(zbl_path)," simmatrix =",os.path.basename(sim_matrix_path)," => ", best_values_stats
    #print "[build_msc_tree] best_values_stats =", _fo_(best_values_stats.values())
            
    print "[build_msc_tree] ============================================================================================================"
    
    #print "[build_msc_tree] --------------------------------------------------------"
    #print "[build_msc_tree] Calculating boding out of new tree..."
    #new_B = B_using_tree_l2c(new_leaf2clusters, bonding_calc)    
    #print "[build_msc_tree] bonding=",str(new_B)[:200]
    #print "[build_msc_tree]  storing new_tree bonding matrix to",NEWTREE_BONDING_PATH
    #matrix_io.fwrite_smatrix(new_B, msc_list, msc_list, NEWTREE_BONDING_PATH)        
        