'''
Created on Jan 2, 2012

@author: mlukasik

Script allowing to create a smaller dataset out of a large SPRINGER data.
It does the task by sampling the input data randomly.

Example use:
python narrow_zbldata.py ../topic_classification/zbl2py/springer011211.txt ../topic_classification/zbl2py/narrow_8 5 15 20 5000 mc ti ab ut
consecutive arguments are: fromfile, savefile, prefixlen, minimum_number_of_occurrence of a given code,
 biggest etiquettes number that are going to be taken, number of elements that are going to be randomly chosen (at the start).
'''

import sys
sys.path.append(r'../')
from data_io.zbl_record_generators import gen_record, gen_record_prefixed, gen_lmc, gen_record_fromshifts, gen_record_filteredbylabels
from tools.msc_processing import get_labels_counts, get_labelperdocuments_counts
from data_io.zbl_io import write_zbl_records

def PRINTER(x):
    print '[narrow_zbldata]: ', x

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except:
        print '1st argument: input file with zbl records.'
        sys.exit(1)
    try:
        savefname = sys.argv[2]
    except:
        print '2nd argument: path where to save the result.'
        sys.exit(1)
    try:
        codeprefixlen = int(sys.argv[3])
    except:
        print '3d argument: code prefix to consider.'
        sys.exit(1)
    try:
        mincodeoccurences = int(sys.argv[4])
    except:
        print '4th argument: minimum occurence of a code.'
        sys.exit(1)
    try:
        biggest_labels_cnt = int(sys.argv[5])
    except:
        print '5th argument: number of labels to consider'
        sys.exit(1)
    try:
        shuffling_cnt = int(sys.argv[6])
    except:
        print '6th argument: How many records to sample before the further filtering.'
        sys.exit(1)
    try:
        filtered_by = sys.argv[7:]
    except:
        print '7th argument: list of the fields to exist in considered records.'
        sys.exit(1)
    
    #prepare generators
    rec_generator_first = lambda: gen_record(fname, filtered_by)
    #choosing shuffling_cnt elements in random:
    PRINTER("shuffling in random")
    import random
    chosen_records = random.sample(list(rec_generator_first()), shuffling_cnt)
    rec_generator = lambda: chosen_records
    
    prefixed_rec_generator = lambda: gen_record_prefixed(rec_generator, codeprefixlen)
    prefix_code_generator = lambda: gen_lmc(prefixed_rec_generator)
    
    #generate labels
    PRINTER("generating labels...")
    labels_counts = get_labels_counts(prefix_code_generator, mincodeoccurences)
    #PRINTER("labels generated."
    #PRINTER(sorted(labels_counts, key = lambda x: x[1], reverse = True)
    biggest_labels = map(lambda x: x[0], sorted(labels_counts, key = lambda x: x[1], 
                                                reverse = True))[:biggest_labels_cnt]
    labelsset = set(biggest_labels)
    PRINTER(biggest_labels)
    
    #gen filtered records:
    prefix_code_generator = lambda: gen_record_filteredbylabels(prefixed_rec_generator, labelsset)
    PRINTER("counting elements...")
    elements_count = len(list(prefix_code_generator()))
    PRINTER("number of elements:"+str(elements_count))
    
    
    codes_generator = lambda: gen_lmc(prefix_code_generator)
    PRINTER("labels per document statistics:"+str(get_labelperdocuments_counts(codes_generator)))
    
    PRINTER("saving...")
    write_zbl_records(open(savefname, 'w'), prefix_code_generator())