"""Framework that calculates similarity matrix and then builds MSC tree using build_msc_tree.py"""
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
from tools import aux
from tools import cpp_wrapper
import build_msc_tree
import subprocess,os
from pipes import *
import inspect
import logging
import sys



if __name__ == "__main__":
    print "Framework that calculates similarity matrix and then builds MSC tree using build_msc_tree.py"
    
    sys.stderr = sys.stdout
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)    
    
    try:
        zbl_path = sys.argv[1]
    except:
        print "Argument expected: zbl-file-path."
        sys.exit(-1)
    try:
        field_name = sys.argv[2]
    except:
        print "Argument exepected: source-field-in-zbl-records e.g. g2"
        sys.exit(-1)
    try:
        similarity_calculator = sys.argv[3]
    except:
        print "Argument exepected: similarity-calculator-name e.g. angular"
        sys.exit(-1)
    try:
        clustering_method = sys.argv[4]
    except:
        print "Argument exepected: clustering method for build_msc_tree.py"
        sys.exit(-1)
                
    sim_matrix_path = os.path.dirname(zbl_path)+"/"+os.path.basename(zbl_path).split('.')[0]+"."+field_name+"."+similarity_calculator+".txt"
                
    print " zbl_path =",zbl_path
    print " sim_matrix_path =",sim_matrix_path
    print " field_name =",field_name
    print " similarity_calculator=",similarity_calculator
    print " clustering_method=",clustering_method
                        
    if not aux.exists(sim_matrix_path):
        cpp_wrapper.zbl_similarity_matrix(zbl_path, sim_matrix_path, field_name, similarity_calculator)
        
    msc_argv = ['python', 'build_msc_tree.py', zbl_path, sim_matrix_path, clustering_method]
    p = subprocess.Popen(msc_argv)
    p.wait()
        

    