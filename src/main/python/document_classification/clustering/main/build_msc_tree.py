"""Framework that reconstructs msc-tree."""
import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')
sys.path.append(r'../../../')
from tools import msc_processing
from tools.msc_processing import *
from tools import randomized
from data_io import zbl_io
from data_io import matrix_io
import sim_matrix
import random
import logging
import pickle
from math import sqrt 
import numpy
from sim_aggregation import *
from tools.stats import *
from tools.randomized import *

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
from tree.random_tree import *


##l - low level, m - medium level, h - highest level of MSC tree

#CODES PREFILTERING:
MIN_COUNT_MSC = 0 #ile minimalnie dokumentow zeby zachowac klase
MIN_COUNT_MSCPRIM = 3
MIN_COUNT_MSCSEC = 0

#SAMPLING OF CODES REPRESENTATIONS:    
mscmsc_calculate_sample_size = lambda n: 100000 #ile par dokument x dokument dla kazdego z msc x msc    

#CLUSTERING:
similarity_aggregator_l = avg #should work on list
similarity_aggregator_m = matrix_avg_U #should work on matrix
clustering_l = lambda sim: kmedoids.kmedoids_clustering(sim, sqrt(len(sim))+1, 100) 
clustering_m = lambda sim: kmedoids.kmedoids_clustering(sim, sqrt(len(sim))+1, 100) 
        
#SIMILARITY CACLULATIONS:    
bonding_calc = lambda common_levels: common_levels/3.0
membership_calc = lambda common_levels: common_levels/2.0
membership_bonding = angular_bonding
only_fast_calculations = True 


def _get_zbl_generator_(zbl_path, must_have_field = 'mc'):
    """Returns zbl-records generator that has guaranteed presence of must_have_field field."""
    UNI = True #unic
    f = zbl_io.open_file(zbl_path, UNI)
    #return (zbl for zbl in zbl_io.read_zbl_records(f, UNI) if must_have_field in zbl)
    for ix,zbl in enumerate(zbl_io.read_zbl_records(f, UNI)): 
        if must_have_field in zbl:
            #zbl[zbl_io.ZBL_ID_FIELD] = ix #replacing ids with numbers for faster processing
            yield zbl
    

                            
            
def __report_simmatrix_routine__(name, matrix):
    if len(sim_matrix.validate_similarity_matrix(matrix))>0: print "ERROR. invalid similarity values in ",name,"!"; sys.exit(-2)
    print "",name," of size ",len(matrix),"x",len(matrix[0])
    print str(numpy.array(matrix))[:500]
    
    
def __generate_trees_routine___(msc2ix, assignment_l, assignment_m, ):            
    msc_tree = trees.build_msctree(msc2ix.keys(), msc2ix)
    msc_leaf2clusters = trees.bottomup2topdown_tree_converter(msc_tree)
    new_tree = trees.build_3level_tree(assignment_l, assignment_m)
    new_leaf2clusters = trees.bottomup2topdown_tree_converter(new_tree)
    rand_tree = get_random_tree(msc2ix.values())    
    rand_leaf2clusters = trees.bottomup2topdown_tree_converter(rand_tree)
    
    ix2msc = dict((ix,msc) for msc,ix in msc2ix.iteritems())
    print " msc2ix=",str(msc2ix)[:200]
    print " msc_tree=",str(trees.map_tree_leaves(msc_tree, ix2msc))[:200]
    print " new_tree=",str(trees.map_tree_leaves(new_tree, ix2msc))[:200]
    print " rand_tree=",str(trees.map_tree_leaves(rand_tree, ix2msc))[:200]
            
    return msc_leaf2clusters, new_leaf2clusters, rand_leaf2clusters


