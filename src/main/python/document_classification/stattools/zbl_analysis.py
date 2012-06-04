"""Simple analysis (statistics) of ZBL files."""
import math
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import re
import sys

sys.path.append(r'../')
from data_io import zbl_io
from tools import msc_processing
from tools.msc_processing import count_msc_occurences
from tools import stats
from tools.stats import avg
from tools.stats import std

 
##############################################################################################

def allow_all_filter(record):
    """Filter that allows all ZBL records (always returns True)."""
    return True


def has_record_fields(record, required_fields):
    """Returns True if record has all the required_fields."""
    num_record_fields = sum(1 for field in required_fields if record.has_key(field))
    return len(required_fields) == num_record_fields          

def count_occurrences(file, required_fields, records_filter = allow_all_filter):
    """Counts records in ZBL file that have all fields from required_fields (and were admitted by filter).
    
    records_filter(record) - should return True if record is admitted"""        
    occurrences = 0    
    for record in zbl_io.read_zbl_records(file):
        if not records_filter(record):
            continue #filter does not allow
        if has_record_fields(record, required_fields):
            occurrences = occurrences + 1
    return occurrences
                  


##############################################################################################


def draw_occur_hist(counts, zoom_out=100, title='', xlabel='Value', ylabel='Count'):
    """Takes dictionary {name: count} and draws histogram."""
    n, bins, patches = plt.hist(counts.values(), len(counts)/zoom_out, normed=False, alpha=0.75)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)    
    plt.show()
    
def print_counts(counts):
    """Takes dictionary {name: count} and prints in desc order."""
    counts = sorted(((b,a) for a,b in counts.iteritems()), reverse=True)
    for count,name in counts:
        print count,"\t",name
        
def filter_counts(counts, pattern):
    """Returns sub-dictionary of dictionary{name: count} that contains
    names matching pattern."""
    regexp = re.compile(pattern)
    return dict( c for c in counts.iteritems() if bool(regexp.match(c[0])) )
                  
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################            
             
def _report_counts_(counts, label = None):
    """Prints report on count statistics (counts = dictionary{name:count}/list of numbers )."""
    try:
        counts = counts.values()
    except:
        pass
    
    if not label is None:
        print label        
    print " Max:", max(counts)
    print " Min:", min(counts)
    try:
        print " Avg:", round(avg(counts),2)        
    except:
        print " Avg: -"        
    try:
        print " Std:", round(std(counts),2)
    except:
        print " Std: -"
    print " Total num of categories:", len(counts)
    #ile mamy kategorii ktora wystepuje tyle a tyle razy
    print " <5:", sum(1 for c in counts if c<5)
    print " <10:", sum(1 for c in counts if c<10)
    print " <25:", sum(1 for c in counts if c<25)
    print " <50:", sum(1 for c in counts if c<50)
    print " <100:", sum(1 for c in counts if c<100)
    print " <1000:", sum(1 for c in counts if c<1000)
    print " <10000:", sum(1 for c in counts if c<10000)
                 
             
def _report_ci_(path, records_filter = allow_all_filter, \
                ci_dst_records_filter = allow_all_filter, \
                uq_id_field_name = zbl_io.ZBL_ID_FIELD):
    """Prints report about citations in ZBL file.
    
    records_filter(record) - should return True if record is admitted
    ci_dst_records_filter(record) -  should return True if record that citation is pointing at is admitted
    uq_id_field_name - name of a field that uniquely identifies record 
    """
    #wczytywanie zbioru na ktory moga wskazywac cytowania:
    print "Loading ids of records that may be citation destination."
    dst_records_ids = set()
    for i,record in enumerate( zbl_io.read_zbl_records(open(path)) ):
        if i%100000 == 0: print i," records considered" #progress bar
        if record.has_key(uq_id_field_name) and ci_dst_records_filter(record):
            dst_records_ids.add(record[uq_id_field_name])            
    print "Done.", len(dst_records_ids), " records loaded."
    
    #statystyki:
    cis_len = [] #liczba cytowan
    cis_matched = [] #liczba cytowan ktore trafiaja w zadany zbior 
    
    for i,record in enumerate(zbl_io.read_zbl_records(open(path))):
        if i%100000 == 0: print i," records considered" #progress bar
        if not record.has_key("ci") or not records_filter(record):
            continue
                
        cis                 = zbl_io.unpack_list_of_dictionaries(record["ci"])
        #identyfikatory cytowan:
        identified_ci_ids   = list(ci[uq_id_field_name] for ci in cis if ci.has_key(uq_id_field_name))
        #rekordy dopsowane do cytowan i w zadanym zbiorze:
        filtered_matched_records = list(id for id in identified_ci_ids if id in dst_records_ids)
                                         
        cis_len.append(len(cis))
        cis_matched.append(len(filtered_matched_records))
      
    cis_matched_div_len = list( float(m)/float(l) for m,l in zip(cis_matched, cis_len) )
        
    print "Citation statistics (only on records with citations) [total, min avg max std]: "
    print "-Number of citations :", "\t", round(sum(cis_len),0), "\t", round(min(cis_len),0), "\t", round(avg(cis_len),2), "\t", round(max(cis_len),0), "\t", round(std(cis_len),2)
    print "-Matching citations:",  "\t", round(sum(cis_matched),0), "\t", round(min(cis_matched),0), "\t", round(avg(cis_matched),2), "\t", round(max(cis_matched),0), "\t", round(std(cis_matched),2)
    print "-Fraction of matching citations: - ",  "\t", round(min(cis_matched_div_len),3), "\t", round(avg(cis_matched_div_len),3), "\t", round(max(cis_matched_div_len),3), "\t", round(std(cis_matched_div_len),3)
    print "-Total Number of citations/Matching citations:", "\t", round(float(sum(cis_matched))/sum(cis_len),3)    
    print "->", round(sum(cis_len),0), (max(cis_len)), round(avg(cis_len),2), round(std(cis_len),2), \
     round(sum(cis_matched),0), (max(cis_matched)), round(avg(cis_matched),2), round(std(cis_matched),2), \
      round(max(cis_matched_div_len),3), round(avg(cis_matched_div_len),3), round(std(cis_matched_div_len),3) 
    
    cis_matched_hist = {}
    for i in xrange(0, max(cis_matched)+1):
        cis_matched_hist[i] = sum(1 for c in cis_matched if c==i)
    print "Histogram:", cis_matched_hist
    
    n, bins, patches = plt.hist(sorted(cis_matched), bins = max(cis_matched), normed=False, alpha=0.75)
    plt.xlabel("Liczba dopasowanych cytowan")
    plt.ylabel("Liczba rekordow")    
    plt.show()     
                
           
           
             
