#!/usr/bin/env python

import numpy as np
import pylab as pl
from itertools import izip
from calc_correctness import read_hyperplane
from calc_weights import read_input_file_shuffling, get_error, get_hyperplane
from scikits.learn import cross_val
import random

if __name__ == "__main__":
	import sys
	if len(sys.argv)<3:
		print "specify file with objects to evaluate and k for k-fold"
		
	k = int(sys.argv[2])
	#print "w:", w, "bias:", bias	
	print "reading input file..."
	X, y = read_input_file_shuffling(sys.argv[1])
	print "read input file."
	#print X, y
	#input_shuffle = range(len(X))
	#random.shuffle(input_shuffle)

	kf = cross_val.KFold(len(X), k)

	for train_index, test_index in kf:
		#print "TRAIN:", train_index, "TEST:", test_index
		#print "sum(train_index), sum(test_index):", sum(map(train_index)), sum(test_index)
		X_small_tr = X[train_index]
		y_small_tr = y[train_index]
		X_small_tst = X[test_index]
		y_small_tst = y[test_index]
		
		w, bias, _ = get_hyperplane(X_small_tr, y_small_tr)
		print "w:", w
		print "bias:", bias
		print "Blad", get_error(w, bias, X_small_tst, y_small_tst)
		#X_train, X_test = X[train_index], X[test_index]
		#y_train, y_test = y[train_index], y[test_index]

