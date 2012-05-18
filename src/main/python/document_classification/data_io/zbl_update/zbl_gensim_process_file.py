"""Processes ZBL file by modifying every record according to rules using GENSIM."""

import sys, pickle
import tempfile                 

sys.path.append(r'../')
import zbl_io

sys.path.append(r'../../')
import logging

from doc_features.semantic_gensim import *
from doc_features.semantic_gensim_readers import *

from tools import msc_processing

import tools
from tools.text_to_words import words_filter
from tools.stop_words_list import *



def text_filter_lower_space(txt):
    return tools.text_to_words.text_filter_lower(txt, replace_with_str=" ")

def def_word_predicate(w): 
    return tools.text_to_words.default_word_predicate(w, stoplist = set(WIKI_STOP_WORDS_LIST))


def gensim_topics_store(semantic_model, flog, topn=100):
    """Writes to flog raport on topics of semantic_model."""
    for topic_no in xrange(semantic_model.num_topics):
        topic = str( semantic_model.print_topic(topic_no, topn) )
        flog.write(str(topic_no)+" =\t"+topic+"\n")


def extract_listpairs_fieldvalue(fieldvalue, val_cast = int, key_cast = int):
    """Takes packed-list-of-pairs-ZBL-field and returns list of pairs (key_cast(dict-key), val_cast(dict-value))."""
    return list((key_cast(k),val_cast(v)) for k,v in zbl_io.unpack_listpairs_field(fieldvalue))

extract_bag_of_ids      = lambda fieldvalue: extract_listpairs_fieldvalue(fieldvalue, val_cast = int, key_cast = int)
extract_bag_of_tfidf    = lambda fieldvalue: extract_listpairs_fieldvalue(fieldvalue, val_cast = float, key_cast = int)


def id_bags_generator(fin, src_field, value_extractor=extract_bag_of_ids):
    """Returns generator that generates gensim-bags-of-ids/tfidfs (read from src_field) from ZBL-file fin."""
    return ( value_extractor(record[src_field]) for record in zbl_io.read_zbl_records(fin) if src_field in record )


def gensim_mapfields_dict(record, fields, filter_by_fields, dictionary, dst_field, id2token={}, dbg_field_name = "g_"):
    """For record, that have filter_by_fields, fields are merged, 
       mapped with gensim dictionary and stored in dst-field."""
    has_filter_by_fields = sum(1 for field in filter_by_fields if field in record) == len(filter_by_fields)
    if has_filter_by_fields: 
        fields_list_of_words = reduce(lambda w1,w2: w1+w2, (record[field].split() for field in fields if field in record) )            
        fields_words_ids = dictionary.doc2bow(fields_list_of_words)
        logging.debug("[gensim_mapfields_dict]"+str(fields_list_of_words)+" -> "+str(fields_words_ids))
        if len(fields_words_ids) > 0:
            record[dst_field] = zbl_io.pack_listpairs_field( fields_words_ids )
            record[dbg_field_name] = zbl_io.pack_listpairs_field( (idx,id2token.get(idx,'?')) for idx,count in fields_words_ids ) #this-line is for debugging purposes
    return record    

def gensim_mapfields_dict_file(fin, fout, fields, filter_by_fields, dictionary, dst_field, dbg_field_name = "g_"):
    """For every records from ZBL-fin-stream that have filter_by_fields 
     fields are merged, mapped with gensim dictionary and stored in dst-field.

       Returns number of processed records."""
    logging.info("[gensim_mapfields_dict_file] filter_by_fields="+str(filter_by_fields)+\
    " fields="+str(fields)+" dictionary="+str(dictionary)+" fin="+str(fin)+" dst_field="+str(dst_field))
    id2token = dict( (idx,token) for idx,token in dictionary.iteritems() ) #this-line is for debugging purposes
    counter = 0
    for i,record in enumerate(zbl_io.read_zbl_records(fin)):                            
        if i%10000 == 0: logging.info("[gensim_mapfields_dict_file] "+str(i)+" records processed")
        record = gensim_mapfields_dict(record, fields, filter_by_fields, dictionary, dst_field, id2token, dbg_field_name)
        if dst_field in record:
            counter = counter + 1 
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")            
    return counter


def gensim_mapfield_model(fin, fout, model, src_field, dst_field,\
                          src_field_value_extractor=extract_bag_of_ids, dst_field_value_builder=zbl_io.pack_listpairs_field):
    """For every records from ZBL-fin-stream that have src_field its content 
    is interpreted as gensim-bag-of-ids(with weights/counts/values) and transformed using model (results are stored into dst_field).

    Returns number of enriched records."""
    logging.info("[gensim_mapfield_model] src_field="+str(src_field)+\
     " model="+str(model)+" fin="+str(fin)+" dst_field="+str(dst_field)+\
     " src_field_value_extractor="+str(src_field_value_extractor)+" dst_field_value_builder="+str(dst_field_value_builder))
    counter = 0
    for i,record in enumerate(zbl_io.read_zbl_records(fin)):                            
        if i%10000 == 0: logging.info("[gensim_mapfield_model] "+str(i)+" documents mapped...")
        if src_field in record:
            bag_of_ids = src_field_value_extractor(record[src_field])
            tfidf_values = model[bag_of_ids]
            record[dst_field] = dst_field_value_builder(tfidf_values)
            logging.debug("[gensim_mapfield_model]"+record[src_field]+" -> "+record[dst_field])
            counter = counter + 1    
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
    return counter

gensim_calctfids_file = gensim_mapfield_model

