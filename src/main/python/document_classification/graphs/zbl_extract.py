"""Methods that extracts connection graphs from ZBL data."""

import logging
from collections import deque
import sys

sys.path.append(r'../')
sys.path.append(r'../../')
from tools import stats
from data_io import zbl_io

from graph_modifications import *
from graph_io import *

def yield_citations(zbl_generator):
    """Yields pairs(zbl_id:list-of-ids-of-known-citations).
    
    >>> ci1 = zbl_io.pack_list_of_dictionaries([{'an':2, 'ti':'TITLE'}, {'an':3}])
    >>> ci2 = zbl_io.pack_list_of_dictionaries([{'an':3}, {'py':'1990', 'an':1}])
    >>> ci3 = zbl_io.pack_list_of_dictionaries([{'an':1}])
    >>> r1 = {'an':'1', 'ci': ci1}
    >>> rx = {'an':'x'}
    >>> r2 = {'an':'2', 'ci': ci2}
    >>> r3 = {'an':'3', 'ci': ci3}    
    >>> list( yield_citations([r1, rx, r2, r3]) )
    [('1', ['2', '3']), ('2', ['3', '1']), ('3', ['1'])]
    """    
    for i,zbl in enumerate(zbl_generator):
        if i%10000==0: logging.info("[yield_citations]"+str(i)+" records processed")
        if not "ci" in zbl: continue
        zbl_id = zbl[zbl_io.ZBL_ID_FIELD]
        cis = zbl_io.unpack_list_of_dictionaries(zbl["ci"])
        identified_ci_ids = list(ci[zbl_io.ZBL_ID_FIELD] for ci in cis if ci.has_key(zbl_io.ZBL_ID_FIELD))
        if len(identified_ci_ids) == 0: continue
        yield (zbl_id, identified_ci_ids )

        
def extract_citations_doublelinked_graph(zbl_generator, container = set):
    """Returns dictionary{zbl_id:container-of-ids} basing on citation structure.
    
    If records r1 cites r2 than in output graph there are two links: r1->r2 and r2->r1.
    
    >>> ci1 = zbl_io.pack_list_of_dictionaries([{'an':2, 'ti':'TITLE'}, {'an':3}])
    >>> ci1e = zbl_io.pack_list_of_dictionaries([{'an':3}])
    >>> ci2 = zbl_io.pack_list_of_dictionaries([{'an':3}, {'py':'1990', 'an':1}])
    >>> ci2e = zbl_io.pack_list_of_dictionaries([{'py':'1990', 'an':1}])
    >>> ci3 = zbl_io.pack_list_of_dictionaries([{'an':1}])
    >>> r1 = {'an':'1', 'ci': ci1}
    >>> r1e = {'an':'1', 'ci': ci1e}
    >>> r11 = {'an':'11', 'ci': ci1}
    >>> rx = {'an':'x'}
    >>> r2 = {'an':'2', 'ci': ci2}
    >>> r2e = {'an':'2', 'ci': ci2e}        
    >>> r3 = {'an':'3', 'ci': ci3}
    >>> r3e = {'an':'3'}
    >>> sorted( list( extract_citations_doublelinked_graph([r1, r11, rx, r2, r3], container = set).iteritems() ) ) == [('1', set(['2', '3'])), ('11', set(['2', '3'])), ('2', set(['1', '11', '3'])), ('3', set(['1', '11', '2']))]
    True
    >>> sorted( list( extract_citations_doublelinked_graph([r1, r11, rx, r2e, r3], container = set).iteritems() ) ) == [('1', set(['2', '3'])), ('11', set(['2', '3'])), ('2', set(['1', '11'])), ('3', set(['1', '11']))] 
    True
    >>> sorted( list( extract_citations_doublelinked_graph([r1e, r11, rx, r2e, r3], container = set).iteritems() ) ) == [('1', set(['2', '3'])), ('11', set(['2', '3'])), ('2', set(['1', '11'])), ('3', set(['1', '11']))] 
    True
    >>> sorted( list( extract_citations_doublelinked_graph([r1e, r11, rx, r2e, r3e], container = set).iteritems() ) ) == [('1', set(['2', '3'])), ('11', set(['2', '3'])), ('2', set(['1', '11'])), ('3', set(['11', '1']))] 
    True
    >>> sorted( list( extract_citations_doublelinked_graph([r1e, r3e], container = set).iteritems() ) ) == [('1', set(['3'])), ('3', set(['1']))]  
    True
    """
    src_id2ids = dict( yield_citations(zbl_generator) )
    return extract_doublelinked_graph(src_id2ids, container)

