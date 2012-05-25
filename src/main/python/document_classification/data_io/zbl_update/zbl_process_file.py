"""Processes ZBL file by modifying every record according to rules."""

import sys, pickle
import tempfile                 

sys.path.append(r'../')
import zbl_io

sys.path.append(r'../../')
import logging

from tools import msc_processing

import tools
from tools.text_to_words import words_filter
from tools.stop_words_list import *


from doc_features.semantic_gensim import *
from doc_features.semantic_gensim_readers import *

from zbl_gensim_process_file import *
from zbl_mscmembership_process_file import *
from zbl_fields_process_file import *
from zbl_tfidflike_process_file import *

from zbl_extract_graph import * 


TEMPDIR = tempfile.gettempdir() #place to store temporary results


def has_all_fields(record, must_have_fields):
    """Returns True iff record contains all fields."""
    for field in must_have_fields:
        if not field in record:
            return False
    return True
         

def keep_records(fin, fout, must_have_fields):
    """Copies records from fin to fout. 
    
    Keeps only these records that have all fields from must_have_fields list.
    """
    kept_counter = 0
    for i,record in enumerate(zbl_io.read_zbl_records(fin)):
        if i%10000 == 0: print "[keep_records]", i,"processed", kept_counter, "kept"
        if has_all_fields(record, must_have_fields):
            zbl_io.write_zbl_record(fout, record)
            fout.write("\n")  
            kept_counter = kept_counter + 1  
    return kept_counter
    

def append_file(fin, fout, fappend):
    """Copies all records from fin and fappend to fout.
    
    Returns number of all copied records."""
    counter = 0
    for record in zbl_io.read_zbl_records(fin):                        
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")    
        counter = counter + 1 
    for record in zbl_io.read_zbl_records(fappend):                    
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")    
        counter = counter + 1
    return counter

def copy_file(fin, fout):
    """Copies all records from fin to fout.
    
    Returns number of all copied records."""
    counter = 0
    for record in zbl_io.read_zbl_records(fin):                        
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")    
        counter = counter + 1 
    return counter

def _extract_surname_name_(astr):
    try:
        parts = astr.split(',')        
        return [parts[0].strip(), parts[1].strip()]
    except:
        pass
    try:
        parts = astr.split('  ')        
        return [parts[0].strip(), parts[1].strip()]        
    except:
        pass
    try:
        parts = astr.split(' ')        
        return [parts[0].strip(), parts[1].strip()]        
    except:
        pass
    #print "[_extract_surname_name_] Warn:", astr
    return [astr, ""]

def _reformat_au_(austr):
    authors = []        
    #print "_reformat_au_", austr
    for author in austr.split(";"):    
        author = author.strip()
        if len(author) < 1:
            continue        
        parts = _extract_surname_name_(author)
        author_packed = zbl_io.pack_multivalue_field(parts, zbl_io.MULTIVAL_FIELD_SEPARATOR2);                
        authors.append(author_packed)        
    authors_packed = zbl_io.pack_multivalue_field(authors)
    return authors_packed


def _reformat_ai_(austr):
    authors = []        
    for author in austr.split(";"):
        author = author.strip()
        if len(author) < 1:
            continue                        
        authors.append(author)        
    authors_packed = zbl_io.pack_multivalue_field(authors)
    return authors_packed
        
def record_keep_authors(record):
    """Basing on records creates new record with only authorship information kept."""
    newrec = {}
    newrec[zbl_io.ZBL_ID_FIELD] = record[zbl_io.ZBL_ID_FIELD]
    if record.has_key('au'):
        newrec['au'] =  _reformat_au_( record['au'] )
    if record.has_key('ai'):
        newrec['ai'] =  _reformat_ai_( record['ai'] )
    return newrec

def keep_authors(fin, fout):
    """Copies all records from fin to fout. 
    
    
    Removes all fields apart from an, au, ai.
    Returns number of all copied records.
    """
    counter = 0
    for record in zbl_io.read_zbl_records(fin):
        zbl_io.write_zbl_record(fout, record_keep_authors(record))
        fout.write("\n")    
        counter = counter + 1 
    return counter


def build_ngrams(words, n = 2, ngram_separator = '-'):
    """Converts single words into n-grams by merging words."""
    ngrams = [ reduce(lambda w1,w2: w1+ngram_separator+w2, words[i:i+n]) for i in xrange(len(words)-n+1) ]
    return ngrams 
    
