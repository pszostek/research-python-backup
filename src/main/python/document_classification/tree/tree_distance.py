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




def get_selected_indexes(leaf2clusters, leaf2clusters2,\
                         selected_indexes,\
                         bonding_calc=None, membership_calc=None, membership_bonding=None):
    """Returns values of selected similarity indexes (e.g. Hf-ARI, Bf-JI,...) calculated for two trees: leaf2clusters, leaf2clusters2.
    
    bonding_calc, membership_calc, membership_bonding - indexes' parameters
    """
    if len( set(leaf2clusters.keys()).intersection(set(leaf2clusters2.keys())) ) == 0:
        raise Exception("[get_selected_indexes][EXCEPTION] Two trees have totally different leaves!")

    selected_indexes = set(selected_indexes)
    index2value = {}
    
    #print "[get_selected_indexes] = ",selected_indexes
    
    ###############################################################################################################################

    if "Bf-RI" in selected_indexes or "Bf-ARI" in selected_indexes or "Bf-JI" in selected_indexes or "Hf-ARI" in selected_indexes:     
        B1,B2,leaf2ix = Brouwer_treestructure_B1B2(leaf2clusters, leaf2clusters2, \
                                                   bonding_calc)

    if "Bf-RI" in selected_indexes or "Bf-ARI" in selected_indexes or "Bf-JI" in selected_indexes:     
        (a,b,c,d) = Brouwer_abcd(B1, B2, \
                     complement_calc = complement, \
                     aggregation_calc = lambda M1,M2: pairwise_aggregation(M1,M2, tau=lambda m1,m2: m1*m2), \
                     matrix2scalar_calc = hsum)  
        Bf_RI, Bf_ARI, Bf_JI    = simindexes.calc_base_indexes(a,b,c,d)
        index2value["Bf-RI"]    = Bf_RI
        index2value["Bf-ARI"]   = Bf_ARI
        index2value["Bf-JI"]    = Bf_JI
                    
    if "Hf-ARI" in selected_indexes:     
        (a,b,c,d) = Brouwer_abcd(B1, B2, \
                     complement_calc = complement, \
                     aggregation_calc = lambda M1,M2: pairwise_aggregation(M1,M2, tau=lambda m1,m2: min(m1,m2)), \
                     matrix2scalar_calc = hsum)  
        Hf_RI, Hf_ARI, Hf_JI    = simindexes.calc_base_indexes(a,b,c,d)
        index2value["Hf-ARI"]   = Hf_ARI
        
    ###############################################################################################################################
        
    if "Hf-RI" in selected_indexes:    
        index2value["Hf-RI"]    = HRI(leaf2clusters, leaf2clusters2, bonding_calc)
        #a,b,c,d = Brouwer_abcd(B1, B2, \
        #         complement_calc = complement, \
        #         aggregation_calc = lambda b1,b2: pairwise_aggregation(b1,b2, tau=min), \
        #         matrix2scalar_calc = hsum)       
        #Hf_RI = ((a+d) / (len(leaf2ix)*(len(leaf2ix)-1)/2))
        
    ###############################################################################################################################

    if "Hm-RI" in selected_indexes:    
        index2value["Hm-RI"]    = HRI_membership(leaf2clusters, leaf2clusters2, membership_calc, membership_bonding)     

    ###############################################################################################################################
    
    if "Bm-RI" in selected_indexes or "Bm-ARI" in selected_indexes or "Bm-JI" in selected_indexes:
        B1,B2, leaf2ix = Brouwer_membership_B1B2(leaf2clusters, leaf2clusters2, \
                                                 membership_calc, membership_bonding)
        (a,b,c,d) = Brouwer_abcd(B1, B2, \
                         complement_calc = complement, \
                         aggregation_calc = pairwise_aggregation, \
                         matrix2scalar_calc = hsum)    
        Bm_RI, Bm_ARI, Bm_JI = simindexes.calc_base_indexes(a,b,c,d)
        index2value["Bm-RI"]    = Bm_RI
        index2value["Bm-ARI"]   = Bm_ARI
        index2value["Bm-JI"]    = Bm_JI
    
    ###############################################################################################################################
    
    if "C-RI" in selected_indexes or "C-ARI" in selected_indexes or "C-JI" in selected_indexes:    
        (V,X,Y,Z),leaf2ix = Campello_VXYZ(leaf2clusters, leaf2clusters2,
                                          membership_calc, max, min)
        (a,b,c,d) = Campello_abcd(V,X,Y,Z, \
                                  aggregation_calc = pairwise_aggregation, \
                                  matrix2scalar_calc = hsum)        
        C_RI, C_ARI, C_JI = simindexes.calc_base_indexes(a,b,c,d)
        index2value["C-RI"]    = C_RI
        index2value["C-ARI"]   = C_ARI
        index2value["C-JI"]    = C_JI
    
    ###############################################################################################################################

    return index2value
    
    

