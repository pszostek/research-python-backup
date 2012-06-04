
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

def run_exec(mpath, args = [], instream=sys.stdin, outstream=sys.stdout, errstream=sys.stderr, prefix = "./"):
    """mpath - path (starting from directory where cpp_wrapper.py is) to the exec-file."""
    strargs = list(str(arg) for arg in args)
    dir = os.path.sep.join([os.path.dirname(inspect.currentframe().f_code.co_filename),os.path.dirname(mpath)])    
    base = os.path.basename(mpath)
    logging.info("[run_exec] Running file="+base+" from dir="+dir+" args="+str(strargs))    
    p = subprocess.Popen(args=[prefix+base]+strargs, stdout=outstream, stderr=errstream, stdin=instream, cwd=dir)
    return p.wait()

        

def aggregate_simmatrix(srcmatrixpath, dstmatrixpath, group2wids_list, method="avg"):    
    """
    Aggregates similarity matrix.
    
    srcmatrixpath - source matrix file path
    dstmatrixpath - output matrix file path
    group2wids_list - list of pairs (group-name, list of pairs (group-element-index, weight) )
    method - avg=average/sl=single link/avgw=weighted average
    """
    groups_tmp_file_path = dstmatrixpath+".groups"
    logging.info("[aggregate_simmatrix] src="+srcmatrixpath+" dst="+dstmatrixpath)
    logging.info("[aggregate_simmatrix] method='"+method+"' group2wids_list="+str(group2wids_list)[:100])
    aux_io.store_group2wids_list(open(groups_tmp_file_path, "w"), group2wids_list)
    fin = open(srcmatrixpath)
    fout = open(dstmatrixpath, "w")
    return run_exec("../cpp_modules/main/aggregate_simmatrix", args = [groups_tmp_file_path, method], instream=fin, outstream=fout)

def zbl_similarity_matrix(zblpath, dstmatrixpath, field_name, similarity_calculator):
    run_exec("../cpp_modules/main/zbl_similarity_matrix", args = [field_name, similarity_calculator], instream=open(zblpath), outstream=open(dstmatrixpath, "w"))
    
