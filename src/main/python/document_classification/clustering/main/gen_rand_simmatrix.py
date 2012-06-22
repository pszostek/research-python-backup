"""The program generates random similarity matrix for MSC codes (filtered and extracted from ZBL file)."""

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
from tools.stats import *
from tools.randomized import *

from data_io import zbl_io
from data_io import matrix_io


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


                
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    try:
        zbl_path = sys.argv[1]
    except:
        print "Argument expected: zbl-file-path."
        sys.exit(-1)
        
    try:
        output_path = sys.argv[2]
    except:
        print "Argument expected: output-similarity-matrix-path."
        sys.exit(-1)        
        
    print "The program generates random similarity matrix for MSC codes (filtered and extracted from ZBL file)."
        
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
    msc_list = list( ix2msc[ix] for ix in xrange(len(ix2msc)) )    
    print " msc2ix=",str(list(msc2ix.iteritems()))[:100]
    
    
    print "--------------------------------------------------------"
    print "Storing random similarity matrix to",output_path
    matrix_io.fwrite_smatrix([ [random.random() for msc in msc_list] for msc in msc_list], msc_list, msc_list, output_path)
            
    