def extract_fieldvalue2ids(zbl_generator, multivalue_field_name = "af", empty_value = "-", container = list):
    """Returns dictionary{field-value: container-of-identified-ids-that-have-this-value}.
    
    >>> r1 = {'an':'1', 'af': zbl_io.pack_multivalue_field(['a1','-','a2']) }
    >>> r2 = {'an':'2', 'af': zbl_io.pack_multivalue_field(['-','a2','a1']) }
    >>> r3 = {'an':'3', 'af': zbl_io.pack_multivalue_field(['a3', '-']) }
    >>> r4 = {'an':'4', 'af': zbl_io.pack_multivalue_field(['a3', '-', 'a2'])}
    >>> sorted(list(extract_fieldvalue2ids([r1,r2,r3]).iteritems()))
    [('a1', ['1', '2']), ('a2', ['1', '2']), ('a3', ['3'])]
    >>> sorted(list(extract_fieldvalue2ids([r1,r2,r3,r4]).iteritems()))
    [('a1', ['1', '2']), ('a2', ['1', '2', '4']), ('a3', ['3', '4'])]
    """
    af2ids = {}
    skipped = 0
    novals = 0
    for i,zbl in enumerate(zbl_generator):
        if i%10000==0: logging.info("[extract_fieldvalue2ids]"+str(i)+" records processed")
        if not multivalue_field_name in zbl:
            skipped = skipped + 1 
            continue
        zbl_id = zbl[zbl_io.ZBL_ID_FIELD] 
        afs = zbl_io.unpack_multivalue_field(zbl[multivalue_field_name])
        afs_ok = list(af for af in afs if af!=empty_value)
        if len(afs_ok)==0: novals = novals + 1
        for af in afs_ok:
            af2ids[af] = af2ids.get(af, []) + [zbl_id]
    logging.info("[extract_fieldvalue2ids] "+str(i)+" records processed")
    logging.info("[extract_fieldvalue2ids] "+str(skipped)+" records skipped")
    logging.info("[extract_fieldvalue2ids] "+str(novals)+" records with only empty values in field")
    fv2ids = dict( (id,container(ids)) for id,ids in af2ids.iteritems())
    logging.info("[extract_fieldvalue2ids] "+str(len(fv2ids))+" authors found.")
    return fv2ids 

def extract_fv_graph(zbl_generator, multival_field_name = "af", empty_value = "-", container = set):
    """Returns dictionary{id:container-of-ids} that describes connection graph.
    
    Between r1 and r2 is (two-way)link if both r1 contains at least single common value in field of field_name.
        
    >>> r1 = {'an':'1', 'af': zbl_io.pack_multivalue_field(['a1','-','a2']) }
    >>> r2 = {'an':'2', 'af': zbl_io.pack_multivalue_field(['-','a2','a1']) }
    >>> r3 = {'an':'3', 'af': zbl_io.pack_multivalue_field(['a3', '-']) }
    >>> r4 = {'an':'4', 'af': zbl_io.pack_multivalue_field(['a3', '-', 'a2'])}
    >>> rx = {'an': 'x'}
    >>> ry = {'an': 'y', 'af': '-'}
    >>> sorted(list(extract_fv_graph([r1,r2,r3,r4]).iteritems())) ==     [('1', set(['2', '4'])), ('2', set(['1', '4'])), ('3', set(['4'])), ('4', set(['1', '2', '3']))]
    True
    >>> sorted(list(extract_fv_graph([r1,r2,ry,r3,r4,rx]).iteritems())) ==     [('1', set(['2', '4'])), ('2', set(['1', '4'])), ('3', set(['4'])), ('4', set(['1', '2', '3']))]
    True
    """
    fv2ids = extract_fieldvalue2ids(zbl_generator, multival_field_name, empty_value, list)
    fv2count = dict( (fv,len(ids)) for fv,ids in fv2ids.iteritems()) #DBG
    logging.info("[extract_fv_graph] max="+ str( max( fv2count.values() ) ) )  #DBG
    logging.info("[extract_fv_graph] avg="+ str( stats.avg( fv2count.values() ) ) )  #DBG
    logging.info("[extract_fv_graph] std="+ str( stats.std( fv2count.values() ) ) )  #DBG
    id2ids = {}
    for rr, (fv,ids) in enumerate(fv2ids.iteritems()):
        if rr%10000 == 0: logging.info("[extract_fv_graph]"+str(rr)+" records processed")
        #logging.info("[extract_fv_graph] considering fv="+str(fv)+" ids="+str(ids)) 
        for i in xrange(len(ids)): #po kazdym majacym dana wartosc
            curr_id = ids[i] #wybierz jednego
            peer_ids = [ ids[j] for j in xrange(len(ids)) if i!=j ] #jego wszysycy sasiedzi
            if len(peer_ids) > 0:
                all_peer_ids = id2ids.get(curr_id, [])
                all_peer_ids.extend(peer_ids)
                id2ids[curr_id] = all_peer_ids                                  
    return dict( (id,container(ids)) for id,ids in id2ids.iteritems())

####################################################################
####################################################################
####################################################################
####################################################################

def extract_citations_graph_file(fin, fout):
    """From fin reads zbl_records and to fout writes in lines: zbl_id:citation-id1,...,citation-idN."""
    zbl_generator = zbl_io.read_zbl_records(fin)
    id2ids_generator = yield_citations(zbl_generator)
    return write_file_id2ids(fout, id2ids_generator, cast_container = set)


def extract_fv_graph_file(fin, fout, multival_field_name = "af", empty_value = "-"):
    """From fin reads zbl_records and to fout writes in lines: zbl_id:id1,id2,id3 (graph extracted from field of name multival_field_name)."""
    zbl_generator =  zbl_io.read_zbl_records(fin)
    fv2ids = extract_fv_graph(zbl_generator, multival_field_name, empty_value, set)
    return write_file_id2ids(fout, fv2ids.iteritems(), cast_container = set)
    

def extract_citations_doublelinked_graph_file(fin, fout):
    """From fin reads zbl_records and to fout writes in lines: zbl_id:zbl-id1,...,zbl-idN.
    
    If records r1 cites r2 than in output graph there are two links: r1->r2 and r2->r1.        
    """
    zbl_generator = zbl_io.read_zbl_records(fin)
    id2ids_generator = extract_citations_doublelinked_graph(zbl_generator)
    #print "[extract_citations_doublelinked_graph_file]",id2ids_generator
    return write_file_id2ids(fout, id2ids_generator.iteritems(), cast_container = set)

