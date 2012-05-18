
"""Methods to compare two ZBL records."""

import sys, os
import zbl_io
import text_analysis
import math
import time


def are_elements_almost_equal(a1, a2, max_hist_dist = 4, max_edit_dist = 2):
    """ Returns true iff a1, a2 fulfill following conditions:
    - distance between histograms <= max_hist_dist
    - edit distance <= max_edit_dist 
    
    
    Sample use:
    >>> are_elements_almost_equal('andrzej', 'endrzaj', 4, 2)
    True
    >>> are_elements_almost_equal('andrzej', 'endrzaje', 4, 2)
    False
    >>> are_elements_almost_equal('andrzej', 'endzraj', 4, 2)
    False
    """
    hist_dist = text_analysis.word_hist_diff_total(a1, a2)
    if hist_dist > max_hist_dist:
        #print "a1=",a1,"a2=",a2,"hist_dist=",hist_dist
        return False
    edit_dist = text_analysis.lev(a1, a2)
    if edit_dist > max_edit_dist:
        #print "a1=",a1,"a2=",a2,"edit_dist=",edit_dist
        return False
    return True

def are_lists_almost_equal(au1, au2, max_hist_dist = 4, max_edit_dist = 2):
    """Compares two list of elements. 
    Returns true iff believed to represent equal data i.e. 
    for every pair of elements are kept conditions described in 
    are_elements_almost_equal function.
    
    Sample use:
    >>> are_lists_almost_equal(['ala', 'andrzej'], ['ele', 'endrzaj'], 4, 2)
    True
    >>> are_lists_almost_equal(['ala', 'andrzej'], ['ele', 'endzraj'], 4, 2)
    False
    """
    if len(au1) != len(au2):
        return False
    for (a1, a2) in zip(au1, au2):
        if not are_elements_almost_equal(a1.lower(), a2.lower(), max_hist_dist, max_edit_dist):
            return False
    return True
            
def are_zbl_records_similar(rec1, rec2):
    """Returns true if (we believe that) rec1 describes the same data as rec2.
    
    The same data has the same zbl-id or mr-id or very similar authors and title
    and the same publication year."""
    if rec1.has_key(zbl_io.ZBL_ID_FIELD) and rec2.has_key(zbl_io.ZBL_ID_FIELD):
        if rec1[zbl_io.ZBL_ID_FIELD] == rec2[zbl_io.ZBL_ID_FIELD]:
            return True
    
    if rec1.has_key("zb") and rec2.has_key("zb"):
        return rec1["zb"] == rec2["zb"]
        
    if rec1.has_key("mr") and rec2.has_key("mr"):
        return rec1["mr"] == rec2["mr"]
        
    #if present publication years must agree        
    if rec1.has_key("py") and rec2.has_key("py"):        
        if rec1["py"] != rec2["py"]: 
            return False
    
    if rec1.has_key("au") and rec2.has_key("au"):
        au1 = zbl_io.unpack_multivalue_field(rec1["au"]);
        au2 = zbl_io.unpack_multivalue_field(rec2["au"]);
        if not are_lists_almost_equal(au1, au2, 4, 2):
            return False
    else: #both articles must have authors 
        return False 
            
    #are titles similar?            
    ti1 = rec1.get('ti', '').lower()
    ti2 = rec2.get('ti', '').lower()        
    if not are_elements_almost_equal(ti1, ti2, 6, 4):
        return False                
    
    return True


def is_ci_similar(record, ci):
    """Returns True if (we believe that) record describes the same data as citation ci."""
    return are_zbl_records_similar(record, ci)
       

def select_best_fitting_record(main_zbl_record, candidates, meaning_fields = ['ti', 'au', 'jt', 'py']):
    """From list of candidate records select the most similar 
    (the one with the smallest edit distance on meaning_fields) to main_zbl_record.
    
    >>> select_best_fitting_record({'ti': 'kot', 'jt': 'Koty', 'py': '1991'}, [{'ti': 'koty', 'jt': 'Koty'}, {'ti': 'kota', 'jt': 'Kozy', 'py': '1991'}]) == {'ti': 'koty', 'jt': 'Koty'}
    True
    """
    if len(candidates) == 1:
        return candidates[0]
    #generate subset of fields present in all records:
    fields = set(main_zbl_record.keys())
    for candidate in candidates:
        fields = fields.intersection(candidate.keys())
    #keep relevant fields:
    fields = fields.intersection(set(meaning_fields)) 
    #estimate edit distances for all candidates:
    edit_distances = []
    for candidate in candidates:
        total_edit_distance = 0
        for field in fields:
            edit_distance = text_analysis.lev(candidate[field].lower(), main_zbl_record[field].lower())
            total_edit_distance = total_edit_distance + edit_distance
        edit_distances.append(total_edit_distance)
    #select most similar:    
    most_similar_ix = edit_distances.index(min(edit_distances))
    return candidates[most_similar_ix]


if __name__=="__main__":

    import doctest
    doctest.testmod()   
                