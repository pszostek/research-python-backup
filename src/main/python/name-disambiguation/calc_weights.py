#!/usr/bin/env python
#!/usr/bin/env python

import numpy as np
import pylab as pl
from scikits.learn import svm
from itertools import izip
import random

#------------------Generating a hyperplane
def get_hyperplane(X, y):
	"""Get hyperplane, to which get_hyper_classif applies"""
	w, bias, clf = get_svn_params(X, y)
	sign = find_sign(w, bias, X, y)
	w = map(lambda x: x*sign, w)
	bias*=sign
	return w, bias, clf

def get_svn_params(X, y):
	clf = svm.SVC(kernel='linear')
	clf.fit(X, y)
	if len(clf.intercept_) <> 1:
		print "ERROR in get_hyperplane(X, y). more than 1 coefficient??"
		return

	return clf.coef_[0], clf.intercept_[0], clf

def find_sign(w, bias, X, y):
	if get_error(w, bias, X, y)>0.5:
		return -1
	return 1
#-----------------Reading input file
def read_input_file(in_file):
	with open(in_file) as f:
		return extract_Xy(f)

def read_input_file_shuffling(in_file):
	"""Used in calc_kf for shuffling the input file before diving into k parts"""	
	with open(in_file) as f:
		Xy = f.readlines()
		random.shuffle(Xy)
		return extract_Xy(Xy)

def extract_Xy(input_stream):
	X = []
	y = []
	for l in input_stream:
		vec = [float(i) for i in l.split(';')[1:]]
		X.append(vec[0:len(vec)-1])
		y.append(int(vec[len(vec)-1]))
	return np.array(X), np.array(y)
	
#-----------------Getting classification from the parameters of a hyperplane
def get_hyper_classif(w, bias, xts):
	if sum(x1*w1 for x1, w1 in zip(xts, w)) + bias>0:
		return 1
	return -1

#-----------------Verification and error estimation
def verify_hard(w, bias, X, y, clf):
	error = 0
	for xts, yts in izip(X, y):
		#if clf.predict(xts) != get_hyper_classif(w, bias, xts):
			#print "ERROR!!! hyperplane handwritten returns smth different than classifier itself"
		#	break
		error += get_hyper_classif(w, bias, xts) != yts
	return (error*1.0/len(X)), len(X), error

def get_error(w, bias, X, y):
	error = sum( map(lambda (xts, yts): get_hyper_classif(w, bias, xts) != yts, izip(X, y) ))
	#error = 0
	#for xts, yts in izip(X, y):
	#	error += get_hyper_classif(w, bias, xts) != yts
	return (error*1.0/len(X))
#----------------------------------------------------
if __name__ == "__main__":
	import sys
	#read input data:
	if len(sys.argv)>1:
		X, y = read_input_file(sys.argv[1])
	else:
		X = np.array([[2, 2], [1, 1], [0, 0], [0.5, 0.5], [0.75, 0.25]])
		y = [1, -1, -1, 1, 1]
		
	w, bias, clf = get_hyperplane(X, y)
	print "w:", w, "bias:", bias
	#print verify_hard(w, bias, X, y, clf)
	#print get_error(w, bias, X, y)
