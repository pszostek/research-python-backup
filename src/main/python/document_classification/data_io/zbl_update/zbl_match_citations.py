"""Parses Pseudo-ZBL file (meta-data corpus) and for every citation found 
tries to match record (adds field <an> to citations)."""

import sys
sys.path.append(r'../')
sys.path.append(r'../../')
import zbl_io
import tree_reconstruction
from tree_reconstruction import analysis
from tree_reconstruction.analysis import zbl_similarity
import time

class CitationMatcher:
    
    def __init__(self, zbl_path, sim_op = zbl_similarity.is_ci_similar, sel_fields = ["ti", "au"]):
        self.main_zbl_path = zbl_path
        
        print "Building map zbl-id -> record-id..."
        self.zbl_to_id_map = zbl_io.build_map_of_fields(open(self.main_zbl_path), "zb", "an")
        print len(self.zbl_to_id_map), "loaded..." 
        print "Building map mr-id -> record-id..."
        self.mr_to_id_map = zbl_io.build_map_of_fields(open(self.main_zbl_path), "mr", "an")
        print len(self.mr_to_id_map), "loaded..."
        
        self.similarity_operator = sim_op
        self.selection_fields = sel_fields
        
        self.missed = 0
        self.matched = 0
        
    def __match_identity_on_id__(self, ci):
        if ci.has_key('mr'):                                
            mr_id = ci['mr']
            if self.mr_to_id_map.has_key(mr_id):
                ci[zbl_io.ZBL_ID_FIELD] = self.mr_to_id_map[mr_id]
                
        if ci.has_key('zbl'):                                
            zbl_id = ci['zbl']
            if self.zbl_to_id_map.has_key(zbl_id):
                ci[zbl_io.ZBL_ID_FIELD] = self.zbl_to_id_map[zbl_id]                        
                
        if ci.has_key('zb'):                                
            zbl_id = ci['zb']
            if self.zbl_to_id_map.has_key(zbl_id):
                ci[zbl_io.ZBL_ID_FIELD] = self.zbl_to_id_map[zbl_id]   
        
    
    def add_citation_identity(self, ci, only_fast_match_methods = True):
        """According to records in ZBL file (self.main_zbl_path) and id-maps (self.mr_to_id_map, self.zbl_to_id_map)
            tries to assign identity (<an> field) to citation (given as a dictionary)."""            
        self.__match_identity_on_id__(ci)
                
        if ci.has_key(zbl_io.ZBL_ID_FIELD):
            #print "Assigning to citation [ID/ZBL/MR]:", ci[zbl_io.ZBL_ID_FIELD]
            self.matched = self.matched + 1 
            return ci        
        elif only_fast_match_methods: 
            self.missed = self.missed + 1
            return ci
        
        candidates = []  
        f = open(self.main_zbl_path, 'r')
        for record in zbl_io.read_zbl_records(f):
            if ci.has_key("py") and record.has_key("py"):
                if ci["py"] != record["py"]:
                    continue
            if self.similarity_operator(record, ci):
                candidates.append(aux_zbl_record)                                                                    
        f.close()
        
        if len(candidates) == 0:           
            self.missed = self.missed + 1               
            return ci    
        
        matching_record = zbl_similarity.select_best_fitting_record(ci, candidates, self.selection_fields)  
        ci[zbl_io.ZBL_ID_FIELD] =  matching_record[zbl_io.ZBL_ID_FIELD]
        #print "Assigning to citation [SIMILARITY]:", ci[zbl_io.ZBL_ID_FIELD]
        self.matched = self.matched + 1 
        return ci



if __name__=="__main__":
    print "The program Parses Pseudo-ZBL file (meta-data corpus)"
    print "and for every citation found tries to match record" 
    print "(adds field <an> to citations)."  
      
    import doctest
    doctest.testmod()   
        
    try:
        main_zbl_path = sys.argv[1]
    except:
        print "First argument expected: main-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)
    try:
        out_path = sys.argv[2]
    except:
        print "Second argument expected: output-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)       
        
    print "src = ", main_zbl_path
    print "dst = ", out_path

    cimatch = CitationMatcher(main_zbl_path)
        
    fout = open(out_path, "w")
    main_counter = 0
    start_time = time.clock()
    for record in zbl_io.read_zbl_records( open(main_zbl_path, 'r') ):
        #update citations:
        if record.has_key("ci"):            
            cis = zbl_io.unpack_list_of_dictionaries(record["ci"])                            
            for ci in cis:
                ci = cimatch.add_citation_identity(ci)                                     
            record["ci"] = zbl_io.pack_list_of_dictionaries(cis)                                    
        #write output:
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
        #progress bar:
        if main_counter%10000 == 0:
            print (time.clock() - start_time),"s - ",main_counter, "processed,", (cimatch.matched),"matched",(cimatch.missed),"missed"
        main_counter = main_counter + 1         
    fout.close()
    
    print "missed=",(cimatch.missed)
    print "matched=",(cimatch.matched)
    
