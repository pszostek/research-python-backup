"""Takes two zbl/pseudo-zbl files and mix them into single file."""

import sys, os
import math
import time

sys.path.append(r'../')
sys.path.append(r'../../')
import zbl_io
import tree_reconstruction
from tree_reconstruction import analysis
from tree_reconstruction.analysis import zbl_similarity
from tree_reconstruction.analysis import text_analysis

def _update_zbl_record_history_(main_zbl_record, aux_zbl_record):
    """Updates field <zz> in main_zbl_record basing on its previous value and <zz> value in aux_zbl_record.

    <zz> - field that identifies records's source (should be merged instead of overwriting.)
    """
    if main_zbl_record.has_key("zz") and aux_zbl_record.has_key("zz"): 
        main_zz_list = zbl_io.unpack_multivalue_field(main_zbl_record["zz"])
        aux_zz_list =  zbl_io.unpack_multivalue_field(aux_zbl_record["zz"])
        main_zz_list.extend(aux_zz_list)
        main_zbl_record["zz"] = zbl_io.pack_multivalue_field(main_zz_list)
    return main_zbl_record

def update_zbl_record(main_zbl_record, aux_zbl_record, forced_fields = []):
    """Updates main_zbl_record with aux_zbl_record data.     
        
       Returned (updated) record = main_zbl_record + fields from aux_zbl_record missed in main_zbl_record or fields among forced_fields.
       forced_fields = list of fields to be copied from aux_zbl_record to main_zbl_record even if main_zbl_record already has such field."""    
    for aux_key in aux_zbl_record:
        if not main_zbl_record.has_key(aux_key) or forced_fields.count(aux_key) > 0:
            main_zbl_record[aux_key] = aux_zbl_record[aux_key]    
    return _update_zbl_record_history_(main_zbl_record, aux_zbl_record)


