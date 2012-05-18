"""Processes ZBL file by modifying every record. Methods connected to membership calculation using MSC codes"""

import sys

sys.path.append(r'../')
import zbl_io

sys.path.append(r'../../')
import logging

from tools import msc_processing



def calc_msc2count(fin, src_field='mc'):
    """Returns msc2counts dictionary."""
    msc2count = {};
    for i,record in enumerate(zbl_io.read_zbl_records(fin)):                            
        if i%10000 == 0: logging.info("[calc_msc_model] "+str(i)+" records processed")
        if not src_field in record: continue
        
        msccodes = zbl_io.unpack_multivalue_field(record[src_field])
        for msc in msccodes:
            msc2count[msc] = msc2count.get(msc, 0) + 1
        
        #zbl_io.write_zbl_record(fout, record)
        #fout.write("\n")            
    return msc2count  

def calc_msc2ix(msccodes):
    """Returns dictionary msc2ix."""
    return dict( (msc,i) for i,msc in enumerate(sorted(msccodes)) )

def filter_msccodes(msccodes, re_pattern):
    """Returns list of msccodes that matches re_pattern."""
    return list(msc for msc in msccodes if not re_pattern.match(msc) is None)
    
def group_by_prefix(msccodes):
    """Returns dictionary {2/3-letters-prefixes: list-of-msc-codes}."""
    prefix2msc = {}
    for msc in msccodes:
        prefix2 = msc[:2]
        prefix3 = msc[:3]
        prefix2msc[prefix2] = prefix2msc.get(prefix2, []) + [msc]
        prefix2msc[prefix3] = prefix2msc.get(prefix3, []) + [msc]
    return prefix2msc     

MSC_0PREFIX_MEMBERSHIP = 0.00
MSC_2PREFIX_MEMBERSHIP = 0.25
MSC_3PREFIX_MEMBERSHIP = 0.50
MSC_5PREFIX_MEMBERSHIP = 0.75

def single_msccode_membership(record_msccode, compared_code):
    """Returns membership to compared_code if there is record_msccode in record."""
    if compared_code[:5] == record_msccode[:5]:
        return MSC_5PREFIX_MEMBERSHIP
    if compared_code[:3] == record_msccode[:3]:
            return MSC_3PREFIX_MEMBERSHIP
    if compared_code[:2] == record_msccode[:2]:
        return MSC_2PREFIX_MEMBERSHIP
    return MSC_0PREFIX_MEMBERSHIP    

def msccode_membership(record_msccodes, compared_code):
    """Returns membership to compared_code if there are record_msccodes in record."""
    return max(single_msccode_membership(msc, compared_code) for msc in record_msccodes) 

def calc_msc_membership(fin, fout, known_msc_codes, \
                        src_field='mc', dst_field='m0', \
                        re_leaf_pattern=msc_processing.MSC_ORDINARY_LEAF_PATTERN_RE, dbg_field='m_'):
    """Updates records with additional dst_field with membership vector calculated basing on msc codes read from src_field."""
    msccodes    = filter_msccodes(known_msc_codes, re_leaf_pattern)
    msc2ix      = calc_msc2ix(msccodes)
    ix2msc      = dict((ix,msc) for msc,ix in msc2ix.iteritems())
    prefix2msc  = group_by_prefix(msccodes)    
        
    counter = 0;
    for i,record in enumerate(zbl_io.read_zbl_records(fin)):                            
        if i%10000 == 0: logging.info("[calc_msc_membership] "+str(i)+" records processed. "+str(counter)+"updated.")
        if src_field in record:         
            record_msccodes = zbl_io.unpack_multivalue_field(record[src_field])
            record_msccodes = filter_msccodes(record_msccodes, re_leaf_pattern)
            
            compared_codes = set() #patrzymy po tych ktore maja zgodne fragmenty prefiksow
            for record_msccode in record_msccodes:                
                prefix2 = record_msccode[:2]
                prefix3 = record_msccode[:3]
                compared_codes.update( prefix2msc[prefix2] )
                compared_codes.update( prefix2msc[prefix3] )

            mscmembership = []
            for compared_code in compared_codes:
                membership = msccode_membership(record_msccodes, compared_code)
                mscmembership.append( (msc2ix[compared_code],membership) )
                    
            if len(mscmembership) > 0: #zapsiujemy wyniki
                mscmembership = sorted(set(mscmembership))
                record[dst_field] = zbl_io.pack_listpairs_field(mscmembership)                
                record[dbg_field] = zbl_io.pack_listpairs_field([(ix2msc[ix],m) for ix,m in mscmembership])
                counter = counter + 1
            
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")            
    return counter            
            

