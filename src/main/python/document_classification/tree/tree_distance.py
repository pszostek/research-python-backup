"""Main file of tree-distances implementation."""
import trees
import logging
import itertools
from itertools import izip
import logging

from tree_distance_Brouwer_membership import *
from tree_distance_Brouwer_treestructure import *    
from tree_distance_Campello_membership import * 
import simindexes
from simindexes import *


def get_indexes_report(leaf2clusters, leaf2clusters2, \
                       bonding_calc, membership_calc, membership_bonding,\
                       only_fast_calculations = False):
    """Returns values of several similarity indexes calculated for two trees."""
    Bf_RI= Bf_ARI= Bf_JI= Bm_RI= Bm_ARI= Bm_JI= C_RI= C_ARI= C_JI= Hm_RI= Hf_RI= Bt_RI = -1.0
        
    ####################################################################
    logging.info("[get_indexes_report] ======================================")    
    logging.info("[get_indexes_report] Brouwer_treestructure_B1B2")
             
    B1,B2,leaf2ix = Brouwer_treestructure_B1B2(leaf2clusters, leaf2clusters2, \
                                               bonding_calc)
    #import numpy
    #print "B1_tree_structure:\n",numpy.array(B1)
    #print "B2_tree_structure:\n",numpy.array(B2)
    (a,b,c,d) = Brouwer_abcd(B1, B2)
    #print "Brouwer (path fraction bonding) a,b,c,d:",a,b,c,d
    Bf_RI, Bf_ARI, Bf_JI = simindexes.calc_base_indexes(a,b,c,d)
            
    ####################################################################
    logging.info("[get_indexes_report] ======================================")
    logging.info("[get_indexes_report] Hullermeier path")
    
    #print "Hullermeier"
    Hf_RI = HRI(leaf2clusters, leaf2clusters2, bonding_calc)
    #return Bf_RI, Bf_ARI, Bf_JI, Bm_RI, Bm_ARI, Bm_JI, C_RI, C_ARI, C_JI, Hm_RI, Hf_RI, Bt_RI
    ####################################################################
    if only_fast_calculations:
        return Bf_RI, Bf_ARI, Bf_JI, Bm_RI, Bm_ARI, Bm_JI, C_RI, C_ARI, C_JI, Hm_RI, Hf_RI, Bt_RI        
    ####################################################################
    logging.info("[get_indexes_report] ======================================")
    logging.info("[get_indexes_report] Hullermeier membership")    
    Hm_RI = HRI_membership(leaf2clusters, leaf2clusters2, \
                                          membership_calc, membership_bonding)     

    ####################################################################
    ####################################################################
    logging.info("[get_indexes_report] ======================================")
    logging.info("[get_indexes_report] Brouwer_treestructure_tau=min")            
                
    a,b,c,d = Brouwer_abcd(B1, B2, \
                 complement_calc = complement, \
                 aggregation_calc = lambda b1,b2: pairwise_aggregation(b1,b2, tau=min), \
                 matrix2scalar_calc = h)   
    #print "Brouwer (path fraction bonding -> min) a,b,c,d:",a,b,c,d
    Bt_RI = ((a+d) / (len(leaf2ix)*(len(leaf2ix)-1)/2))
    # print " numapairs->",len(leaf2ix)*(len(leaf2ix)-1)/2
    # simindexes.report_indexes(a,b,c,d)
    ####################################################################
    logging.info("[get_indexes_report] ======================================")
    logging.info("[get_indexes_report] Brouwer_membership_B1B2")
    
    #M_dict = M_dictionary(T, membership_calc)
    #M      = M_dictionary2matrix(M_dict, leaf2ix)
    #print "M_dict(Tree1)",M_dict
    #print "M(Tree1)",M    
    
    B1,B2, leaf2ix = Brouwer_membership_B1B2(leaf2clusters, leaf2clusters2, \
                                             membership_calc, membership_bonding)
    #import numpy
    #print "B1_membership:\n",numpy.array(B1)
    #print "B2_membership:\n",numpy.array(B2)
    (a,b,c,d) = Brouwer_abcd(B1, B2, \
                     complement_calc = complement, \
                     aggregation_calc = pairwise_aggregation, \
                     matrix2scalar_calc = h)
    #print "Brouwer (membership -> cos) a,b,c,d:",a,b,c,d
    Bm_RI, Bm_ARI, Bm_JI = simindexes.calc_base_indexes(a,b,c,d)
    ####################################################################
    return Bf_RI, Bf_ARI, Bf_JI, Bm_RI, Bm_ARI, Bm_JI, C_RI, C_ARI, C_JI, Hm_RI, Hf_RI, Bt_RI        
    ####################################################################
    logging.info("[get_indexes_report] ======================================")
    logging.info("[get_indexes_report] Campello_VXYZ")

    (V,X,Y,Z),leaf2ix = Campello_VXYZ(leaf2clusters, leaf2clusters2,
                                      membership_calc, max, min)
    (a,b,c,d) = Campello_abcd(V,X,Y,Z, \
                              aggregation_calc = pairwise_aggregation, \
                              matrix2scalar_calc = h)
    #print "Campello (membership -> cos) a,b,c,d:",a,b,c,d
    C_RI, C_ARI, C_JI = simindexes.calc_base_indexes(a,b,c,d)
    ####################################################################
    ####################################################################
    
    return Bf_RI, Bf_ARI, Bf_JI, Bm_RI, Bm_ARI, Bm_JI, C_RI, C_ARI, C_JI, Hm_RI, Hf_RI, Bt_RI