def _report_af_quality_(path, records_filter = allow_all_filter):
    """Prints report about authors' identities quality."""    
    afs_len = []
    afs_ok_len = []
    
    for i,record in enumerate(zbl_io.read_zbl_records(open(path))):
        if i%100000 == 0: print i," records considered" #progress bar
        if not record.has_key("af") or not records_filter(record):
            continue        
        
        afs = zbl_io.unpack_multivalue_field(record["af"])
        afs_ok = list( af for af in afs if af!='-' )
        
        afs_len.append(len(afs))
        afs_ok_len.append(len(afs_ok))
        
    afs_ok_frac = list( float(m)/float(l) for m,l in zip(afs_ok_len, afs_len) )    
        
    print max(afs_len), "\n", round(avg(afs_len),2), "\n", round(std(afs_len),2)
    print max(afs_ok_len), "\n", round(avg(afs_ok_len),2), "\n", round(std(afs_ok_len),2)
    print round(max(afs_ok_frac),2), "\n", round(avg(afs_ok_frac),2), "\n", round(std(afs_ok_frac),2)
    

    
def _draw_af_hist_(path, records_filter = allow_all_filter):
    """Draws histogram of authorship."""    
    af_count = {} #dict{author: count}
    
    for i,record in enumerate(zbl_io.read_zbl_records(open(path))):
        if i%100000 == 0: print i," records considered" #progress bar
        if not record.has_key("af") or not records_filter(record):
            continue        
        
        afs = zbl_io.unpack_multivalue_field(record["af"])
        afs_ok = list( af for af in afs if af!='-' )
        
        for af in afs_ok:
            af_count[af] = af_count.get(af, 0) + 1
             
    print len(af_count), " authors found."
    print max(af_count.values()), " = max"
    print min(af_count.values()), " = min"
    avg_af_values = avg(af_count.values())
    print round(avg_af_values, 2), " = avg"
    print round(std(af_count.values()), 2), " = std"
    print sum(1 for af in af_count.values() if af > avg_af_values) , " authors above avg"
    print sum(1 for af in af_count.values() if af < avg_af_values) , " authors below avg"
    
    n, bins, patches = plt.hist(af_count.values(), bins = max(af_count.values()), normed=False, log=True, alpha=0.75)
    plt.xlabel("Liczba wystapien w rekordach")
    plt.ylabel("Liczba autorow")    
    plt.show()     
    
                
def _draw_mc_hist(path, records_filter = allow_all_filter):
    """Draws histogram of MSC codes occurrence in records."""    
    mc_counts = []
    
    for i,record in enumerate(zbl_io.read_zbl_records(open(path))):
        if i%100000 == 0: print i," records considered" #progress bar
        if not record.has_key("mc") or not records_filter(record):
            continue          
        
        mc = zbl_io.unpack_multivalue_field(record["mc"])
        mc_counts.append(len(mc))
        
    print len(mc_counts), " record found."
    print max(mc_counts), " = max"
    print min(mc_counts), " = min"
    print round(avg(mc_counts), 2), " = avg"
    print round(std(mc_counts), 2), " = std"
    n, bins, patches = plt.hist(mc_counts, bins = max(mc_counts), normed=False, alpha=0.75)
    plt.xlabel("Liczba kodow MSC w rekordzie")
    plt.ylabel("Liczba rekordow")    
    plt.show()                  
                         
