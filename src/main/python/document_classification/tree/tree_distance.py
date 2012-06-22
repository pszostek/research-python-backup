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
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    bonding_calc = lambda common_path_fraction: common_path_fraction
    membership_calc = lambda common_levels: common_levels/2.0
    membership_bonding = angular_bonding
        
    msc_str = [[[u'42B20', u'42B25']], [[u'60E15'], [u'60G15', u'60G07', u'60G40', u'60G42', u'60G44', u'60G48', u'60G60', u'60G17', u'60G57', u'60G51', u'60G50'], [u'60F05', u'60F17', u'60F15', u'60F10'], [u'60B05', u'60B10', u'60B15'], [u'60H07', u'60H05', u'60H99', u'60H15', u'60H10', u'60H20'], [u'60K40', u'60K35', u'60K37', u'60K25'], [u'60J60', u'60J65', u'60J25', u'60J35', u'60J45', u'60J10', u'60J55', u'60J80']], [[u'68Q45', u'68Q65', u'68Q60', u'68Q55', u'68Q80', u'68Q10', u'68Q15', u'68Q42', u'68Q05', u'68Q25', u'68Q70'], [u'68R10', u'68R15']], [[u'62G07', u'62G05', u'62G10'], [u'62E20'], [u'62H25', u'62H30'], [u'62M05']], [[u'35G10'], [u'35A20', u'35A27'], [u'35D10', u'35D05'], [u'35B25', u'35B27', u'35B65', u'35B40', u'35B05', u'35B45'], [u'35L05', u'35L70', u'35L75', u'35L45', u'35L15', u'35L65', u'35L60'], [u'35K20', u'35K55', u'35K57', u'35K65', u'35K60'], [u'35J70', u'35J15', u'35J25', u'35J20', u'35J10', u'35J60', u'35J65'], [u'35S05'], [u'35R35', u'35R30'], [u'35Q40', u'35Q75', u'35Q60', u'35Q99', u'35Q30', u'35Q53', u'35Q55', u'35Q35'], [u'35P25', u'35P20', u'35P05', u'35P15']], [[u'82C40']], [[u'03B40']], [[u'01A60']], [[u'20K20'], [u'20M35'], [u'20E15'], [u'20D10', u'20D30'], [u'20G05'], [u'20F36', u'20F05']], [[u'22E50', u'22E47', u'22E40', u'22E45', u'22E46', u'22E30']], [[u'49L25'], [u'49N60'], [u'49J20', u'49J10', u'49J45', u'49J40'], [u'49K15', u'49K20'], [u'49Q15', u'49Q10', u'49Q20', u'49Q05']], [[u'46S10'], [u'46N99', u'46N50'], [u'46E35'], [u'46G20']], [[u'47A40'], [u'47N50'], [u'47B38'], [u'47F05'], [u'47D03']], [[u'45K05']], [[u'28D05']], [[u'43A85', u'43A80']], [[u'05C05']], [[u'76S05'], [u'76P05'], [u'76N10'], [u'76M25', u'76M12', u'76M10'], [u'76B47'], [u'76D05']], [[u'74B20'], [u'74S05'], [u'74K20']], [[u'91B14', u'91B28']], [[u'90B30', u'90B35', u'90B25', u'90B22', u'90B80', u'90B50'], [u'90C30', u'90C35', u'90C05', u'90C08', u'90C10', u'90C29', u'90C27']], [[u'93D15'], [u'93C20'], [u'93B05']], [[u'58Z05'], [u'58E20', u'58E05'], [u'58C25'], [u'58J35', u'58J65', u'58J60', u'58J20', u'58J50', u'58J15', u'58J47', u'58J40']], [[u'11G35', u'11G40', u'11G18', u'11G09', u'11G05'], [u'11D41'], [u'11F33', u'11F70', u'11F80', u'11F67'], [u'11B85', u'11B37'], [u'11M41', u'11M06'], [u'11N25', u'11N37'], [u'11H55'], [u'11K06', u'11K38', u'11K65'], [u'11J70', u'11J72', u'11J81', u'11J86'], [u'11S40'], [u'11R37', u'11R04', u'11R58', u'11R18', u'11R29', u'11R27', u'11R23', u'11R70', u'11R42', u'11R33', u'11R32'], [u'11Y40']], [[u'39A10']], [[u'12H25', u'12H05']], [[u'14C30', u'14C05', u'14C25', u'14C20'], [u'14P25', u'14P10'], [u'14F10', u'14F05', u'14F40', u'14F30'], [u'14G10', u'14G20', u'14G35', u'14G40', u'14G05'], [u'14D20'], [u'14E05', u'14E15'], [u'14N10'], [u'14L05', u'14L30'], [u'14M17'], [u'14J10', u'14J17', u'14J30'], [u'14K15', u'14K10'], [u'14H10', u'14H40', u'14H45', u'14H30', u'14H60', u'14H20', u'14H50']], [[u'17B10', u'17B20', u'17B37', u'17B35']], [[u'55P62']], [[u'18B30', u'18B25'], [u'18C10'], [u'18F15'], [u'18G30', u'18G55'], [u'18D10', u'18D05']], [[u'57M25', u'57M50'], [u'57R30'], [u'57N10']], [[u'30D05']], [[u'37J99', u'37J35', u'37J45'], [u'37A99'], [u'37C75', u'37C85'], [u'37B10'], [u'37D99', u'37D40'], [u'37G99'], [u'37F10', u'37F75']], [[u'53C55', u'53C35', u'53C30', u'53C20', u'53C21', u'53C22', u'53C23', u'53C25', u'53C50', u'53C12', u'53C15', u'53C42', u'53C40'], [u'53B50'], [u'53A10'], [u'53D50'], [u'53Z05']], [[u'34G20'], [u'34A60'], [u'34C25'], [u'34L99'], [u'34M99']], [[u'32B20', u'32B05'], [u'32C38', u'32C30'], [u'32A25'], [u'32D15'], [u'32J15'], [u'32L10'], [u'32M15', u'32M05'], [u'32S05', u'32S65', u'32S25', u'32S40'], [u'32V40'], [u'32W05'], [u'32U05']], [[u'65D17'], [u'65N30', u'65N25', u'65N15', u'65N55'], [u'65M60', u'65M06', u'65M15', u'65M12'], [u'65K10'], [u'65H10'], [u'65R20'], [u'65Z05']]]
    #msc = []
    #counter = 0
    #for h_str in msc_str:
    #    h = []
    #    for m_str in h_str:
    #        m = []
    #        for l_str in m_str:
    #             m.append(counter)
    #             counter = counter + 1
    #        h.append(m)
    #    msc.append(h)
    msc = msc_str
        
    leaf2clusters = trees.bottomup2topdown_tree_converter(msc)
    print "NUM NODES AT H LEVEL:",len(msc)
    
    
    leaves = []
    for h in msc:
        for m in h:
            for l in m:
                leaves.append(l)
    #print 'LEAVES:',leaves
    
    print "-------------------------------------------------------"
    
    msc2 = msc                                        
    MAX_MODIFICATIONS = 1    
    for i in xrange(0,15):        
        leaf2clusters2 = trees.bottomup2topdown_tree_converter(msc2)                
        print get_indexes_dict(leaf2clusters, leaf2clusters2, bonding_calc, membership_calc, membership_bonding, True)
        
        msc3 = []
        nummodifications = 0
        for h in msc2:
            if len(h) == 1 or nummodifications >= MAX_MODIFICATIONS:
                msc3.append(h)
            else:                
                for e in h:
                    msc3.append([e])
                nummodifications = nummodifications + 1
        #print msc3
        msc2 = msc3 
        
    print "-------------------------------------------------------"
    #print msc  
        
    
    
    msc2 = [[leaves]]
    leaf2clusters2 = trees.bottomup2topdown_tree_converter(msc2)    
    print "TOTAL MERGE:",get_indexes_dict(leaf2clusters, leaf2clusters2, bonding_calc, membership_calc, membership_bonding, True)
    
    print "-------------------------------------------------------"          
    
    msc2 = msc                    
    print "NUM NODES AT H LEVEL:",len(msc)            
    MAX_MODIFICATIONS = 1
    
    for i in xrange(0,15):
        leaf2clusters2 = trees.bottomup2topdown_tree_converter(msc2)                
        print get_indexes_dict(leaf2clusters, leaf2clusters2, bonding_calc, membership_calc, membership_bonding, True)        
        
        msc3 = []
        nummodifications = 0
        for h in msc2:
            if len(h) == 1 or nummodifications >= MAX_MODIFICATIONS:
                msc3.append(h)
            else:          
                new_h = []      
                for m in h:
                    new_h.extend(m)
                    msc3.append([new_h])
                nummodifications = nummodifications + 1
        #print msc3
        msc2 = msc3 
                
    #print msc2