def build_ngrams_with_endings(words, n = 2, ngram_separator = '-'):
    """Converts single words into n-grams by merging words.

    Keeps shorter n-grams at the ending.
    """
    ngrams = [ reduce(lambda w1,w2: w1+ngram_separator+w2, words[i:i+n]) for i in xrange(len(words)) ]
    return ngrams 


def build_ngrams_file(fin, fout, list_of_fields, n = 2, ngram_separator = '-', keep_endings = False):
    """Converts single words in selected fields into n-grams by merging words."""
    if keep_endings:
        ngram_calculator = build_ngrams_with_endings
    else:
        ngram_calculator = build_ngrams
    #print "[build_ngrams_file] ngram_calculator =",ngram_calculator

    for record in zbl_io.read_zbl_records(fin):
        for field in list_of_fields:
            if not record.has_key(field): continue
            words = record[field].split()
            ngrams = ngram_calculator(words, n, ngram_separator)
            if len(ngrams) <= 0: 
                logging.warn("No "+str(n)+"-grams found in an="+str(record[zbl_io.ZBL_ID_FIELD])+" in field "+ str(field)+ "="+str(record[field])+". Using single words instead.")
                ngrams = words
            record[field] = reduce(lambda w1,w2: (w1)+' '+(w2), ngrams)
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
                                                
                

        
        
def filter_fields_vals(fin, fout, list_of_fields, text_filter = text_filter_lower_space, word_predicate = def_word_predicate):
    """Copies records from fin to fout and for fields on list_of_fields filters its' values."""
    logging.info("[filter_fields_vals] text_filter="+str(text_filter)+" word_predicate="+str(word_predicate))
    for record in zbl_io.read_zbl_records(fin):
        for field in list_of_fields:   
            if record.has_key(field):         
                try:   
                    record[field] = words_filter(text_filter(record[field]), word_predicate)
                except:
                    logging.warn("Removing field in an="+str(record[zbl_io.ZBL_ID_FIELD])+" (is field empty?):"+field+" = "+record[field])
                    record.pop(field)             
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
                
        
def filter_records(fin, fout, bad_ids_file):
    """Copies records from fin to fout. Filters out records of ids contained in file bad_ids_file (path).
    
    Returns list of skipped (filtered out) ids."""
    filter_ids = set(line.strip() for line in open(bad_ids_file).xreadlines())
    skipped_ids = set()        
    for record in zbl_io.read_zbl_records(fin):
        if record[zbl_io.ZBL_ID_FIELD] in filter_ids:
            skipped_ids.add(record[zbl_io.ZBL_ID_FIELD])
            continue
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
    return skipped_ids

def keep_records_ids(fin, fout, keep_ids_file):
    """Copies records from fin to fout. Keeps only those records of ids contained in file keep_ids_file (path).
    
    Returns list of kept ids."""
    filter_ids = set(line.strip() for line in open(keep_ids_file).xreadlines())
    print len(filter_ids)," on the 'keep-ids' list"
    kept_ids = set()        
    for record in zbl_io.read_zbl_records(fin):
        if not record[zbl_io.ZBL_ID_FIELD] in filter_ids: continue
        kept_ids.add(record[zbl_io.ZBL_ID_FIELD])
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
    return kept_ids


def fix_id(id):
    """Fixes formatting of ZBL-ID (currently it is just removing prefix 'pre')."""
    if id.startswith("pre"):
        id =  id.replace('pre', '')
    return id
    

def filter_duplicates(fin, fout):
    """Copies records from fin to fout. Records with duplicated id are filtered out.
    
    Returns list of duplicated ids."""
    ids = set()
    duplicated_ids = set()
    for record in zbl_io.read_zbl_records(fin):
        id = fix_id(record[zbl_io.ZBL_ID_FIELD])        
        if id in ids:
            duplicated_ids.add(id)
            continue        
        ids.add(id)
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")    
    return duplicated_ids

def filter_af(fin, fout):
    """Copies records from fin to fout but also removes from records empty (only "-" values) af fields.
    
    Returns number of removed fields.
    """
    counter = 0
    for record in zbl_io.read_zbl_records(fin):
        if record.has_key("af"):
            af = zbl_io.unpack_multivalue_field(record["af"])
            empty = sum(1 for a in af if a == '-') == len(af)
            if empty:
                record.pop("af")
                counter = counter + 1
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")            
    return counter

    
    
