"""Package of functions for reading and parsing ZBL-txt files."""
import codecs

    
ZBL_ID_FIELD = 'an'
    
MULTIVAL_FIELD_SEPARATOR = '\t;\t'
MULTIVAL_FIELD_SEPARATOR2 = '\t,\t'
DICT_FIELD_SEPARATOR = ': '
    
BAD_MULTIVAL_FIELD_ENDINGS = ['\t;','\t,']
        
def unpack_multivalue_field(strval, field_separator = MULTIVAL_FIELD_SEPARATOR, bad_endings = BAD_MULTIVAL_FIELD_ENDINGS):
    """Takes field that contains many values and splits it into list.
    
    Sample use:
    >>> unpack_multivalue_field('first val\t;\tsecond val\t;\t')
    ['first val', 'second val']    
    >>> unpack_multivalue_field('first val\t;\tsecond val')
    ['first val', 'second val']
    """    
    for bad_ending in bad_endings: #filter bad endings
        if strval.endswith(bad_ending):
            strval = strval[0:(len(strval)-len(bad_ending))]
            
    vals = strval.split(field_separator)
    return _filter_last_empty_(vals)
    
def unpack_dictionary_field(strdict):    
    """Extracts dictionary from single string.
    
    Sample use:
    >>> unpack_dictionary_field("a:A\t,\tb:B\t,\tc:C\t,\t")
    {'a':'A', 'b':'B', 'c':'C'}
    """
    strpairs = unpack_multivalue_field(strdict, MULTIVAL_FIELD_SEPARATOR2)
    dict = {}
    for strpair in strpairs:
         div_ix = strpair.find(DICT_FIELD_SEPARATOR)
         key = strpair[0:div_ix].strip()
         val = strpair[(div_ix+1):len(strpair)].strip()
         dict[key] = val
    return dict

        
def unpack_listpairs_field(strdict):    
    """Extracts list of pairs from single string."""
    strpairs = unpack_multivalue_field(strdict, MULTIVAL_FIELD_SEPARATOR2)
    lp = []
    for strpair in strpairs:
         div_ix = strpair.find(DICT_FIELD_SEPARATOR)
         key = strpair[0:div_ix].strip()
         val = strpair[(div_ix+1):len(strpair)].strip()
         lp.append( (key,val) )
    return lp



def pack_multivalue_field(vals, field_separator = MULTIVAL_FIELD_SEPARATOR):
    """Takes list of many values and packs it into single string.
    
    Sample use:
    >>> pack_multivalue_field(['a','b','c'])
    'a\t;\tb\t;\tc'
    """
    return reduce(lambda x,y: str(x)+field_separator+str(y), vals)

def pack_dictionary_field(dict):    
    """Takes dictionary and packs it into single string.
    
    Sample use:
    >>> pack_dictionary_field({1:11, 2:22})
     '1:11\t,\t2:22'
    """
    return pack_multivalue_field( (str(key)+DICT_FIELD_SEPARATOR+str(dict[key]) for key in dict), MULTIVAL_FIELD_SEPARATOR2)


def pack_listpairs_field(lp):    
    """Takes list of pairs and packs it into single string."""
    return pack_multivalue_field( (str(key)+DICT_FIELD_SEPARATOR+str(val) for key,val in lp), MULTIVAL_FIELD_SEPARATOR2)


def unpack_list_of_dictionaries(packed_str):
    """See: unpack_dictionary_field & unpack_multivalue_field"""
    ci_in_strs = unpack_multivalue_field(packed_str)
    cis = []
    for dictstr in ci_in_strs:
        ci = unpack_dictionary_field(dictstr)            
        cis.append(ci)
    return cis

def pack_list_of_dictionaries(cis):
    """See: pack_dictionary_field & pack_multivalue_field"""
    ci_out_strs = []
    for ci in cis:
        dictstr = pack_dictionary_field(ci)
        ci_out_strs.append(dictstr)
    return pack_multivalue_field(ci_out_strs)