def get_indexes_dict(leaf2clusters, leaf2clusters2,\
                     bonding_calc, membership_calc, membership_bonding,\
                     only_fast_calculations = False):
    """Returns dictionary{similarity-index-name: index-value}."""
    Bf_RI, Bf_ARI, Bf_JI, Bm_RI, Bm_ARI, Bm_JI, C_RI, C_ARI, C_JI, Hm_RI, Hf_RI, Bt_RI = get_indexes_report(leaf2clusters, leaf2clusters2, bonding_calc, membership_calc, membership_bonding, only_fast_calculations)    
    d = {'Bf_RI':Bf_RI, 'Bf_ARI':Bf_ARI, 'Bf_JI':Bf_JI, 'Bm_RI':Bm_RI, 'Bm_ARI':Bm_ARI, 'Bm_JI':Bm_JI, 'C_RI':C_RI, 'C_ARI':C_ARI, 'C_JI':C_JI, 'Hm_RI':Hm_RI, 'Hf_RI':Hf_RI, 'Bt_RI':Bt_RI}
    d = dict( (k,v) for k,v in d.iteritems() if v>=0.0)
    return d

         
def _comparision_report_(T,T2):
    """Prints comparsion results for two trees: T and T2."""
    print "------------------------------------------------------"
    print "Tree1:",T
    print "Tree2:",T2

    bonding_calc = lambda common_levels: common_levels/3.0
    membership_calc = lambda common_levels: common_levels/2.0
    membership_bonding = angular_bonding
    
    leaf2clusters = trees.bottomup2topdown_tree_converter(T)
    leaf2clusters2 = trees.bottomup2topdown_tree_converter(T2)
    
    indexes_dict = get_indexes_dict(leaf2clusters, leaf2clusters2, bonding_calc, membership_calc, membership_bonding)
    print indexes_dict
    
    ####################################################
    print "Multilabelling example:---------------"
    M1 = [[0.67,0.67,0.33,0.33,0.67,0.00],
          [0.33,0.33,0.67,0.67,0.33,0.00],
          [0.00,0.00,0.00,0.00,0.00,0.67]]
    B1 = B_using_membership(M1)

    M2 = [[0.33,0.67,0.33,0.00,0.00,0.00],
          [0.33,0.33,0.67,0.67,0.33,0.00],
          [0.00,0.00,0.00,0.33,0.67,0.67]]
    B2 = B_using_membership(M2)

    M3 = [[0.33,0.67,0.67,0.33,0.33,0.00],
          [0.33,0.33,0.67,0.67,0.33,0.00],
          [0.00,0.00,0.00,0.33,0.67,0.67]]
    B3 = B_using_membership(M3)
    
    print "HRI(M1,M2)",(1.0-H_distance(B1,B2))
    print "HRI(M2,M3)",(1.0-H_distance(B2,B3))
    print "HRI(M1,M3)",(1.0-H_distance(B1,B3))

    
if __name__=="__main__":
      
    import doctest
    doctest.testmod()
  
    T = [[['a','b','c'],['d','e'],['f']],[['g']]]
    T_X1 = [[['a','b'],['c','d','e'],['f']],[['g']]]
    T_X2 = [[['a','b','c'],['d','e','f']],[['g']]]
    T_X12 = [[['a','b'],['c','d','e','f']],[['g']]]
    T_X3 = [[['a','b','c'],['d','e'],['f','g']]]
    T_X4 = [[['a','b','c'],['d','e','g'],['f']]]

    #T2 = [[['a','b','c'],['d','e'],['f','f2']],[['g','h','i'],['j','k'],['l','l2']]]
    #T3 = [[['a','b','c','c2'],['d','e','e2'],['f','f2']],[['g','h','i','i2'],['j','k','k2'],['l','l2']]]   
        
        
    _comparision_report_(T,T)
    #_comparision_report_([T[0],[['g']]],[T[0],[['g']]])
    #_comparision_report_([T[0]],[T[0],[['g']]])    
    #_comparision_report_(T2,T2)
    #_comparision_report_(T3,T3)
    
    _comparision_report_(T, T_X2)
    _comparision_report_(T, T_X1)
    _comparision_report_(T, T_X12)
    _comparision_report_(T, T_X3)
    _comparision_report_(T, T_X4)
    