def get_indexes_dict(leaf2clusters, leaf2clusters2,\
                     bonding_calc, membership_calc, membership_bonding,\
                     only_fast_calculations = False):
    """Returns dictionary{similarity-index-name: index-value}. 
    
    For details see: get_selected_indexes
    """
    if only_fast_calculations:
        selected_indexes = ["Bf-RI", "Bf-ARI", "Bf-JI", "Hf-ARI", "Hf-RI"]
    else:
        selected_indexes = ["Bf-RI", "Bf-ARI", "Bf-JI", "Hf-ARI", "Hf-RI", "Hm-RI", "Bm-RI", "Bm-ARI", "Bm-JI", "C-RI", "C-ARI", "C-JI"]
    return  get_selected_indexes(leaf2clusters, leaf2clusters2, selected_indexes, bonding_calc, membership_calc,membership_bonding)

         
def _comparision_report_(T,T2):
    """Prints comparsion results for two trees: T and T2."""
    print "------------------------------------------------------"
    print "Tree1:",T
    print "Tree2:",T2

    bonding_calc = lambda common_path_fraction: common_path_fraction
    membership_calc = lambda common_levels: common_levels/2.0
    membership_bonding = angular_bonding
    
    leaf2clusters = trees.bottomup2topdown_tree_converter(T)
    leaf2clusters2 = trees.bottomup2topdown_tree_converter(T2)
    
    indexes_dict = get_indexes_dict(leaf2clusters, leaf2clusters2, bonding_calc, membership_calc, membership_bonding, False)
    print indexes_dict
    
    ####################################################
    return
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
    
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

  
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

    
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    T = [ [['a']], [['b']], [['c']], [['d']],[['e'],['f']], [['g', 'h'],['i', 'j']], [['k','l'],['m'],['n','o','p']] ]
    T_1 = [ [['a']], [['b']], [['c']], [['d']],[['e']],[['f']], [['g', 'h'],['i', 'j']], [['k','l']],[['m']],[['n','o','p']] ]
    T_2 = [ [['a']], [['b']], [['c']], [['d']],[['e'],['f']], [['g', 'h']],[['i', 'j']], [['k','l']],[['m']],[['n','o','p']] ]
    T_3 = [ [['a']], [['b']], [['c']], [['d']],[['e']], [['f']], [['g']], [['h']],[['i']], [['j']], [['k']],[['l']],[['m']],[['n']],[['o']],[['p']] ]
    
    
    _comparision_report_(T, T)
    _comparision_report_(T, T_1)
    _comparision_report_(T, T_2)
    _comparision_report_(T, T_3)
    
    
    T = [ [['a']], [['b']], [['c']], [['d']],[['e'],['f']], [['g', 'h'],['i', 'j']], [['k','l'],['m'],['n','o','p']] , [['x1','x2'],['x3'],['x4','x5','x6']] ]
    T_1 = [ [['a']], [['b']], [['c']], [['d']],[['e']],[['f']], [['g', 'h'],['i', 'j']], [['k','l']],[['m']],[['n','o','p']], [['x1','x2']],[['x3']],[['x4','x5','x6']] ]
    T_2 = [ [['a']], [['b']], [['c']], [['d']],[['e'],['f']], [['g', 'h']],[['i', 'j']], [['k','l']],[['m']],[['n','o','p']], [['x1','x2']],[['x3']],[['x4','x5','x6']] ]
    T_3 = [ [['a']], [['b']], [['c']], [['d']],[['e']], [['f']], [['g']], [['h']],[['i']], [['j']], [['k']],[['l']],[['m']],[['n']],[['o']],[['p']], [['x1','x2']],[['x3']],[['x4','x5','x6']] ]

    _comparision_report_(T, T)
    _comparision_report_(T, T_1)
    _comparision_report_(T, T_2)
    _comparision_report_(T, T_3)
    
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
