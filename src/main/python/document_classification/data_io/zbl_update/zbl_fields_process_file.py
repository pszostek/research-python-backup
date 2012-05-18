"""Processes ZBL file by modifying every record according to rules for single fields."""

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


def add_field(fin, fout, add_field_name, add_field_value):
    """To every record from fin adds field (add_field_value:add_field_name) and stores record to fout."""
    for record in zbl_io.read_zbl_records(fin):
        record[add_field_name] = add_field_value            
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
        
def copy_field(fin, fout, src_field, dst_field):
    """In every record from fin copies field src_field to field dst_field and stores record to fout."""
    for record in zbl_io.read_zbl_records(fin):
        if record.has_key(src_field):            
            record[dst_field] = record[src_field]
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")

def mv_field(fin, fout, src_field, dst_field):
    """In every record from fin moves field src_field to field dst_field and stores record to fout."""
    for record in zbl_io.read_zbl_records(fin):
        if record.has_key(src_field):            
            record[dst_field] = record[src_field]
            record.pop(src_field)
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
        
def merge_fields(fin, fout, src_fields, dst_field, separator = " "):
    """In every record from fin merges fields from src_field to field dst_field and stores record to fout."""
    for record in zbl_io.read_zbl_records(fin):
        try:
            dst_val = reduce(lambda a,b: a+separator+b, (record[src_field] for src_field in src_fields if src_field in record) )
            record[dst_field] = dst_val
        except:
            print "[merge_fields] Failed merging in record an=", record[zbl_io.ZBL_ID_FIELD]
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")


def filter_field(fin, fout, field_name):
    """Copies records from fin to fout but keeping only id and field of field_name.    
    
    Returns number of found fields.
    """
    counter = 0
    for record in zbl_io.read_zbl_records(fin):
        newrec = {}
        newrec[zbl_io.ZBL_ID_FIELD] = record[zbl_io.ZBL_ID_FIELD]
        if record.has_key(field_name):
            newrec[field_name] = record[field_name]            
            counter = counter + 1
        zbl_io.write_zbl_record(fout, newrec)
        fout.write("\n")            
    return counter    

def extract_field_value(fin, fout, field_name):
    """Extracts to fout value of a field of field_name.    
    
    Returns number of found fields.
    """
    counter = 0
    for record in zbl_io.read_zbl_records(fin):
        if record.has_key(field_name):
            fout.write(str(record[field_name]))
            fout.write("\n")            
            counter = counter + 1
    return counter    
