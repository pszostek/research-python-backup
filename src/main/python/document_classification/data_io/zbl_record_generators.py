'''
Created on Dec 15, 2011

@author: mlukasik

Generators which allow to read processed records one by one.
'''
import codecs
import sys
sys.path.append(r'../') 
from zbl_io import read_zbl_records, MULTIVAL_FIELD_SEPARATOR
from tools.msc_processing import get_prefixes_list, zblrecord_deep_copy, get_labels_min_occurence

def gen_record(fname, filtered_by, uni = False):
    """
    Returns records that contain fields specified in filtered_by
    
    """    
    if type(fname) == file:
        ff = fname
    elif uni:
        ff = codecs.open(fname, 'r', encoding='utf-8')
    else:
        ff = open(fname, 'r')
            
    for r in read_zbl_records(ff, uni):
        if reduce(lambda x, y: x and y, map(lambda f: f in r, filtered_by)):
            yield r

def gen_text(fname, fields, filtered_by = ['mc'], uni = False):
    """
    Returns text created by joining fields from fields list, only those that contain all the field from fields + filtered_by
    
    """
    for r in gen_record(fname, fields+filtered_by, uni):
        yield " ".join(map(lambda f: r[f], fields))

def gen_text_mc(fname, fields, filtered_by = ['mc'], uni = False):
    """
   Returns text created by joining fields from fields list, only those that contain all the field from fields + filtered_by; 
    returns mc code as well
    
    """
    for r in gen_record(fname, fields+filtered_by, uni):
        yield " ".join(map(lambda f: r[f], fields)), mc2lmc_tomka_blad(r)
        

def gen_lmc(record_generator, mc = 'mc'):
    """
    Returns codes of records, only those that contain all the field from fields + filtered_by;
    
    """
    for r in record_generator():
        #TODO map z powodu takiego ze wygenerowane z bledem tomka
        yield mc2lmc_tomka_blad(r)
        
def mc2lmc_tomka_blad(r, mc = 'mc'):
    """
    Zwraca kody kasyfikacyjne MSC w postaci listy.
    
    Sample use:
    >>> mc2lmc_tomka_blad({'ab': 5, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"+MULTIVAL_FIELD_SEPARATOR}) == ["a", "g", "h"]
    True
    >>> mc2lmc_tomka_blad({'ab': 5, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"+MULTIVAL_FIELD_SEPARATOR+"e"}) == ["a", "g", "h", "e"]
    True
    """
    return filter(lambda x: x, r[mc].split(MULTIVAL_FIELD_SEPARATOR))

def lmc2mc_tomka_blad(l):
    """
    Zwraca kody klasyfikacyjne z listy do formatu jak w rekordzie ZBL.
    
    Sample use:
    >>> lmc2mc_tomka_blad(["a", "g", "h"]) == "a"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"
    True
    """
    return MULTIVAL_FIELD_SEPARATOR.join(l)  

def gen_record_prefixed(gen_record, prefixlen, mc = 'mc'):
    """
    Returns records that contain fields specified in filtered_by. 
    Returns prefixes of its codes of length prefixlen.
    
    TESTED.
    """
    for r in gen_record():
        prefixed_codes = get_prefixes_list(mc2lmc_tomka_blad(r), prefixlen)
        r[mc] = lmc2mc_tomka_blad(prefixed_codes)
        yield r

def gen_1record_prefixed(record, prefixlen, mc = 'mc'):
    """
    Returns a deep copy of a record that contain fields specified in filtered_by. 
    Returns prefixes of its codes of length prefixlen.
    
    """
    record_new = zblrecord_deep_copy(record)
    prefixed_codes = get_prefixes_list(mc2lmc_tomka_blad(record_new), prefixlen)
    record_new[mc] = lmc2mc_tomka_blad(prefixed_codes)
    return record_new
         
def gen_record_fromshifts(gen_record, shifts):
    """
    Returns records that are in consecutive shifts of gen_record.
    
    TESTED.
    """
    ind = 0
    shift_ind = 0
    for r in gen_record():
        if ind==shifts[shift_ind]:
            yield r
            shift_ind+=1
            if shift_ind>=len(shifts):
                break
        ind+=1

def gen_record_filteredbylabels(gen_record, labels, mc='mc'):
    """
    Returns records, filtering the labels, narrowing them to only those that are amongst labels.
    
    labels - set of labels
    
    Tested.
    """
    for r in gen_record():
        new_mc = list(set(mc2lmc_tomka_blad(r))&labels)
        if new_mc:
            r[mc] = lmc2mc_tomka_blad(new_mc)
            yield r

def gen_record_filteredbyprefix(gen_record, filter_by_prefix, mc='mc'):
    """
    Returns records, filtering the labels, narrowing them to only those that are prefixed by filter_by_prefix.
    
    """
    for r in gen_record():
        new_mc = filter(lambda code: code.startswith(filter_by_prefix), mc2lmc_tomka_blad(r))
        if new_mc:
            new_r = dict(r)
            new_r[mc] = lmc2mc_tomka_blad(new_mc)
            yield new_r



def map_frecords(frecords, record_mapping):
    '''
    Map each record from frecords into some other record according to the record mapping. 
    '''
    for record in frecords():
        yield record_mapping(record)

def extract_curr_level_labels(frecords):
    '''
    Extract labels that sit in frecords
    '''
    code_generator = lambda: gen_lmc(frecords)
    return get_labels_min_occurence(code_generator, 1)#get all the labels, regardless of their occurences counts


if __name__ == "__main__":
    import doctest
    doctest.testmod()
