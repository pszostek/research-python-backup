"""Framework that builds MSC trees using build_msc_tree.py"""
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
    sys.stderr = sys.stdout
    print "[zbl_build_msc_tree] ============================================================================================================"        
    print "[zbl_build_msc_tree] Framework that builds MSC trees using build_msc_tree.py"
        
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)    
    
    try:
        zbl_path = sys.argv[1]
    except:
        print "Argument expected: zbl-file-path."
        sys.exit(-1)
    try:
        parameters_file = sys.argv[2]
    except:
        print "Argument exepected: parameters-file"
        sys.exit(-1)

    print "[zbl_build_msc_tree]  zbl_path =",zbl_path
    print "[zbl_build_msc_tree]  parameters_file =",parameters_file

    parameters = open(parameters_file).readlines()
        
    for configuration in parameters:
        msc_argv = ['python', 'build_msc_tree.py', zbl_path] + configuration.split()
        print "[zbl_build_msc_tree]  running:",msc_argv
        p = subprocess.Popen(msc_argv)
        print "--->",p.wait()
        

    