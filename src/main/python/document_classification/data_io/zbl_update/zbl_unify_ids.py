"""Parses Pseudo-ZBL file and unifies (maps) ZBL ids according to id-mapping file."""

import sys
import os
import re

sys.path.append(r'../')
import zbl_io


#known zbl-id formats:
ZBL10_REGEXP = re.compile("\w\w\w\w.\w\w\w\w\w")
ZBL8_REGEXP = re.compile("\w\w\w\w\w\w\w\w")
ZBLPRE8_REGEXP = re.compile("pre\w\w\w\w\w\w\w\w")

    
class ZblIdMapper:

    def  __init__(self, mapping_path, inverse_mapping = False):
        """inverse_mapping - whether map loaded from file at mapping_path should be inverted or not."""
        file_map = zbl_io.load_map_from_file(open(mapping_path,'r'))
        if inverse_mapping:
            self.ids_map = dict((file_map[key], key) for key in file_map)
        else:
            self.ids_map = file_map
        #used for statistics:
        self.missed_ids = set()
        self.matched_ids = set()
        self.fixed_pre_ids = set()
    
    
    
    def map_zbl_id(self, id):
        """Takes incorrect id and maps it to new id."""
        if self.ids_map.has_key(id):
            self.matched_ids.add(id)
            return self.ids_map[id]
        
        if id.startswith("pre"): #if id is in format preXXXXXXXX
            id = id.replace('pre', '') #than check also XXXXXXXX without pre
            if self.ids_map.has_key(id):
                self.matched_ids.add(id)
                return self.ids_map[id]
            
        self.missed_ids.add(id)
        return None
    
    def fix_id(self, id):
        """Fixes formatting of ZBL-ID (currently it is just removing prefix 'pre')."""
        if id.startswith("pre"):
            id =  id.replace('pre', '')
            self.fixed_pre_ids.add(id)       
        return id
    
    
        
    def update_zbl_record_id(self, record):
        """Updates id format in ID field."""
        if not record.has_key(zbl_io.ZBL_ID_FIELD):
            return record
        id = record[zbl_io.ZBL_ID_FIELD]        
        new_id = self.map_zbl_id(id)
        if not new_id is None:
            record[zbl_io.ZBL_ID_FIELD] = self.fix_id(new_id)        
        record[zbl_io.ZBL_ID_FIELD] = self.fix_id(record[zbl_io.ZBL_ID_FIELD])                
        return record            
    
    def update_zbl_record_no(self, record):
        """Updates id format in ZB field."""
        if not record.has_key("zb"):
            return record
        id = record["zb"]
        new_id = self.map_zbl_id(id)
        if not new_id is None:
            record["zb"] = new_id        
        record["zb"] = self.fix_id(record["zb"])
        return record            
    
    def update_zbl_record_citations(self, record):
        """Updates id format in CI field (citations)."""
        if not record.has_key("ci"):
            return record
               
        #unpacking:  
        cis = zbl_io.unpack_list_of_dictionaries(record["ci"])
            
        #updating:
        for ci in cis:
            if ci.has_key('zbl'):                                
                new_id = self.map_zbl_id(ci['zbl'])
                if not new_id is None:
                    ci['zbl'] = new_id
                ci['zbl'] = self.fix_id(ci['zbl'])
                    
        #packing & overwriting:
        record["ci"] = zbl_io.pack_list_of_dictionaries(cis)
            
        return record  


    def update_record(self, record):
        """Updates id format in record (in all known fields)."""
        record = self.update_zbl_record_id(record)
        record = self.update_zbl_record_no(record)
        record = self.update_zbl_record_citations(record)
        return record
        
        
    def print_ids(self):
        print "-------------------------"   
        print "Matched ids:"
        for id in self.matched_ids:
            print id 
        print "-------------------------"   
        print "Missed ids:"
        for id in self.missed_ids:
            print id
        print "-------------------------"   
        print "Fixed ids:"
        for id in self.fixed_pre_ids:
            print id
        print "--------------------------------------------" 
        
    def print_stats(self):
        print "Matched zbl ids:", len(self.matched_ids)    
        print "Missed zbl ids:", len(self.missed_ids)
        print "Fixed zbl ids:", len(self.fixed_pre_ids)

if __name__ == "__main__":
    print "The program parses Pseudo-ZBL file and unifies ZBL ids according to the id-mapping file"    
        
    try:
        mapping_path = sys.argv[1]
    except:
        print "First argument expected: mapping-file-path (every line in format: src-id dst-id)"        
        sys.exit(-1)
    try:
        in_path = sys.argv[2]
    except:
        print "Second argument expected: input-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)
    try:
        out_path = sys.argv[3]
    except:
        print "Third argument expected: output-zbl-file-path (Pseudo-ZBL)"        
        sys.exit(-1)        
        
    print "mapping_path =", mapping_path
    print "in_path =", in_path
    print "out_path =", out_path


    id_mapper = ZblIdMapper(mapping_path, False)
    fin = open(in_path, 'r')
    fout = open(out_path, 'w')
    for record in zbl_io.read_zbl_records(fin):        
        zbl_io.write_zbl_record(fout, id_mapper.update_record(record))           
        fout.write("\n")               
    fin.close()
    fout.close()
    
    id_mapper.print_stats()
    
   

        
    