def find_file_map_value(f, expected_key):
    """Parses file f (every line in format: key value - space between key and value) 
    and finds value that matches expected_key."""
    for line in f.xreadlines():
        div_pos = line.find(' ')
        key = line[0:div_pos].strip()
        val = line[div_pos+1: len(line)].strip()
        if key == expected_key:
            return val
    return None

def find_file_path_map_value(path, expected_key):
    """See: find_file_map_value"""
    return find_file_map_value(open(path, 'r'), expected_key)

def find_file_map_key(f, expected_value):
    """Parses file f (every line in format: key value - space between key and value) 
    and finds key that matches expected_value."""
    for line in f.xreadlines():
        div_pos = line.find(' ')
        key = line[0:div_pos].strip()
        val = line[div_pos+1: len(line)].strip()
        if val == expected_value:
            return key
    return None
    
def find_file_path_map_key(path, expected_value):
    """See: find_file_map_key"""
    return find_file_map_key(open(path, 'r'), expected_value)

def load_map_from_file(f):
    """Parses file f (every line in format: key value - space between key and value) 
    and builds dictionary out of it."""
    map = {}
    for line in f.xreadlines():
        div_pos = line.find(' ')
        key = line[0:div_pos].strip()
        val = line[div_pos+1: len(line)].strip()
        map[key] = val
    return map
    
def open_file(path, uni = False):
    if uni:
        return codecs.open(path, "r", "utf-8")
    else:
        return open(path, "r")
    
def read_zbl_records(f, uni = False):
    """Generates records of ZBL data from stream (file) f."""
    record = {}
    for line in f.xreadlines():  
        if len(line.strip()) <= 1: #skip empty lines
            continue
                              
        division = line.find(" ")
        key = line[0:division].strip()
        if uni: 
            value = unicode(line[division:].strip(), errors="ignore")
        else:
            value = line[division:].strip()        
        if key == ZBL_ID_FIELD and record != {}:
            yield record
            record = {}
        record[key] = value        
        
    if record != {}:
        yield record
        
def read_zbl_records_id(f, field_vals, field_name = ZBL_ID_FIELD):
    """Reads records from stream (file) f and returns list of these records 
    for which record[field_name] belongs to field_vals."""
    field_vals = set(field_vals)
    found = []
    for record in read_zbl_records(f):        
        if record.has_key(field_name) and record[field_name] in field_vals:
            found.append(record)
    return found
        
def read_zbl_records_filtered(f, filter):
    """Reads records from stream (file) f and returns list of these records 
    for which filter(record) returns True."""    
    found = []
    for record in read_zbl_records(f):        
        if filter(record):
            found.append(record)
    return found

def load_identifiers(file):
    """Loads from file set of ZBL identifiers of all found records."""
    ids = set()
    for record in read_zbl_records(file):
        ids.add(record[ZBL_ID_FIELD])
    return ids        
        
def build_map_of_fields(file, src_field, dst_field):
    """Loads from file set of ZBL records and basing on them builds map {record[src_field]: record[src_dst_field]}."""    
    map = {}    
    for record in read_zbl_records(file):        
        if record.has_key(src_field) and record.has_key(dst_field) :
            map[ record[src_field] ] = record[dst_field]
    return map        

def load_zbl_file(path):
    """Returns list of zbl records loaded from file of given path."""    
    return list( read_zbl_records( open(path, 'r') ) )

def __write_zbl_field__(f, key, val):
    f.write(key+"  "+val+"\n")


def write_zbl_record(f, record):
    """Writes single ZBL record to file f."""
    __write_zbl_field__(f, ZBL_ID_FIELD, record[ZBL_ID_FIELD])
    for field_name in record:
        if field_name != ZBL_ID_FIELD:
            __write_zbl_field__(f, field_name, record[field_name])

def write_zbl_records(f, records):
    """Writes ZBL records to file f."""
    for record in records:
        write_zbl_record(f, record)
        
def _filter_last_empty_(vec):
    """Removes last empty element in the list vec."""
    if len(vec) == 0:
        return vec    
    last = vec[len(vec)-1]
    if last is None or len(last) <= 0:
        vec.pop();
    return vec    
    
if __name__ == "__main__":

    import doctest
    doctest.testmod()   
    
    
