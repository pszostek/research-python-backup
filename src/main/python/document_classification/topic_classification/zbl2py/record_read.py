'''
Created on Nov 3, 2011

@author: mlukasik
'''
import pickle

def read_list_records(fname):
    with open(fname, 'rb') as pkl_file:
        return pickle.load(pkl_file)
    