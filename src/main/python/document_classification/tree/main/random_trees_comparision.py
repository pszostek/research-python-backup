
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

def _get_zbl_generator_(zbl_path, must_have_fields):
    """Returns zbl-records generator that has guaranteed presence of must_have_fields."""
    UNI = True #unic
    f = zbl_io.open_file(zbl_path, UNI)    
    for ix,zbl in enumerate(zbl_io.read_zbl_records(f, UNI)):        
        has_all_fields = sum(1 for field in must_have_fields if field in zbl) == len(must_have_fields)
        #has_all_fields = True
        #for field in must_have_fields:
        #    if not field in zbl:
        #        has_all_fields = False                
        #        break
        #print zbl,"->",has_all_fields                
        if has_all_fields:
            zbl[zbl_io.ZBL_ID_FIELD] = ix #replacing ids with numbers for faster processing
            yield zbl


#must_have_fields = ['mc']
#must_have_fields = ['mc','ti','py','ab', 'ut', 'ft', 'ci','au', 'af', 'jt', 'jn'] #full-data
must_have_fields = ['mc','ti','py','ab','ut','ci'] #AB-CI
 
MIN_COUNT_MSC = 3 #ile minimalnie dokumentow zeby zachowac klase
NUM_TRIES = 100 #ile eksperymenow
VALID_LEAF_PATTERN_RE = msc_processing.MSC_ORDINARY_LEAF_PATTERN_RE

bonding_calc = lambda common_path_fraction: common_path_fraction
membership_calc = lambda common_levels: common_levels/2.0
membership_bonding = angular_bonding
only_fast_calculations = False
        
if __name__ == "__main__":
    #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    try:
        zbl_path = sys.argv[1]
    except:
        print "First argument expected: zbl-file-path."
        sys.exit(-1)
    #l - low level, m - medium level, h - highest level of MSC tree
    print "MIN_COUNT_MSC=",MIN_COUNT_MSC 
    print "NUM_TRIES=",NUM_TRIES
    print "VALID_LEAF_PATTERN_RE=",VALID_LEAF_PATTERN_RE    
    print "must_have_fields=",must_have_fields
    print "zbl_path=",zbl_path
     
    print "Building list of msc-primary-codes that should be considered..."
    start = time.clock()
    msc2count = {}
    for i,zbl in enumerate(_get_zbl_generator_(zbl_path, must_have_fields)):
        if i%10000 == 0: print "",i,"records processed in",(time.clock()-start),"s ->",sum(msc2count.values()),"kept"        
        msc_codes = [ zbl_io.unpack_multivalue_field(zbl['mc'])[0] ] #only primary
        for msc in msc_codes:
            #print msc,"->",(not VALID_LEAF_PATTERN_RE.match(msc) is None)
            if not VALID_LEAF_PATTERN_RE.match(msc) is None:
                msc2count[msc] = msc2count.get(msc, 0)+1        
    print "Filtering for with MIN_COUNT_MSC:",MIN_COUNT_MSC," out of", sum(msc2count.values())
    msc2count = dict((msc,count) for msc,count in msc2count.iteritems() if count>=MIN_COUNT_MSC)
    print "Building mapping msc2ix"
    msc2ix = dict((msc,ix) for ix,msc in enumerate(msc2count))
    ix2msc = dict((ix,msc) for msc,ix in msc2ix.iteritems())
    leaves = list( msc2ix )
    num_leaves = len(leaves)
    print "Building MSC tree out of", num_leaves, "leaves"
    msc_tree = trees.build_msctree(msc2ix.keys(), msc2ix)
    #print str(trees.map_tree_leaves(msc_tree, ix2msc))[:400] 

    msc_leaf2clusters = trees.bottomup2topdown_tree_converter(msc_tree)
                        
                    
    print "Random trees..."
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
