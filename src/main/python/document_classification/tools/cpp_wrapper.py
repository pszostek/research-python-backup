
import subprocess,os
from pipes import *
import inspect
import logging
import sys
    
import sys,os
sys.path.append(r'../')
sys.path.append(r'../../')
sys.path.append(r'../../../')

from data_io import aux_io    

def run_exec(mpath, args = [], instream=sys.stdin, outstream=sys.stdout, errstream=sys.stderr):
    """mpath - path (starting from directory where cpp_wrapper.py is) to the exec-file."""
    strargs = list(str(arg) for arg in args)
    dir = os.path.sep.join([os.path.dirname(inspect.currentframe().f_code.co_filename),os.path.dirname(mpath)])    
    base = os.path.basename(mpath)
    logging.info("[run_exec] Running file="+base+" from dir="+dir+" args="+str(strargs))    
    p = subprocess.Popen(args=["./"+base]+strargs, stdout=outstream, stderr=errstream, stdin=instream, cwd=dir)
    return p.wait()

        

AGG_SIM_GROUP2WIXS_LIST_PATH = "/tmp/AGG_SIM_GROUP2WIXS_LIST_PATH.txt"

def aggregate_simmatrix(srcmatrixpath, dstmatrixpath, group2wids_list, method="avg"):    
    """
    Aggregates similarity matrix.
    
    srcmatrixpath - source matrix file path
    dstmatrixpath - output matrix file path
    group2wids_list - list of pairs (group-name, list of pairs (group-element-index, weight) )
    method - avg=average/sl=single link/avgw=weighted average
    """
    logging.info("[aggregate_simmatrix] src="+srcmatrixpath+" dst="+dstmatrixpath+" method="+method+" group2wids_list="+str(group2wids_list)[:50])
    aux_io.store_group2wids_list(open(AGG_SIM_GROUP2WIXS_LIST_PATH, "w"), group2wids_list)
    fin = open(srcmatrixpath)
    fout = open(dstmatrixpath, "w")
    return run_exec("../cpp_modules/main/aggregate_simmatrix", args = [AGG_SIM_GROUP2WIXS_LIST_PATH, method], instream=fin, outstream=fout)

