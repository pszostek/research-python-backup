
import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')

from tools import msc_processing
from tools import randomized
from data_io import zbl_io
from trees import *
from tree_distance import *
import tree_distance
from random_tree import *


import random
import logging
import trees
import math
import time

from tools.stats import *

bonding_calc = lambda common_path_fraction: common_path_fraction
membership_calc = lambda common_levels: common_levels/2.0
membership_bonding = angular_bonding
only_fast_calculations = True

NUM_TRIES = 100 #how many experiments
        
if __name__ == "__main__":
    print "345-pattern-tree from NUMDAM/CEDRAM data..."
    msc_tree = [[[u'42B20', u'42B25']], [[u'60E15'], [u'60G15', u'60G07', u'60G40', u'60G42', u'60G44', u'60G48', u'60G60', u'60G17', u'60G57', u'60G51', u'60G50'], [u'60F05', u'60F17', u'60F15', u'60F10'], [u'60B05', u'60B10', u'60B15'], [u'60H07', u'60H05', u'60H99', u'60H15', u'60H10', u'60H20'], [u'60K40', u'60K35', u'60K37', u'60K25'], [u'60J60', u'60J65', u'60J25', u'60J35', u'60J45', u'60J10', u'60J55', u'60J80']], [[u'68Q45', u'68Q65', u'68Q60', u'68Q55', u'68Q80', u'68Q10', u'68Q15', u'68Q42', u'68Q05', u'68Q25', u'68Q70'], [u'68R10', u'68R15']], [[u'62G07', u'62G05', u'62G10'], [u'62E20'], [u'62H25', u'62H30'], [u'62M05']], [[u'35G10'], [u'35A20', u'35A27'], [u'35D10', u'35D05'], [u'35B25', u'35B27', u'35B65', u'35B40', u'35B05', u'35B45'], [u'35L05', u'35L70', u'35L75', u'35L45', u'35L15', u'35L65', u'35L60'], [u'35K20', u'35K55', u'35K57', u'35K65', u'35K60'], [u'35J70', u'35J15', u'35J25', u'35J20', u'35J10', u'35J60', u'35J65'], [u'35S05'], [u'35R35', u'35R30'], [u'35Q40', u'35Q75', u'35Q60', u'35Q99', u'35Q30', u'35Q53', u'35Q55', u'35Q35'], [u'35P25', u'35P20', u'35P05', u'35P15']], [[u'82C40']], [[u'03B40']], [[u'01A60']], [[u'20K20'], [u'20M35'], [u'20E15'], [u'20D10', u'20D30'], [u'20G05'], [u'20F36', u'20F05']], [[u'22E50', u'22E47', u'22E40', u'22E45', u'22E46', u'22E30']], [[u'49L25'], [u'49N60'], [u'49J20', u'49J10', u'49J45', u'49J40'], [u'49K15', u'49K20'], [u'49Q15', u'49Q10', u'49Q20', u'49Q05']], [[u'46S10'], [u'46N99', u'46N50'], [u'46E35'], [u'46G20']], [[u'47A40'], [u'47N50'], [u'47B38'], [u'47F05'], [u'47D03']], [[u'45K05']], [[u'28D05']], [[u'43A85', u'43A80']], [[u'05C05']], [[u'76S05'], [u'76P05'], [u'76N10'], [u'76M25', u'76M12', u'76M10'], [u'76B47'], [u'76D05']], [[u'74B20'], [u'74S05'], [u'74K20']], [[u'91B14', u'91B28']], [[u'90B30', u'90B35', u'90B25', u'90B22', u'90B80', u'90B50'], [u'90C30', u'90C35', u'90C05', u'90C08', u'90C10', u'90C29', u'90C27']], [[u'93D15'], [u'93C20'], [u'93B05']], [[u'58Z05'], [u'58E20', u'58E05'], [u'58C25'], [u'58J35', u'58J65', u'58J60', u'58J20', u'58J50', u'58J15', u'58J47', u'58J40']], [[u'11G35', u'11G40', u'11G18', u'11G09', u'11G05'], [u'11D41'], [u'11F33', u'11F70', u'11F80', u'11F67'], [u'11B85', u'11B37'], [u'11M41', u'11M06'], [u'11N25', u'11N37'], [u'11H55'], [u'11K06', u'11K38', u'11K65'], [u'11J70', u'11J72', u'11J81', u'11J86'], [u'11S40'], [u'11R37', u'11R04', u'11R58', u'11R18', u'11R29', u'11R27', u'11R23', u'11R70', u'11R42', u'11R33', u'11R32'], [u'11Y40']], [[u'39A10']], [[u'12H25', u'12H05']], [[u'14C30', u'14C05', u'14C25', u'14C20'], [u'14P25', u'14P10'], [u'14F10', u'14F05', u'14F40', u'14F30'], [u'14G10', u'14G20', u'14G35', u'14G40', u'14G05'], [u'14D20'], [u'14E05', u'14E15'], [u'14N10'], [u'14L05', u'14L30'], [u'14M17'], [u'14J10', u'14J17', u'14J30'], [u'14K15', u'14K10'], [u'14H10', u'14H40', u'14H45', u'14H30', u'14H60', u'14H20', u'14H50']], [[u'17B10', u'17B20', u'17B37', u'17B35']], [[u'55P62']], [[u'18B30', u'18B25'], [u'18C10'], [u'18F15'], [u'18G30', u'18G55'], [u'18D10', u'18D05']], [[u'57M25', u'57M50'], [u'57R30'], [u'57N10']], [[u'30D05']], [[u'37J99', u'37J35', u'37J45'], [u'37A99'], [u'37C75', u'37C85'], [u'37B10'], [u'37D99', u'37D40'], [u'37G99'], [u'37F10', u'37F75']], [[u'53C55', u'53C35', u'53C30', u'53C20', u'53C21', u'53C22', u'53C23', u'53C25', u'53C50', u'53C12', u'53C15', u'53C42', u'53C40'], [u'53B50'], [u'53A10'], [u'53D50'], [u'53Z05']], [[u'34G20'], [u'34A60'], [u'34C25'], [u'34L99'], [u'34M99']], [[u'32B20', u'32B05'], [u'32C38', u'32C30'], [u'32A25'], [u'32D15'], [u'32J15'], [u'32L10'], [u'32M15', u'32M05'], [u'32S05', u'32S65', u'32S25', u'32S40'], [u'32V40'], [u'32W05'], [u'32U05']], [[u'65D17'], [u'65N30', u'65N25', u'65N15', u'65N55'], [u'65M60', u'65M06', u'65M15', u'65M12'], [u'65K10'], [u'65H10'], [u'65R20'], [u'65Z05']]]
    print "Converting tree..."
    msc_leaf2clusters_strs = trees.bottomup2topdown_tree_converter(msc_tree)
    msc_leaf2clusters = msc_leaf2clusters = dict( (ix,lst) for ix, (code,lst) in enumerate( msc_leaf2clusters_strs.iteritems() ) )
    #print msc_leaf2clusters 
                    
    print "Calculating for random trees..."
    results = {} #{index-name: list of results}
    start = time.clock()
    for i in xrange(NUM_TRIES):
        print "",(time.clock()-start),i,"out of",NUM_TRIES,
        (num_l, num_m, indexes_dict) = compare_to_random_tree(msc_leaf2clusters, \
                                                              bonding_calc, membership_calc, membership_bonding,\
                                                              only_fast_calculations)
        indexes_dict["num_l"] = num_l
        indexes_dict["num_m"] = num_m
        for id, val in indexes_dict.iteritems():
            results[id] = results.get(id,[])+[val]
    print "Results:",results
    
    print "Tree self-comparison..."
    print "",tree_distance.get_indexes_dict(msc_leaf2clusters, msc_leaf2clusters, \
                                                  bonding_calc, membership_calc, membership_bonding,\
                                                  only_fast_calculations)
        
    print "Stats..."
    print "\tid\tavg\tstd"
    for id,vals in results.iteritems():
        print "\t",id,"\t",avg(vals),"\t",std(vals)        
        
    print "Num clusters vs index..."    
    for id,vals in results.iteritems():
        if id == "num_l" or id == "num_m": continue
        num_l = results["num_l"]
        num_m = results["num_m"]
        print "\t",id,"----------"
        print "\tnum_l\tnum_m\tval"
        for i in xrange(len(vals)):
            print "\t",num_l[i],"\t",num_m[i],"\t",vals[i]