def __calc_simindexes_routine__(msc_leaf2clusters, new_leaf2clusters, rand_leaf2clusters):
    self_comparision = tree_distance.get_indexes_dict(msc_leaf2clusters, msc_leaf2clusters, \
                                            bonding_calc, membership_calc, membership_bonding,\
                                            only_fast_calculations)
    new_comparision = tree_distance.get_indexes_dict(msc_leaf2clusters, new_leaf2clusters, \
                                            bonding_calc, membership_calc, membership_bonding,\
                                            only_fast_calculations)
    rand_comparision = tree_distance.get_indexes_dict(msc_leaf2clusters, rand_leaf2clusters, \
                                            bonding_calc, membership_calc, membership_bonding,\
                                            only_fast_calculations)
    return self_comparision,new_comparision,rand_comparision
 
            
        
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
        
        
    print "--------------------------------------------------------"           
    print "Loading ZBL records from zbl_path=",zbl_path    
    zblid2zbl = dict( (zbl[zbl_io.ZBL_ID_FIELD],zbl) for zbl in _get_zbl_generator_(zbl_path) )
    print " zblid2zbl=",str(list(zblid2zbl.iteritems()))[:100]
    
    print "--------------------------------------------------------"
    print "Building model MSC codes counts..."
    mscmodel = msc_processing.MscModel( zblid2zbl.values() )
    
    print "--------------------------------------------------------"
    print "Filtering msccodes with MIN_COUNT_MSC=",MIN_COUNT_MSC," MIN_COUNT_MSCPRIM=",MIN_COUNT_MSCPRIM," MIN_COUNT_MSCSEC=",MIN_COUNT_MSCSEC
    mscmodel.keep_msc_mincount(MIN_COUNT_MSC, MIN_COUNT_MSCPRIM, MIN_COUNT_MSCSEC)
    mscmodel.report()
    
    print "--------------------------------------------------------"
    print "Calculating msc2ix mapping..."
    msc2ix = dict((msc,ix) for ix,msc in enumerate(mscmodel.allcodes()))    
    print " msc2ix=",str(list(msc2ix.iteritems()))[:100] 
        
    print "--------------------------------------------------------"
    print "Loading sim_matrix_p from sim_matrix_path=",sim_matrix_path
    if sim_matrix_path.endswith(".pickle"):
        (rows, cols, sim_matrix_p) = pickle.load(open(sim_matrix_path))
    else:
        (rows, cols, sim_matrix_p) = matrix_io.fread_smatrix_L(sim_matrix_path) #, datareader=matrix_io.__read_ftabs__, maxrows=1000
        print " pickling to=",(sim_matrix_path+".pickle")
        pickle.dump((rows, cols, sim_matrix_p), open(sim_matrix_path+".pickle", "wb"))    
    print "","matrix of size=",len(rows),"x",len(cols),"loaded:",str(sim_matrix_p[:10])[:100]
    if len(sim_matrix.validate_similarity_matrix(sim_matrix_p))>0: print "ERROR. invalid elements in sim_matrix_p!"; sys.exit(-2)
    zblid2simix = dict( (label,ix) for ix,label in enumerate(rows) )
    print " zblid2simix=", str(list(zblid2simix.iteritems()))[:100] 
    #metoda liczenia odleglosci miedzy dwoma dokumentami:
    def doc2doc_similarity_calculator(zbl1, zbl2):        
        zblid1, zblid2 = zbl1[zbl_io.ZBL_ID_FIELD], zbl2[zbl_io.ZBL_ID_FIELD]
        #logging.info("[doc2doc_similarity_calculator] comparing "+str(zblid1)+" vs. "+str(zblid2)) 
        ix1,ix2 = zblid2simix[zblid1],zblid2simix[zblid2]
        #print "[doc2doc_similarity_calculator] ix1,ix2=",ix1,ix2
        return sim_matrix_p[max(ix1,ix2)][min(ix1,ix2)]
    
    print "--------------------------------------------------------"
    print "Preparing similarity matrix on L-level ..."
    sim_matrix_l = matrix_io.create_matrix(mscmodel.N(), mscmodel.N(), value = 0.0)
    matrix_io.set_diagonal(sim_matrix_l, sim_matrix.MAX_SIMILARITY_VALUE)
    
    print "--------------------------------------------------------"
    print "Building similarity matrix on L-level (aggregator:",similarity_aggregator_l,")..."
    for (msc1,msc2),zbl_ids_pairs in mscmsc2sampleids_generator(mscmodel.mscprim2count.keys(), mscmodel.mscprim2zblidlist, mscmsc_calculate_sample_size):        
        mscix1, mscix2 = msc2ix[msc1], msc2ix[msc2]         
        zbl2zbl_sim_submatrix  = sim_matrix.build_sparse_similiarity_matrix(zblid2zbl, zbl_ids_pairs, doc2doc_similarity_calculator)                        
        sim_matrix_l[mscix1][mscix2] = sim_matrix_l[mscix2][mscix1] = similarity_aggregator_l(zbl2zbl_sim_submatrix.values())
        #logging.info("[build_mscmsc_sim]"+str((msc1,msc2))+":"+str(list(zbl2zbl_sim_submatrix.iteritems()))[:100]+ " -> "+str(sim_matrix_l[mscix1][mscix2]) )                 
    __report_simmatrix_routine__("sim_matrix_l", sim_matrix_l)
            
    print "--------------------------------------------------------"
    print "Clustering L-level (xxyzz) (method:",str(clustering_l),")..."
    assignment_l = clustering_l(sim_matrix_l)
    print "\tassignment_l = ",str(assignment_l)[:200]        
    
    print "--------------------------------------------------------"
    print "Aggregating similarity matrix on M-level (aggregator:",str(similarity_aggregator_m),")..."
    sim_matrix_m = sim_matrix.aggregate_similarity_matrix_a(sim_matrix_l, assignment_l, similarity_aggregator_m)
    __report_simmatrix_routine__("sim_matrix_m", sim_matrix_m)

    print "--------------------------------------------------------"
    print "Clustering M-level (xxy) (method:",str(clustering_m),")..."
    assignment_m = clustering_m(sim_matrix_m)
    print "\tassignment_m = ",str(assignment_m)[:200]    
        
    print "--------------------------------------------------------"
    print "--------------------------------------------------------"    
    print "Building MSC tree(s) out of", len(set(msc2ix.keys())), "leaves"
    msc_leaf2clusters, new_leaf2clusters, rand_leaf2clusters = __generate_trees_routine___(msc2ix, assignment_l, assignment_m)        
    
    print "--------------------------------------------------------"
    print "--------------------------------------------------------"
    print "Calculating similarity indexes..."
    self_comparision,new_comparision,rand_comparision = \
    __calc_simindexes_routine__(msc_leaf2clusters, new_leaf2clusters, rand_leaf2clusters)
    print " *******************************************"
    print " self_comparision indexes=",self_comparision
    print " new_comparision=",new_comparision
    print " rand_comparision=",rand_comparision
 
    
    
    
    