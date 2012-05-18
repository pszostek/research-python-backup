'''
Created on Feb 13, 2012

@author: mlukasik
'''

#----------------------------PICKLE-------------------------------#
import pickle

def read_pickle(fname):
    pkl_file = open(fname, 'rb')
    
    data = pickle.load(pkl_file)
    
    pkl_file.close()
    
    return data

def save_pickle(obj, savepath):
    output = open(savepath, 'wb')

    # Pickle dictionaries
    pickle.dump(obj, output)
    
    output.close()