def _report_fields_(path, required_fields):
    """Prints report: counts of records with all the required_fields from ZBL file (path)."""    
    print "Number of records that have", required_fields, "fields:", count_occurrences(open(path), required_fields)
                 
                 
def _report_msc_counts_(path, selected_fields):  
    """Prints report on MSC distribution among records that have fields from selected_fields."""  
    msc_counts = count_msc_occurences(open(path), lambda record: has_record_fields(record, selected_fields))
    msc_counts = dict( (n.upper(), c) for n,c in msc_counts.iteritems() ) #To upper case
    
    msc_counts_lp = filter_counts(msc_counts, msc_processing.MSC_LEAF_PATTERN)
    msc_counts_olp = filter_counts(msc_counts, msc_processing.MSC_ORDINARY_LEAF_PATTERN)
    msc_counts_slp = filter_counts(msc_counts, msc_processing.MSC_SPECIAL_LEAF_PATTERN)
    
    msc_counts_sl = filter_counts(msc_counts, msc_processing.MSC_SECOND_LEVEL)
    msc_counts_osl = filter_counts(msc_counts, msc_processing.MSC_ORDINARY_SECOND_LEVEL)
    msc_counts_ssl = filter_counts(msc_counts, msc_processing.MSC_SPECIAL_SECOND_LEVEL)
    
    #############################################
    
    #draw_occur_hist(msc_counts, zoom_out=100, title='Histogram liczby wystapien kategorii w rekordach', xlabel='Ranga kategorii', ylabel='Liczba wystapien w rekordach')
    
    n, bins, patches = plt.hist(msc_counts.values(), len(msc_counts)/100, log=True, normed=False, alpha=0.75)
    plt.xlabel("Ranga kategorii")
    plt.ylabel("Liczba wystapien w rekordach")    
    plt.show()
    
    _report_counts_(msc_counts, "--All categories:--")
    _report_counts_(msc_counts_lp, "--MSC_LEAF_PATTERN:--")
    _report_counts_(msc_counts_olp, "--MSC_ORDINARY_LEAF_PATTERN:--")
    _report_counts_(msc_counts_slp, "--MSC_SPECIAL_LEAF_PATTERN:--")
    _report_counts_(msc_counts_sl, "--MSC_SECOND_LEVEL:--")
    _report_counts_(msc_counts_osl, "--MSC_ORDINARY_SECOND_LEVEL:--")
    _report_counts_(msc_counts_ssl, "--MSC_SPECIAL_SECOND_LEVEL:--")
    #print_counts(msc_counts)
    
    #############################################

                             

if __name__=="__main__":
    print "The program parses Pseudo-ZBL and generates statistics."  
      
    import doctest
    doctest.testmod()   
        
    try:
        path = sys.argv[1]
    except:
        print "First argument expected: main-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)
    try:
        selected_fields = sys.argv[2].replace('\'', '').split(',')
    except:
        print "Second argument expected: list of fields to be considered. Using default."
        selected_fields = [zbl_io.ZBL_ID_FIELD]
    try:
        ci_dst_fields = sys.argv[3].replace('\'', '').split(',')
    except:
        print "Third argument expected: list of fields"  
        print " that record must have to be considered as citation destination. Using default."
        ci_dst_fields = [zbl_io.ZBL_ID_FIELD]        
    
    print "------------------------------------------------"
    print "Input file =",  path
    print "Fields that record must have to be considered =", selected_fields
    print "Fields that record must have to be citation destination = ", ci_dst_fields
    print "------------------------------------------------"
    
            
    #print "------------------------------------------------"
    #ids = zbl_io.load_identifiers(open(path))
    #print "Total number of records:", len(ids)
    
    #print "------------------------------------------------"
    #_report_fields_(path, selected_fields);
    
    print "------------------------------------------------"
    _report_msc_counts_(path, selected_fields)
    
    #print "------------------------------------------------"
    #print "CI_DST_FIELDS = ", ci_dst_fields
    #_report_ci_(path, \
    #            records_filter = lambda record: has_record_fields(record, selected_fields), \
    #            ci_dst_records_filter = lambda record: has_record_fields(record, ci_dst_fields))
    #print "CI_DST_FIELDS = ", selected_fields  
    #_report_ci_(path, \
    #            records_filter = lambda record: has_record_fields(record, selected_fields), \
    #            ci_dst_records_filter = lambda record: has_record_fields(record, selected_fields))
    
    #print "------------------------------------------------"
    #print "Authors identity (af) quality:"
    #_report_af_quality_(path, records_filter = lambda record: has_record_fields(record, selected_fields)) 
    #_draw_af_hist_(path, records_filter = lambda record: has_record_fields(record, selected_fields))
    
    #print "-----------------------------------------------"
    #print "MSC codes (mc) per record:"
    #_draw_mc_hist(path, records_filter = allow_all_filter)
    
    print "------------------------------------------------"
    