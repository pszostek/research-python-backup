"""IO for graphs represented as src-node-id:list-of-output-nodes-id."""

import logging
from collections import deque

import sys
sys.path.append(r'../')
sys.path.append(r'../../')
from tools import stats


def yield_file_nodes(fgraph):
    """Yields pairs (node-id: list-of-outgoing-nodes-ids) read from fgraph file.
    
    File should be in format where every line is: id_src:id_dst1,id_dst2,id_dst3,...,id_dstN
    """
    for line in fgraph.xreadlines():
        if line.strip() == '':
            logging.warn("[yield_file_nodes] empty line=("+line+") found in fgraph.") 
            continue #skip empty lines
        #print "[yield_file_nodes] line=",line
        parts = line.split(":")
        src_id = parts[0].strip()
        dst_ids = [id.strip() for id in parts[1].split(',')]
        #if len(src_id)<4: print "[yield_file_nodes]", src_id
        #for id in dst_ids:
        #    if len(id)<4: print "[yield_file_nodes] bad id:", src_id                    
        yield (src_id, dst_ids)
        
def write_file_id2ids(fout, id2ids_generator, cast_container = list):
    """Writes to fout lines: id_src:id_dst1,id_dst2,id_dst3,...,id_dstN read from id2ids_generator.        """
    #id1,...,idN should be unique because are casted to set before writing.
    counter = 0
    for zbl_id,ids in id2ids_generator:        
        fout.write(str(zbl_id));
        fout.write(":")
        ids_str = reduce(lambda c1,c2: c1+","+c2, (str(c) for c in cast_container(ids)) )
        fout.write(ids_str)
        fout.write("\n")
        counter = counter + 1
    return counter