class ZblRecordMatcher:
    """For given record finds best match out of known (aux) records."""
    
    def __init__(self, aux_zbl_path, similarity_op = zbl_similarity.are_zbl_records_similar, sel_fields = ['ti', 'au'], fix_pre_ids = True):
        """aux_zbl_path - zbl-file with (aux) records.
          similarity_op(rec1, rec2) - decides if rec1 is similar to rec2
          sel_fields - list of fields that should be considered when selecting the most similar record to the given      
          fix_pre_ids - True when we try to fix formatting (e.g. by removing 'pre') of ids
        """        
        
        self.fix_ids = fix_pre_ids
        self.similarity_operator = similarity_op
        self.selection_fields = sel_fields
        
        self.aux_zbl_recs_list = zbl_io.load_zbl_file(aux_zbl_path) #list        
        #fix ids:
        for rec in self.aux_zbl_recs_list:
            rec[zbl_io.ZBL_ID_FIELD] = self.__fix_id__(rec[zbl_io.ZBL_ID_FIELD])
        
        self.__init_speed_up_structures__()
        self.__init_match_stats_structures__()

    def __fix_id__(self, id):
        """If self.fix_ids==True then fixes formatting of ZBL-ID (currently it is just removing prefix 'pre')."""
        if not self.fix_ids:
            return id
        if id.startswith("pre"):
            id =  id.replace('pre', '')      
        return id                             
        
    def __init_speed_up_structures__(self):
        #dictionaries {id: record}:        
        self.aux_zbl_recs_id_dict = dict( (rec[zbl_io.ZBL_ID_FIELD], rec) for rec in self.aux_zbl_recs_list ) #dictionary {id: record}
        self.aux_zbl_recs_zb_dict = dict( (rec["zb"], rec) for rec in self.aux_zbl_recs_list if rec.has_key("zb") ) #dictionary {mr: record}
        self.aux_zbl_recs_mr_dict = dict( (rec["mr"], rec) for rec in self.aux_zbl_recs_list if rec.has_key("mr") ) #dictionary {mr: record}                                
        #list of records without year set
        self.aux_zbl_recs_list_no_py = [rec for rec in self.aux_zbl_recs_list if not rec.has_key("py")]
        #dictionary{year:list of records}
        self.aux_zbl_recs_dict_py = {}
        for rec in self.aux_zbl_recs_list:
            if rec.has_key("py"):
                year = rec["py"]
                if not self.aux_zbl_recs_dict_py.has_key(year):
                    self.aux_zbl_recs_dict_py[year] = []
                self.aux_zbl_recs_dict_py[year].append(rec)   


    def __init_match_stats_structures__(self):
        # self.match_aux_record results:
        self.matched_on_id = set()
        self.matched_on_zb = set()
        self.matched_on_mr = set()
        self.matched_on_similarity = set()
        self.missed = set()
        self.aux_used_ids = set()
        
        
    def total_processed_records_num(self):
        """Returns how many times match_aux_record were invoked."""
        return len(self.missed)+len(self.matched_on_similarity)+len(self.matched_on_mr)+len(self.matched_on_zb)+len(self.matched_on_id)

    def total_matched_records_num(self):
        """Return number of all matched records."""
        return self.total_processed_records_num() - len(self.missed) 
    
    def print_report(self):        
        print "-----------------------------------"
        print "Processed records:", self.total_processed_records_num()
        print "Matched records:", self.total_matched_records_num()
        print " - on id:", len(self.matched_on_id)
        print " - on zb:", len(self.matched_on_zb)
        print " - on mr:", len(self.matched_on_mr)
        print " - on similarity:", len(self.matched_on_similarity)
        print "Missed records:", len(self.missed)
        print "Used aux records:", len(self.aux_used_ids)
        if len(self.aux_used_ids) != self.total_matched_records_num():
            print "Warning: Used aux records != Matched records"
            print "It means that some records were matched more than one time"
        print "-----------------------------------"
        
    def print_py_report(self):
        """Prints report on py (publication year) distribution among loaded (aux) records."""
        print "-----------------------------------"
        print "Year ?:", len(self.aux_zbl_recs_list_no_py)
        total = 0
        for year in sorted(self.aux_zbl_recs_dict_py.keys()):
            count_in_year = len(self.aux_zbl_recs_dict_py[year])
            total = total + count_in_year
            print "Year",year,":", count_in_year
        print "Total with year set:", total
        print "-----------------------------------"
        
    def print_ids_stats(self):
        print "-----------------------------------"
        print "matched_on_id"
        for id in self.matched_on_id:
            print id
        print "-------------------------"    
        print "matched_on_zb"
        for id in self.matched_on_zb:
            print id
        print "-------------------------"
        print "matched_on_mr"
        for id in self.matched_on_mr:
            print id
        print "-------------------------"
        print "matched_on_similarity"
        for id in self.matched_on_similarity:            
            print id
        print "-------------------------"
        print "missed"
        for id in self.missed:
            print id
        print "-------------------------"
        print "aux_used_ids"
        for id in self.aux_used_ids:
            print id
        print "-------------------------"
        print "-----------------------------------"
        
    def append_not_matched_records(self, fout):
        """Appends to fout all loaded (aux) records that have never been matched in self.match_aux_record.
        
        Returns number of records appended.
        """
        counter = 0
        for rec in self.aux_zbl_recs_list:
            if not rec[zbl_io.ZBL_ID_FIELD] in self.aux_used_ids:
                zbl_io.write_zbl_record(fout, rec)  
                fout.write("\n")
                counter = counter + 1
        return counter                                   
    
    def find_most_similar_zbl_record(self, main_zbl_record):
        """Walks through the list of loaded (self.aux_zbl_recs_list) 
        (aux) records and searches for zbl record 
        that self.similarity_operator(rec1, rec2) states as similar to main_zbl_record.
        If more than one found then the most similar is selected.
        The most similar means the one that has the smallest edit distance calculated on self.selection_fields."""
        
        candidates = []    
        if main_zbl_record.has_key("py"):
            #check all publications with this year:
            for aux_zbl_record in self.aux_zbl_recs_dict_py.get(main_zbl_record["py"], []):
                if self.similarity_operator(main_zbl_record, aux_zbl_record):
                    candidates.append(aux_zbl_record)
            #check all the publications without year:                    
            for aux_zbl_record in self.aux_zbl_recs_list_no_py:
                if self.similarity_operator(main_zbl_record, aux_zbl_record):
                    candidates.append(aux_zbl_record)
        else:
            #check all the publications
            for aux_zbl_record in self.aux_zbl_recs_list:
                if self.similarity_operator(main_zbl_record, aux_zbl_record):
                    candidates.append(aux_zbl_record)
                                
        if len(candidates) == 0:
            return None        
        
        matching_record = zbl_similarity.select_best_fitting_record(main_zbl_record, candidates, self.selection_fields)
        #print "[find_most_similar_zbl_record] matching:", main_zbl_record[zbl_io.ZBL_ID_FIELD], "&", matching_record[zbl_io.ZBL_ID_FIELD], "out of", [r[zbl_io.ZBL_ID_FIELD] for r in candidates]
        return matching_record
    
    
    def match_aux_record(self, main_zbl_record, only_fast_match_methods = True):
        """For given main_zbl_record finds best match among loaded (aux) records (if nothing is close enough None returned)."""
        #print "Entering: match_aux_record"
                
        id = self.__fix_id__(main_zbl_record[zbl_io.ZBL_ID_FIELD])
           
        if self.aux_zbl_recs_id_dict.has_key(id):
            aux_zbl_record = self.aux_zbl_recs_id_dict[id]
            self.matched_on_id.add(id)
        elif main_zbl_record.has_key("zb") and self.aux_zbl_recs_zb_dict.has_key(main_zbl_record["zb"]):
            aux_zbl_record = self.aux_zbl_recs_zb_dict[ main_zbl_record["zb"] ]
            self.matched_on_zb.add(id)
        elif main_zbl_record.has_key("mr") and self.aux_zbl_recs_mr_dict.has_key(main_zbl_record["mr"]):
            aux_zbl_record = self.aux_zbl_recs_mr_dict[ main_zbl_record["mr"] ]
            self.matched_on_mr.add(id)
        elif not only_fast_match_methods:                    
            aux_zbl_record = self.find_most_similar_zbl_record(main_zbl_record)
            if not aux_zbl_record is None:
                self.matched_on_similarity.add(id)
        else: 
            aux_zbl_record = None
            
        if aux_zbl_record is None:
            self.missed.add(id)
        else:
            self.aux_used_ids.add(aux_zbl_record[zbl_io.ZBL_ID_FIELD])

        #print "Leaving: match_aux_record"
        return aux_zbl_record
    




