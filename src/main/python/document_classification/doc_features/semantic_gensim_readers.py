"""Readers and filters of data for semantic_gensim module."""
import sys, os, logging
sys.path.append(r'../')

from gensim import corpora, models, similarities

from tools.text_to_words import text_filter_lower
from tools.text_to_words import default_word_predicate

from data_io import zbl_record_generators


#########################################################################################
#FILE -> STREAM OF LISTS OF WORDS



def stream_to_wordsstream_generator(src_stream, line_filter=text_filter_lower, word_predicate=default_word_predicate):
    """Returns generator of lists of words build out of src_stream (e.g. file).
    
    Generates lists of words. Single list is generated out of single line.    
    Lines are filtered by line_filter and only those words
    for which word_predicate returns true are included."""
    for line in src_stream:
        #line = unicode(line_filter(line), errors='ignore') #words in unicode
        line = line_filter(line) #word not in unicode
        yield list( word for word in line.split() if word_predicate(word) )
        
def stream_to_wordsstream_generator_simple(src_stream):
    """Simplified version of stream_to_wordsstream_generator (no filtering included)."""
    for line in src_stream:
        yield line.split()
        #yield unicode(line, errors='ignore').split()
        
def zbl_generator(zbl_file_path, fields, filtered_by = ['mc'], uni = False, line_filter=text_filter_lower, word_predicate=default_word_predicate):
    """Wrapper that simplifies reading from ZBL files. 
    
    Based on zbl_record_generators.gen_text.
    Returns generator that generates lists of words (single line=single list)."""
    src_stream = zbl_record_generators.gen_text(zbl_file_path, fields, filtered_by, uni) 
    wordslist_generator = stream_to_wordsstream_generator(src_stream, line_filter, word_predicate)
    return wordslist_generator


def zbl_generator_q(zbl_file_path, fields, filtered_by = ['mc'], uni = False):
    """Faster version of zbl_generator (data is not filtered)."""
    logging.info("[zbl_generator_q] fields="+str(fields)+" filtered_by="+str(filtered_by)+" infile="+str(zbl_file_path))
    src_stream = zbl_record_generators.gen_text(zbl_file_path, fields, filtered_by, uni) 
    wordslist_generator = stream_to_wordsstream_generator_simple(src_stream)
    return wordslist_generator

