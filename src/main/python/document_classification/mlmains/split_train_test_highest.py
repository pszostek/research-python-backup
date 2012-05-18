'''
Created on Feb 22, 2012

@author: mlukasik
'''
import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import gen_1record_prefixed, gen_record, gen_record_prefixed, gen_lmc, gen_record_fromshifts, gen_record_filteredbylabels, mc2lmc_tomka_blad
from tools.msc_processing import get_labels_min_occurence
#for splitting the data into training and testing
from tools.randomly_divide import randomly_divide

import logging
log_level = logging.INFO
logging.basicConfig(level=log_level)

def PRINTERMAIN(x):
    logging.info('[split_train_test_highest][main]: '+str(x))
    #print '[split_train_test_highest][main]: '+str(x)

def PRINTER(x):
    #pass
    #import logging
    #logging.info(x)
    logging.info('[split_train_test_highest][main]: '+str(x))
    #print '[split_train_test_highest]: '+str(x)
    
def split_train_test_highest(fname, codeprefixlen, mincodeoccurences, filtered_by):
    #prepare generators
    rec_generator = lambda:gen_record(fname, filtered_by)
    prefixed_rec_generator = lambda:gen_record_prefixed(rec_generator, codeprefixlen)
    prefix_code_generator = lambda:gen_lmc(prefixed_rec_generator)
    #generate labels
    PRINTER('generating labels...')
    labels = get_labels_min_occurence(prefix_code_generator, mincodeoccurences)
    PRINTER('labels generated:')
    PRINTER(str(labels))
    
    #gen filtered records:
    labelsset = set(labels)
    prefix_code_generator = lambda:gen_record_filteredbylabels(prefixed_rec_generator, labelsset)
    PRINTER('counting elements...')
    elements_count = len(list(prefix_code_generator()))
    PRINTER('number of elements' +str(elements_count))
    
    #split into training and testing samples
    PRINTER('splitting into training and testing...')
    train_inds, test_inds = randomly_divide(elements_count, int(elements_count / 10))
    train_generator = lambda:gen_record_fromshifts(prefix_code_generator, train_inds)
    test_generator = lambda:gen_record_fromshifts(prefix_code_generator, test_inds)
    PRINTER('splitted.')
    
    elements_count = len(list(prefix_code_generator()))
    return train_generator, test_generator, elements_count, labels, elements_count

if __name__ == "__main__":
    try:
        fname = sys.argv[1]
    except:
        print '1st argument: file name with zbl records.'
        sys.exit(1)
    try:
        codeprefixlen = int(sys.argv[2])
    except:
        print '2nd argument: length of a prefix of codes to be considered'
        sys.exit(1)
    try:
        mincodeoccurences = int(sys.argv[3])
    except:
        print '3d argument: minimum occurence of each of the codes.'
        sys.exit(1)
    try:
        save_train_generator_path = sys.argv[4]
    except:
        print '4th argument: path where the training records are to be stored.'
        sys.exit(1)
    try:
        save_test_generator_path = sys.argv[5]
    except:
        print '5th argument: path where the testing records are to be stored.'
        sys.exit(1)
    try:
        save_labels_path =sys.argv[6]
    except:
        print '6th argument: path where labels list is to be stored.'
        sys.exit(1)
    try:
        save_elements_count_path = sys.argv[7]
    except:
        print '7th argument: path where elements count is to be stored.'
        sys.exit(1)
    try:
        filtered_by = sys.argv[8:]
    except:
        print '8th argument: field names which have to occur for the record to be considered.'
        sys.exit(1)
    
    """
    PRINTERMAIN("Input arguments:")
    PRINTERMAIN("fname: "+fname)
    PRINTERMAIN("codeprefixlen: "+str(codeprefixlen))
    PRINTERMAIN("mincodeoccurences: "+str(mincodeoccurences))
    PRINTERMAIN("save_train_generator_path: "+save_train_generator_path)
    PRINTERMAIN("save_test_generator_path: "+save_test_generator_path)
    PRINTERMAIN("save_labels_path: "+save_labels_path)
    PRINTERMAIN("save_elements_count_path: "+save_elements_count_path)
    PRINTERMAIN("filtered_by: "+str(filtered_by))
    """
    
    train_generator, test_generator, elements_count, labels, elements_count = split_train_test_highest(fname, codeprefixlen, mincodeoccurences, filtered_by)

    from tools.pickle_tools import save_pickle
    save_pickle(list(train_generator()), save_train_generator_path)
    save_pickle(list(test_generator()), save_test_generator_path)
    save_pickle(labels, save_labels_path)
    save_pickle(elements_count, save_elements_count_path)