#######################################################################################
#######################################################################################
#######################################################################################    
    
    
    
#supported command names:
ADD_FIELD_CMD_NAME = '-addfield'
COPY_FIELD_CMD_NAME = '-copyfield'
MERGE_FIELDS = '-mergefields'
MV_FIELD_CMD_NAME = '-mvfield'
FILTER_RECORDS_WITH_FIELDS = '-filterrecfield'
EXTRACT_FIELD_CMD_NAME = '-field'
EXTRACT_FIELDVAL_CMD_NAME = '-fieldval'

FILTER_ID_CMD_NAME = '-filterids' 
KEEP_ID_CMD_NAME = '-keepids'
FILTER_ID_DUPLICATES_CMD_NAME = '-idduplicates'
APPEND_FILE_CMD_NAME = '-appendfile'
CPY_FILE_CMD_NAME = '-copy'

EXTRACT_AUTHORS_CMD_NAME = '-authors'
FILTER_AUTHOR_FINGERPRINTS_CMD_NAME = '-af'


FILTER_TEXT = '-filter'    
STEMMING = '-stemming'
NGRAMS = '-ngram'
NGRAMS2 = '-ngram2'         
       
GENSIM_DICT = '-gensim_dict'    
GENSIM_MAP = '-gensim_map'
GENSIM_TFIDF = '-gensim_tfidf'
GENSIM_TFIDFMAP = '-gensim_tfidfmap'
GENSIM_LDA = '-gensim_lda'
GENSIM_LSA = '-gensim_lsa'
GENSIM_SEMANTIC_MAP = '-gensim_lmap'

WD_MODEL = '-words_docs_model'
WD_MAP = '-words_docs_map'

MSC_MODEL = '-mscmodel'
MSC_MEMBERSHIP = '-mscmembership'
#MSC_FILTER_RECORDS = '-mscmin'

CI_GRAPH = '-cigraph'
DL_CI_GRAPH = '-dlcigraph'
AF_GRAPH = '-afgraph'
JN_GRAPH = '-jngraph'
    
