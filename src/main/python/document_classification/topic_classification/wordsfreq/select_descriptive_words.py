'''
Created on Nov 13, 2011

@author: mlukasik
'''
from __future__ import division
from collections import defaultdict

"""Functions for reading dictionary of words -> freqs from a file"""
def read_freq_dict_from_f(f):
    """Read a frequency list from a file"""
    d = {}
    with open(f) as df:
        d = convert_to_freq_dict(df)
    return d

def convert_to_freq_dict(f):
    """Read a frequency list from a file"""
    d = {}
    i=0
    for l in f:
        i+=1
        l_list = l.replace(' ', '').replace('\n', '').split(":")
        d[l_list[0]] = (l_list[1], i)
    return d

def select_descriptive_words_quotientmethod(extr_fromfname, basefname, words_count, thresh_div):
    """Extract words_count number of words from extr_fromfname, which are more frequent then in basefname, that is:
        -either they are not in basefname at all
        -or their position no1 in extr_fromfname divided by their position in basefname is bigger than thresh_div
    """
    extr_from = read_freq_dict_from_f(extr_fromfname)
    base = read_freq_dict_from_f(basefname)
    
    extr_from_sorted = sorted(list(extr_from.iteritems()), key=lambda l: l[1][1])#sort by frequencies
    
    selected = 0
    el_ind = 0
    words = []
    for el_all in extr_from_sorted:#iterate from the most popular number
        el = el_all[0]
        #print el_all
        #print "considering", el
        el_ind+=1
        if not base.has_key(el):
            selected+=1
            #print selected, el_all
            words.append(el)
            if selected>=words_count:
                break
        else:
            base_el = base[el]
            if base_el[1] < el_ind and thresh_div < el_ind/base_el[1]:
                #print "thresh_div, el_ind, base_el[1], el_ind/base_el[1]", thresh_div, el_ind, base_el[1], el_ind/base_el[1]
                selected+=1
                #print selected, el_all
                words.append(el)
                if selected>=words_count:
                    break
    return words

def select_descriptive_words_keywords(frecords, how_many_elems=100):
    """Extract words that occur in keywords"""
    words = defaultdict(lambda: 0)
    for rec in frecords:
        #print rec
        for kw in rec['keywords']:
            words[kw]+=1
    
    return sorted(map(lambda x: (x[0], x[1]), words.iteritems()), key=lambda x: x[1], reverse=True)[:how_many_elems]
    
    #return list(set( reduce(lambda a, b: a+b, map(lambda x: x['keywords'], frecords)) ))
    
if __name__ == '__main__':
    import sys
    for thresh_div in [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50]:
        print "thresh_div:", thresh_div
        for i in select_descriptive_words_quotientmethod(sys.argv[1], sys.argv[2], int(sys.argv[3]), thresh_div):#float(sys.argv[4])):
            print i
        print "--------------------------------"