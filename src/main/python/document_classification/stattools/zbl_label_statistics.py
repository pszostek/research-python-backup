'''
Created on Mar 11, 2012

@author: mlukasik
'''
from __future__ import division 
import sys
sys.path.append(r'../')
#from data_io.zbl_record_generators import gen_lmc
#from tools import msc_processing
from tools.msc_processing import count_msc_occurences

def count_label_statistics(counts_lowest, label_mappings):
    """
    Counts the following statistics:
    
    ->how many times each label occurs
    ->->how many times each of its sub-labels occurs
    ->->->how many times each of its sub-sub-labels occurs
    ->how many labels each document has on average
    
    """
    counts_higher = [{} for _ in label_mappings]
    
    for key, count in counts_lowest.iteritems():
        for ind, label_map in enumerate(label_mappings):
            higher_key = label_map(key)
            if higher_key in counts_higher[ind]:
                counts_higher[ind][higher_key]['count'] += count
                counts_higher[ind][higher_key]['elements'].add(key)
            else:
                counts_higher[ind][higher_key] = {}
                counts_higher[ind][higher_key]['count'] = count
                counts_higher[ind][higher_key]['elements'] = set([key])
            key = label_map(key)
    counts_higher.reverse()
    return counts_lowest, counts_higher

def print_counts(counts_lowest, counts_higher, curr_labels, start_printable, data4avg_stats):
    '''
    Print the dictionaries in a nested way.
    
    At the same time, gather the data needed to calculate the average statistics on the gathered data:
    -average and std deviation of a degree of a parental node
    -average and std deviation of number of representatives of a node
    '''
    if counts_higher:
        for curr_l in curr_labels:
            print start_printable+"[print_counts] key: "+curr_l+": "+str(counts_higher[0][curr_l]['count'])+", children: "+str(len(counts_higher[0][curr_l]['elements']))
            print_counts(counts_lowest, counts_higher[1:], counts_higher[0][curr_l]['elements'], start_printable+'\t', data4avg_stats)
            
            #add data to data4avg_stats:
            curr_level = len(counts_higher)
            if curr_level not in data4avg_stats:
                data4avg_stats[curr_level] = {'degrees': [], 'counts': []}
            data4avg_stats[curr_level]['degrees'].append(len(counts_higher[0][curr_l]['elements']))
            data4avg_stats[curr_level]['counts'].append(counts_higher[0][curr_l]['count'])

    else:
        for curr_l in curr_labels:
            print start_printable+"[print_counts] key: "+curr_l+": "+str(counts_lowest[curr_l])

def calc_avg_dev(l):
    '''
    Calculate avg and std deviation.
    '''
    import numpy
    return numpy.average(l), numpy.std(l)

def print_avg_stats(data4avg_stats):
    '''
    calculate and print the average statistics on the gathered data:
    -average and std deviation of a degree of a parental node
    -average and std deviation of number of representatives of a node
    '''
    for key, val in data4avg_stats.iteritems():
        print "-----------------------------------------------------"
        print "Statistics for level: "+str(key)
        
        avg, std_dev = calc_avg_dev(val['degrees'])
        print "List of degrees: "+str(val['degrees'])
        print "Average degree: "+str(avg)
        print "Standard deviation of a degree: "+str(std_dev)
        
        avg, std_dev = calc_avg_dev(val['counts'])
        print "List of counts: "+str(val['counts'])
        print "Average count: "+str(avg)
        print "Standard deviation of a count: "+str(std_dev)
        

#def print_counts(counts_lowest, counts_higher, curr_labels, start_printable):
#    '''
#    Print the dictionaries in a nested way.
#    '''
#    if counts_higher:
#        for curr_l in curr_labels:
#            print start_printable+"[print_counts] key: "+curr_l+": "+str(counts_higher[0][curr_l]['count']+", children: "+str(len(counts_higher[0][curr_l]['elements'])))
#            print_counts(counts_lowest, counts_higher[1:], counts_higher[0][curr_l]['elements'], start_printable+'\t')
#    else:
#        for curr_l in curr_labels:
#            print start_printable+"[print_counts] key: "+curr_l+": "+str(counts_lowest[curr_l])

if __name__ == '__main__':
    fname = sys.argv[1]
    print "fname:", fname
    counts_lowest, counts_higher = count_label_statistics(count_msc_occurences(open(fname, 'r')), label_mappings = [lambda x: x[:3], lambda x: x[:2]])
    #print counts_lowest, counts_higher
    data4avg_stats = {}
    print_counts(counts_lowest, counts_higher, list(counts_higher[0].iterkeys()), '', data4avg_stats)
    print_avg_stats(data4avg_stats)