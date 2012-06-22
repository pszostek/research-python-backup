"""The module that allows to run MATLAB scripts."""
import subprocess,os
from pipes import *
import inspect
import logging
    
MATLAB_COMMAND = "octave"
MATLAB_STDOUT = open('/tmp/matlab_wrapper_stdout.txt','a+')

def run_matlab(mpath, args = []):
    """mpath - path (starting from directory where matlab_wrapper.py is) to the M-file."""
    strargs = list(str(arg) for arg in args)
    dir = os.path.sep.join([os.path.dirname(inspect.currentframe().f_code.co_filename),os.path.dirname(mpath)])    
    base = os.path.basename(mpath)
    logging.info("[run_matlab] Running M-file="+base+" from dir="+dir)
    t = Template()
    p = subprocess.Popen(args=[MATLAB_COMMAND]+[base]+strargs, stdout=MATLAB_STDOUT, stderr=MATLAB_STDOUT, cwd=dir)
    return p.wait()