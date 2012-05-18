#!/usr/bin/env python

import numpy as np
import pylab as pl
from itertools import izip
from calc_weights import read_input_file, get_hyper_classif, get_error

def read_hyperplane(fname):
	with open(fname) as f:
		wbiasl = (f.readlines()[-1]).split("bias:")
		bias = float(wbiasl[1])
		w = map(lambda x: float(x), wbiasl[0].replace("w:", "").replace("[", "").replace("]", "").split(","))
	return w, bias

if __name__ == "__main__":
	import sys
	if len(sys.argv)<3:
		print "specify output file from calc-weights and file with objects to evaluate"
		
	w, bias = read_hyperplane(sys.argv[1])
	print "w:", w, "bias:", bias	
	X, y = read_input_file(sys.argv[2])
	print get_error(w, bias, X, y)