if __name__=="__main__":
    print "The program parses Pseudo-ZBL files: appends second one (auxiliary) to the first one (main)."  
      
    import doctest
    doctest.testmod()   
        
    try:
        main_zbl_path = sys.argv[1]
    except:
        print "First argument expected: main-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)
    try:
        aux_zbl_path = sys.argv[2]
    except:
        print "Second argument expected: auxiliary-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)
    try:
        out_path = sys.argv[3]
    except:
        print "Third argument expected: output-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)        
    try:
        #which fields should be copied from aux records anyway
        forced_fields = sys.argv[4].split(',')      
    except:
        forced_fields = ["mc"]    
    try:
        #what to do with aux records that have not been matched
        append_not_matched_records_flag = bool(int(sys.argv[5]))
    except:
        append_not_matched_records_flag = True             
    try:
        #if only indexes should be used or similar-record searching is also ok
        only_fast_match_methods = bool(int(sys.argv[6]))
    except:     
        only_fast_match_methods = True
    try:
        #should we remove 'pre' in zbl-ids?
        try_fixing_ids = bool(int(sys.argv[7]))
    except:     
        try_fixing_ids = True
    
    print "-----------------------------------"
    print "Forced fields =", forced_fields
    print "Append Not Matched Records Flag =", append_not_matched_records_flag
    print "Only fast matching methods = ", only_fast_match_methods
    print "Trying to fix ids = ", try_fixing_ids
    
    print "Loading auxiliary file =",  aux_zbl_path
    zbl_matcher = ZblRecordMatcher(aux_zbl_path, zbl_similarity.are_zbl_records_similar, ['ti', 'au'], try_fixing_ids)
    print len(zbl_matcher.aux_zbl_recs_list), "zbl records loaded." 

    print "Opening main file =",  main_zbl_path
    fmain = open(main_zbl_path, 'r') 

    print "Opening output file =",  out_path  
    fout = open(out_path, 'w')

    print "-----------------------------------"
    zbl_matcher.print_py_report()
    print "-----------------------------------"

    ######################################################################################################
    #mix records from two files:
    start_time = time.clock()
    for main_zbl_record in zbl_io.read_zbl_records(fmain):       

        aux_zbl_record = zbl_matcher.match_aux_record(main_zbl_record, only_fast_match_methods)                        
        if not aux_zbl_record is None: #mix two records:                                        
            main_zbl_record = update_zbl_record(main_zbl_record, aux_zbl_record, forced_fields)
            
        #write results:    
        zbl_io.write_zbl_record(fout, main_zbl_record)  
        fout.write("\n")
        
        #progress bar:   
        main_counter = zbl_matcher.total_processed_records_num()
        matched_counter = zbl_matcher.total_matched_records_num()
        if main_counter%10000 == 0:
            print (time.clock() - start_time),"s - ",main_counter, "processed,",matched_counter,"matched"
           
    ######################################################################################################
    if append_not_matched_records_flag:                   
        print zbl_matcher.append_not_matched_records(fout), " appended not matched records..."
                    
    fmain.close()
    fout.close()
    
    #zbl_matcher.print_ids_stats()
    zbl_matcher.print_report()
    
    