if __name__ == "__main__":    
    #try:
    #    in_path = sys.argv[1]
    #except:
    #    print "First argument expected: source-file"        
    #    sys.exit(-1)
    #try:
    #    out_path = sys.argv[2]
    #except:
    #    print "Second argument expected: output file"        
    #    sys.exit(-1)
    #print "Source file:", in_path
    #print "Destination file:", out_path
    #fout = open(out_path, "w")
    #fin = open(in_path, "r")

    fin = sys.stdin
    fout = sys.stdout
    sys.stdout = sys.stderr
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


    sys.argv = sys.argv + ['','']
    for i in xrange(len(sys.argv)-1, 2, -1): #fixing argv after in/out-path removal
        sys.argv[i] = sys.argv[i-2]
    sys.argv[1] = 'stdin'
    sys.argv[2] = 'stdout'


    try: 
        cmd = sys.argv[3]        
        if cmd == ADD_FIELD_CMD_NAME:
            add_field_name = sys.argv[4]
            add_field_value = sys.argv[5]    
        elif cmd == COPY_FIELD_CMD_NAME or cmd == MV_FIELD_CMD_NAME:
            src_field = sys.argv[4]
            dst_field = sys.argv[5]
        elif cmd == MERGE_FIELDS:
            list_of_fields = sys.argv[4].split(',')
            dst_field = sys.argv[5]
            try:
                separator = sys.argv[6]
            except:
                separator = ' '
        elif cmd == FILTER_ID_CMD_NAME:
            bad_ids_file = sys.argv[4]         
        elif cmd == KEEP_ID_CMD_NAME:
            keep_ids_file = sys.argv[4]         
        elif cmd == APPEND_FILE_CMD_NAME:
            append_file_path = sys.argv[4] 
        elif cmd == EXTRACT_FIELD_CMD_NAME or cmd == EXTRACT_FIELDVAL_CMD_NAME:
            field_name = sys.argv[4]  
        elif cmd == FILTER_TEXT:
            list_of_fields = sys.argv[4].split(',')
        elif cmd == STEMMING:            
            method = sys.argv[4]
            list_of_fields = sys.argv[5].split(',')
        elif cmd == NGRAMS or cmd == NGRAMS2:
            n = int(sys.argv[4])
            list_of_fields = sys.argv[5].split(',')
            try:
                ngram_separator = sys.argv[6]
            except:                
                ngram_separator = '-'
            if cmd == NGRAMS:
                keep_endings = False
            else:
                keep_endings = True
        elif cmd == GENSIM_DICT:
            list_of_fields = sys.argv[4].split(',')
            try:
                filter_by_fields = sys.argv[5].split(',')
            except:
                filter_by_fields = ['mc']
            try:
                dict_pickle = sys.argv[6]
            except:
                dict_pickle = str(TEMPDIR)+"/gensim_dict.pickle"
            try:
                min_word_freq_in_corpora = int(sys.argv[7])
            except:
                min_word_freq_in_corpora = 2                     
        elif cmd == GENSIM_MAP:
            list_of_fields = sys.argv[4].split(',')
            try:
                filter_by_fields = sys.argv[5].split(',')
            except:
                filter_by_fields = ['mc']
            try:
                dict_pickle = sys.argv[6]
            except:
                dict_pickle = str(TEMPDIR)+"/gensim_dict.pickle"
            try:
                dst_field = sys.argv[7]
            except:
                dst_field = 'g0'         
        elif cmd == GENSIM_TFIDF:
            try:
                tfidf_pickle = sys.argv[4]
            except:
                tfidf_pickle = str(TEMPDIR)+"/gensim_tfidf_model.pickle"
            try:
                src_field = sys.argv[5]
            except:
                src_field = 'g0'            
        elif cmd == GENSIM_TFIDFMAP:
            try:
                tfidf_pickle = sys.argv[4]
            except:
                tfidf_pickle = str(TEMPDIR)+"/gensim_tfidf_model.pickle"
            try:
                src_field = sys.argv[5]
            except:
                src_field = 'g0'         
            try:
                dst_field = sys.argv[6]
            except:
                dst_field = 'g1' 
        elif cmd == GENSIM_LDA or cmd == GENSIM_LSA:
            try:
                num_topics = int(sys.argv[4])
            except:
                num_topics = 300
            try:
                src_field = sys.argv[5]
            except:
                src_field = 'g1'
            try:
                dict_pickle = sys.argv[6]
            except:
                dict_pickle = str(TEMPDIR)+"/gensim_dict.pickle"
            try:
                semantic_model_pickle = sys.argv[7]
            except:
                semantic_model_pickle = str(TEMPDIR)+"/gensim_semantic_model.pickle"            
            try:
                topics_log_path = sys.argv[8]
            except:
                topics_log_path = str(TEMPDIR)+"/gensim_semantic_model_topics.txt"
        elif cmd == GENSIM_SEMANTIC_MAP:
            try:
                src_field = sys.argv[4]
            except:
                src_field = 'g1'
            try:
                dst_field = sys.argv[5]
            except:
                dst_field = 'g2'
            try:
                semantic_model_pickle = sys.argv[6]
            except:
                semantic_model_pickle = str(TEMPDIR)+"/gensim_semantic_model.pickle"
        elif cmd == MSC_MODEL:
            try:
                msc_model_pickle = sys.argv[4]
            except:
                msc_model_pickle = str(TEMPDIR)+"/msc_model.pickle"
            try:
                src_field = sys.argv[5]
            except:
                src_field = 'mc'
        elif cmd == MSC_MEMBERSHIP:
            try:
                msc_model_pickle = sys.argv[4]
            except:
                msc_model_pickle = str(TEMPDIR)+"/msc_model.pickle"
            try:
                src_field = sys.argv[5]
            except:
                src_field = 'mc'
            try:
                dst_field = sys.argv[6]
            except:
                dst_field = 'm0'
            try:
                if sys.argv[7] == '0':
                    leaf_pattern = msc_processing.MSC_LEAF_PATTERN_RE
                elif sys.argv[7] == '1':
                    leaf_pattern = msc_processing.MSC_ORDINARY_LEAF_PATTERN_RE
                elif sys.argv[7] == '2':
                    leaf_pattern = msc_processing.MSC_SPECIAL_LEAF_PATTERN_RE
                else:
                    print "Bad argument for leaf-pattern-no command:",MSC_MEMBERSHIP,"(1/2/3 supported)"
                    sys.exit(-1)
            except:
                leaf_pattern = msc_processing.MSC_ORDINARY_LEAF_PATTERN_RE
        elif cmd == FILTER_RECORDS_WITH_FIELDS:
            list_of_fields = sys.argv[4].split(',')
        elif cmd == WD_MODEL:
            try:
                src_field = sys.argv[4]
            except:
                src_field = 'g0'
            try:
                model_pickle = sys.argv[5]
            except:
                model_pickle = str(TEMPDIR)+"/wd_model.pickle"
        elif cmd == WD_MAP:
            try:
                mode = sys.argv[4]
            except:
                mode = "tf-idf"
            try:
                src_field = sys.argv[5]
            except:
                src_field = 'g0'
            try:
                model_pickle = sys.argv[6]
            except:
                model_pickle = str(TEMPDIR)+"/wd_model.pickle"
            try:
                dst_field = sys.argv[7]
            except:
                dst_field = 'g1'                                  
    except:
        print "Processes ZBL stream (read from stdin) modifying every record according to given rule."
        print "Argument expected: command (what to do with records)."  
        print "Currently supported commands:"
        print ADD_FIELD_CMD_NAME, "[fieldname] [fieldvalue] - adds to every record field of given name and value"
        print COPY_FIELD_CMD_NAME, "[src fieldname] [dst fieldname] - copies value of source field to destination field"
        print MERGE_FIELDS, "[list-of-src-fields-separated-with-,] [dst field] [separator (opt)] merges src-fields into dst-field"
        print MV_FIELD_CMD_NAME, "[src fieldname] [dst fieldname] - moves value of source field to destination field"
        print FILTER_RECORDS_WITH_FIELDS, "[list-of-fields] - keeps only those records that have all fields in list-of-fields (separated by ,)"
        print EXTRACT_FIELD_CMD_NAME, '[field-name] - keeps only field of field-name in records'
        print EXTRACT_FIELDVAL_CMD_NAME, '[field-name] - extracts value of field of field-name from records'

        print FILTER_ID_CMD_NAME, "[id-list-file] - removes records of id contained in id-list-file (single id per line)"
        print KEEP_ID_CMD_NAME, "[id-list-file] - keeps records of id contained in id-list-file (single id per line)"
        print FILTER_ID_DUPLICATES_CMD_NAME, " - removes records with id duplicated"    
        print APPEND_FILE_CMD_NAME, "[append-file-path] - appends append-file-path file to source file"
        print CPY_FILE_CMD_NAME, " - copies file from source to destination"
        
        print EXTRACT_AUTHORS_CMD_NAME, ' - keeps just authors information (fields: au, ai)'
        print FILTER_AUTHOR_FINGERPRINTS_CMD_NAME, ' - removes from records empty af (only "-" values) fields'
        
        print FILTER_TEXT, '[list-of-fields] - filters fields from list-of-fields (separated by ,) - removes punctuation and words from stoplist.'
        print STEMMING, '[method] [list-of-fields] - stems fields from list-of-fields using given method (lancaster/porter/wordnet)'   
        print NGRAMS,"/",NGRAMS2, '[n-value] [list-of-fields] [ngrams-separator (opt)] - converts single words in fields (separated by ,) into ngrams (connected with ngrams-separator)' 
        
        print GENSIM_DICT, '[list-of-fields] [filter-by-fields (opt)] [gen-sim-dict-pickle (opt)] [min word freq in corpora (opt)] - builds and pickles gensim dictionary (token->id)'
        print GENSIM_MAP, '[list-of-fields] [filter-by-fields (opt)] [gen-sim-dict-pickle (opt)] [dst-field-name (opt)] - merges selected fields and maps them using gensim-dictionary (results stored as additional field)'
        print GENSIM_TFIDF, '[gen-sim-tfidf-model-pickle (opt)] [src-field-name (opt)] - builds and pickles gensim tfidf model'
        print GENSIM_TFIDFMAP, '[gen-sim-tfidf-model-pickle (opt)] [src-field-name (opt)] [dst-field-name (opt)] - calculates TFIDF for src-field and stores into dst-field'
        print GENSIM_LDA,"/",GENSIM_LSA,"[num_topics (opt)] [id:weight-field-name (opt)] [gensim-dict-pickle-path (opt)] [topics-log-path (opt)] - builds LDA/LSA model"
        print GENSIM_SEMANTIC_MAP,"[id:weight-src-field-name (opt)] [id:weight-dst-field-name (opt)] [gensim-semantic-model-pickle-path (opt)] - calculates weights using semantic-model"
        
        print WD_MODEL, "[id:count-src-field-name (opt)] [words-docs-model-pickle-path (opt)] builds words x docs model"
        print WD_MAP, "[mode:tf-idf/tf-ent/wf-idf/...] [id:count-src-field-name (opt)] [words-docs-model-pickle-path (opt)] [id:weight-dst-field-name (opt)] maps words' counts into words' weights using model"
        
        print MSC_MODEL, "[msc-model-pickle-path (opt)] [msc-values-field-name (opt)] calculates msc-counts"
        print MSC_MEMBERSHIP, "[msc-model-pickle-path (opt)] [msc-values-field-name (opt)] [dst-membership-field-name (opt)] [msc-codes-filter:0=all,1=ordinary,2=special (opt)] calculates msc-membership"
        #print MSC_FILTER_RECORDS , "[msc-model-pickle-path (opt)] [min-count (opt)] keeps only those records for which primary code occurrs at least min-count times."
        
        print CI_GRAPH, "extracts citations graph from source file"
        print DL_CI_GRAPH, "extracts citations graph from source file (connections are both ways)"
        print AF_GRAPH, "extracts common-authorship graph from source file"
        print JN_GRAPH, "extracts common-journal-number graph from source file"
        sys.exit(-1)

    try:        
        script_start = time.clock()
        print "Command:", cmd
        if cmd == ADD_FIELD_CMD_NAME:        
            add_field(fin, fout, add_field_name, add_field_value)
        elif cmd == COPY_FIELD_CMD_NAME: 
            print "src_field=",src_field   
            print "dst_field=",dst_field
            copy_field(fin, fout, src_field, dst_field)
        elif cmd == MERGE_FIELDS:
            print "src_fields=",list_of_fields
            print "dst_field=",dst_field
            print "separator=",separator
            merge_fields(fin, fout, list_of_fields, dst_field, separator)
        elif cmd == MV_FIELD_CMD_NAME:
            mv_field(fin, fout, src_field, dst_field)
        elif cmd == FILTER_ID_CMD_NAME:                
            skipped_ids = filter_records(fin, fout, bad_ids_file)
            print "Skipped ids:", skipped_ids
            print "Total:", len(skipped_ids)
        elif cmd == KEEP_ID_CMD_NAME:
            kept_ids = keep_records_ids(fin, fout, keep_ids_file)
            print "Total kept:", len(kept_ids)
        elif cmd == FILTER_ID_DUPLICATES_CMD_NAME:
            duplicated_ids = filter_duplicates(fin, fout)        
            print "Duplicated ids:", duplicated_ids
            print "Total:", len(duplicated_ids)
        elif cmd == APPEND_FILE_CMD_NAME:
            print append_file(fin, fout, open(append_file_path)), "records copied."
        elif cmd == CPY_FILE_CMD_NAME:
            print copy_file(fin, fout), "records copied."
        elif cmd == EXTRACT_AUTHORS_CMD_NAME:
            print keep_authors(fin, fout), "records processed."
        elif cmd == FILTER_AUTHOR_FINGERPRINTS_CMD_NAME:
            print filter_af(fin, fout), "empty af fields removed."
        elif cmd == EXTRACT_FIELD_CMD_NAME:
            print filter_field(fin, fout, field_name), "records copied."
        elif cmd == EXTRACT_FIELDVAL_CMD_NAME:
            print extract_field_value(fin, fout, field_name), "values extracted."        
        elif cmd == FILTER_TEXT:
            print "List of fields to be filtered = ", list_of_fields        
            filter_fields_vals(fin, fout, list_of_fields, text_filter_lower_space, def_word_predicate)
        elif cmd == STEMMING:            
            print "List of fields to be filtered = ", list_of_fields
            print "Stemming method = ", method
            import nltk
            if method == 'lancaster':
                stemmer = nltk.stem.LancasterStemmer()
            elif method == 'porter': 
                stemmer = nltk.stem.PorterStemmer()            
            elif method == 'wordnet':
                stemmer = nltk.stem.WordNetStemmer()
                stemmer.stem = stemmer.lemmatize            
            else:
                print "Bad stemming method (try: lancaster/porter/wordnet)!"
                exit(-1)        
            line_stemmer = lambda line: reduce(lambda w1,w2: w1+' '+w2, (stemmer.stem(w) for w in line.split()) )
            filter_fields_vals(fin, fout, list_of_fields, line_stemmer, def_word_predicate)
            #filter_fields_vals(fin, fout, list_of_fields, line_stemmer, lambda x: True)
        elif cmd == NGRAMS or cmd == NGRAMS2:  
            print "List of fields to be processed = ", list_of_fields
            print "N-value = ", n
            print "ngram-separator = <", ngram_separator,">"
            print "keep-endings =",keep_endings
            build_ngrams_file(fin, fout, list_of_fields, n, ngram_separator, keep_endings)
        elif cmd == GENSIM_DICT:
            print "list of fields to be merged and converted=",list_of_fields   
            print "filter_by_fields=",filter_by_fields
            print "dict_pickle =",dict_pickle
            print "min_word_freq_in_corpora =", min_word_freq_in_corpora
    
            #Dictionary: #for already filtered data
            start = time.clock()
            dictionary = build_dictionary( zbl_generator_q(fin, list_of_fields, filter_by_fields), stoplist=[], min_freq=min_word_freq_in_corpora)
            print "Building token2id dictionary=",dictionary," in", time.clock()-start,"s -> ", str(dictionary.token2id)[:100],"..."
            print "Pickling dictionary into file",dict_pickle
            pickle.dump(dictionary, open(dict_pickle, 'wb'))
        elif cmd == GENSIM_MAP:
            print "list of fields to be merged and converted=",list_of_fields   
            print "filter_by_fields=",filter_by_fields
            print "dict_pickle =",dict_pickle
            print "dst_field =",dst_field 
    
            print "Loading dictionary from file",dict_pickle
            dictionary = pickle.load( open(dict_pickle) )
            print "Loaded token2id dictionary=",dictionary," -> ", str(dictionary.token2id)[:100],"..."
            num_enriched_records = gensim_mapfields_dict_file(fin, fout, list_of_fields, filter_by_fields, dictionary, dst_field)
            print num_enriched_records, "records enriched..."    
        elif cmd == GENSIM_TFIDF:
            print "tfidf_pickle =", tfidf_pickle
            print "src_field =", src_field         
            print "Building TFIDF model..."
            start = time.clock()
            tfidf_model = build_tfidf_model( id_bags_generator(fin, src_field) )
            print "Building TFIDF model=",tfidf_model," in", time.clock()-start,"s"
            print "Pickling dictionary into file",tfidf_pickle
            pickle.dump(tfidf_model, open(tfidf_pickle, 'wb'))        
        elif cmd == GENSIM_TFIDFMAP:
            print "tfidf_pickle =", tfidf_pickle
            print "src_field =", src_field         
            print "dst_field =", dst_field         
    
            print "Loading TFIDF model from file",tfidf_pickle
            tfidf_model = pickle.load( open(tfidf_pickle) )
            print "Loaded TFIDF model=",tfidf_model
            num_enriched_records = gensim_calctfids_file(fin, fout, tfidf_model, src_field, dst_field)                    
            print num_enriched_records, "records enriched..."    
        elif cmd == GENSIM_LSA or cmd == GENSIM_LDA:
            print "num_topics =",num_topics
            print "src_field =",src_field
            print "dict_pickle =",dict_pickle
            print "semantic_model_pickle =",semantic_model_pickle
            print "topics_log_path =", topics_log_path
    
            print "Loading dictionary from file",dict_pickle
            dictionary = pickle.load( open(dict_pickle) )
            print "Building semantic model..."   
            start = time.clock()
            bag_of_ids_vals_generator = id_bags_generator(fin, src_field, value_extractor=extract_bag_of_tfidf)
            if cmd == GENSIM_LDA:
                print "Building LDA-semantic model..."   
                semantic_model = build_lda_model(bag_of_ids_vals_generator, dictionary, num_topics)
            else:
                print "Building LSA-semantic model..."   
                semantic_model = build_lsi_model(bag_of_ids_vals_generator, dictionary, num_topics)
            print "Storing topics into",topics_log_path 
            gensim_topics_store(semantic_model, open(topics_log_path, "w"), topn=100)                
            print "Building semantic model=",semantic_model," in", time.clock()-start,"s"
            print "Pickling model into file",semantic_model_pickle
            pickle.dump(semantic_model, open(semantic_model_pickle, 'wb'))        
        elif cmd == GENSIM_SEMANTIC_MAP:
            print "src_field =",src_field
            print "dst_field =",dst_field
            print "semantic_model_pickle =",semantic_model_pickle
    
            print "Loading semantic model from file",semantic_model_pickle
            semantic_model = pickle.load(open(semantic_model_pickle))
            print "Loaded semantic model=",semantic_model
            num_enriched_records = gensim_mapfield_model(fin, fout, semantic_model, src_field, dst_field, \
                                                         src_field_value_extractor=extract_bag_of_tfidf, \
                                                         dst_field_value_builder=zbl_io.pack_listpairs_field)    
            print num_enriched_records, "records enriched..."
            
        elif cmd == WD_MODEL:
            print "src_field=",src_field
            print "model_pickle=",model_pickle
            print "Building Words-Docs model"
            wordsmodel = build_wordsmodel(fin, fout, src_field)
            wordsmodel.report()
            print "Pickling into", model_pickle
            pickle.dump(wordsmodel, open(model_pickle, 'wb'))
        elif cmd == WD_MAP:
            print "mode=",mode
            lw = mode.split('-')[0]
            gw = mode.split('-')[1]
            if lw == "tf":
                localweigting = tf
            elif lw == "wf":
                localweigting = wf
            else:
                print "UNKNOWN LOCAL WEIGHTING METHOD!"
                sys.exit(-2)
            if gw == "idf":
                globalweigting = idf
            elif gw == "ent":
                globalweigting = ent
            else:
                print "UNKNOWN GLOBAL WEIGHTING METHOD!"
                sys.exit(-2)
            print "localweigting=",localweigting
            print "globalweigting=",globalweigting
            print "src_field=",src_field
            print "model_pickle=",model_pickle
            print "dst_field=",dst_field      
            print "Loading pickled model from", model_pickle
            wordsmodel = pickle.load(open(model_pickle))
            wordsmodel.report()
            print "Mapping src_field into dst_field..."
            enriched = map_wordsmodel(fin, fout, wordsmodel, src_field, dst_field, localweigting, globalweigting)
            print enriched,"records enriched."                                                                
        elif cmd == MSC_MODEL:
            print "msc_model_pickle=",msc_model_pickle
            print "src_field=",src_field
            msc2count = calc_msc2count(fin, src_field)
            print "sample counts=",str(list(msc2count.iteritems()))[:100],"..."
            print "Pickling model into file",msc_model_pickle
            pickle.dump(msc2count, open(msc_model_pickle, 'wb'))
        elif cmd == MSC_MEMBERSHIP:
            print "msc_model_pickle=",msc_model_pickle
            print "src_field=",src_field
            print "dst_field=",dst_field
            print "leaf_pattern=",leaf_pattern
            print "Loading model from file",msc_model_pickle
            msc2count = pickle.load(open(msc_model_pickle, 'r'))
            print "sample counts=",str(list(msc2count.iteritems()))[:100],"..."
            updated = calc_msc_membership(fin, fout, msc2count.keys(), src_field, dst_field, leaf_pattern)
            print updated," records have been updated."
            
        elif cmd == FILTER_RECORDS_WITH_FIELDS:
            print "must_have_fields=",list_of_fields   
            kept = keep_records(fin, fout, list_of_fields)
            print kept," records have been kept."
            
        elif cmd == CI_GRAPH:
            print "extracting citations graph"
            extracted = extract_citations_graph_file(fin, fout)
            print extracted," lines extracted"
        elif cmd == DL_CI_GRAPH:
            print "extracting double-linked citations graph"
            extracted = extract_citations_doublelinked_graph_file(fin, fout)
            print extracted," lines extracted"
        elif cmd == AF_GRAPH:
            print "extracting authorship graph"
            extracted = extract_fv_graph_file(fin, fout, "af", "-")
            print extracted," lines extracted"
        elif cmd == JN_GRAPH:
            print "extracting common-journal-number graph"
            extracted = extract_fv_graph_file(fin, fout, "jn", "-")
            print extracted," lines extracted"        
        else: 
            print "Bad command!"
    except IOError, e:
        import errno
        if e.errno == errno.EPIPE:
            print "Pipe broken while processing. Finishing..."
        else:
            print "IOException",e    
        
    
    #fin.close()
    #fout.close()
    
    print "Command:",cmd," executed in", (time.clock()-script_start)," sec"
    
    
