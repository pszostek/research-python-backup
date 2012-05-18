"""Functions that modify graphs represented as src-node-id:list-of-output-nodes-id."""
import logging
from collections import deque
import random
import sys

sys.path.append(r'../')
sys.path.append(r'../../')

from tools import stats
from tools.stats import *
from graph_io import *

####################################################################
####################################################################
####################################################################

def build_doublelinked_graph(src_id2ids, container = set):
    """Returns dictionary{id:container-of-ids} basing on src-graph structure.
    
    src_id2ids - graph given as dictionary{id: list-of-ids} 
    If records r1->r2 in src graph than in output graph there are two links: r1->r2 and r2->r1.
    """
    id2ids = {}
    for i, (curr_id,peer_ids) in enumerate(src_id2ids.iteritems()):
        if i%10000==0: logging.info("[extract_doublelinked_graph]"+str(i)+" records processed")
        id2ids[curr_id] = id2ids.get(curr_id, [])+peer_ids
        for c_id in peer_ids:            
            id2ids[c_id] = id2ids.get(c_id, [])+[curr_id]            
    return dict((id,container(ids)) for id,ids in id2ids.iteritems())

def is_doublelinked_graph(id2ids):
    """Returns True iff every edge has its other-direction complementary edge."""
    id2ids_set = dict( (id, set(ids)) for id,ids in id2ids.iteritems() ) 
    for id,peer_ids in id2ids_set.iteritems():
        for peer_id in peer_ids:
            if not id in id2ids_set[peer_id]:
                return False
    return True

def extract_doublelinked_graph(src_id2ids, container = set):
    """Historical version of build_doublelinked_graph."""
    return build_doublelinked_graph(src_id2ids, container)


def invert_graph_edges(src_id2ids):
    """Returns graph of inverted direction of edges.
    
    Graphs are represented as dictionary {src-node-id: dst-nodes-ids-container}
    """
    id2ids = {}
    for srcid, dstids in src_id2ids.iteritems():
        for dstid in dstids:
            id2ids[dstid] = id2ids.get(dstid, []) + [srcid]  
    return id2ids 

####################################################################
####################################################################
####################################################################



def extract_subgraph(id2ids, start_nodes_ids):
    """Returns subgraph of a given graph.
    
    Graph is given as a dictionary id2ids = {src_node_id: dst_nodes_ids_container}.
    Subgraph is returned in the same form but only those nodes are kept
    that are reachable from any of nodes from start_nodes_ids list.
    
    >>> g1 = {1: [3],2: [1], 3: [2]}
    >>> g2 = {4: [5, 6]}
    >>> g3 = {7: [9], 8: [9]}
    >>> g4 = {10: [11], 11: [12], 12: [13]}
    >>> g5 = {14: [15], 15: [18], 16: [18], 17: [18], 18: [19, 20], 20: [14]} 
    >>> id2ids = {}
    >>> id2ids.update(g1); id2ids.update(g2); id2ids.update(g3); id2ids.update(g4); id2ids.update(g5)        
    >>> extract_subgraph(id2ids, []) == {}
    True
    >>> extract_subgraph(id2ids, [3]) == g1
    True
    >>> extract_subgraph(id2ids, [4]) == g2
    True
    >>> extract_subgraph(id2ids, [7, 8]) == g3
    True
    >>> extract_subgraph(id2ids, [10, 12]) == g4
    True
    >>> extract_subgraph(id2ids, [17, 16]) == g5
    True
    >>> extract_subgraph(id2ids, [17, 16, 1]) == {1: [3],2: [1], 3: [2], 14: [15], 15: [18], 16: [18], 17: [18], 18: [19, 20], 20: [14]}
    True
    >>> extract_subgraph(id2ids, [14, 1]) == {1: [3],2: [1], 3: [2], 14: [15], 15: [18], 18: [19, 20], 20: [14]}
    True
    >>> extract_subgraph(id2ids, [14, 1, 11]) == {1: [3],2: [1], 3: [2], 14: [15], 15: [18], 18: [19, 20], 20: [14], 11: [12], 12: [13]}
    True
    """
    dst_graph = {}
    #def keep_ids(ids):
    #    for id in ids: 
    #        if (id in id2ids) and (not id in dst_graph):
    #            dst_graph[id] = id2ids[id]
    #            keep_ids(dst_graph[id])
    #keep_ids(start_nodes_ids)
    queue = deque(start_nodes_ids)
    while len(queue) > 0:
        id = queue.popleft()
        if (id in id2ids) and (not id in dst_graph):
            dst_graph[id] = id2ids[id]  
            queue.extend(dst_graph[id])
    return dst_graph 

def extract_subgraph_rigid_generator(id2ids, allowed_nodes_ids):
    """See: extract_subgraph_rigid."""
    allowed_nodes_ids = set(allowed_nodes_ids)
    for id in allowed_nodes_ids:
        if id in id2ids:
            peer_ids = [peer_id for peer_id in id2ids[id] if peer_id in allowed_nodes_ids]
            if len(peer_ids) > 0:
                yield(id, peer_ids)

def extract_subgraph_rigid(id2ids, allowed_nodes_ids):
    """Returns subgraph of a given graph.
    
    Graph is given as a dictionary id2ids = {src_node_id: dst_nodes_ids_container}.
    Subgraph is returned in the same form but only those nodes are kept
    that are on the allowed_nodes_ids list.
    >>> g1 = {1: [3],2: [1], 3: [2]}
    >>> g2 = {4: [5, 6]}
    >>> g3 = {7: [9], 8: [9]}
    >>> g4 = {10: [11], 11: [12], 12: [13]}
    >>> g5 = {14: [15], 15: [18], 16: [18], 17: [18], 18: [19, 20], 20: [14]} 
    >>> id2ids = {}
    >>> id2ids.update(g1); id2ids.update(g2); id2ids.update(g3); id2ids.update(g4); id2ids.update(g5)        
    >>> extract_subgraph_rigid(id2ids, []) == {}
    True
    >>> extract_subgraph_rigid(id2ids, [3,2,1]) == g1
    True
    >>> extract_subgraph_rigid(id2ids, [4]) == {}
    True
    >>> extract_subgraph_rigid(id2ids, [14,15,18,19,20]) == {14:[15],15:[18],18:[19,20],20:[14]}
    True
    """
    return dict( extract_subgraph_rigid_generator(id2ids, allowed_nodes_ids) )

####################################################################
####################################################################
####################################################################
        
def get_graph_nodes(id2ids):
    """Extracts set of nodes from graph given as dictionary{src-node-id:list-of-dst-nodes-ids}."""
    nodes = set()
    for id,ids in id2ids.iteritems():
        nodes.update([id])
        nodes.update(ids)
    return nodes


####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################


def divide_reachable_graphs(id2ids):
    """Divides given graph into partitions (sets) of nodes according to nodes reachability."""
    id2ids  = extract_doublelinked_graph(id2ids) #must have two-ways edges
    nodes   = get_graph_nodes(id2ids)    
    
    partitions = []
    reached_nodes = set()
    while len(nodes)>0:
        starting_node = nodes.pop()                
        queue = deque([starting_node])
        while len(queue) > 0:
            id = queue.popleft()
            if not id in reached_nodes:
                reached_nodes.update([id])
                try: nodes.remove(id) 
                except: pass
                if id in id2ids:                
                    queue.extend(id2ids[id])                    
        partitions.append(reached_nodes)
        reached_nodes = set()
    return partitions 


def random_graph(minnodes, maxnodes, minout, maxout):
    """Returns random graph in format {src-node-id:list-of-dst-nodes-ids}.
    
    [minnodes,maxnodes] - range for number of nodes
    [minout,maxout] - range for number of outgoing edges per every single node (independently)
    """    
    numnodes = random.randint(minnodes, maxnodes)
    nodes = range(numnodes)
    id2ids = {}
    for id in nodes:
        numout = random.randint(minout, maxout)
        id2ids[id] = random.sample(nodes, numout)
    return id2ids

####################################################################
####################################################################
####################################################################
####################################################################
####################################################################
####################################################################


def extract_subgraph_rigid_file(fin, fout, argv):     
    try:    
        ids_path = argv[0]
    except:
        print "Arg expected: list-of-ids"
        sys.exit(-1)
    try:    
        mode = int(argv[1])        
    except:
        print "Arg expected: mode-number:"
        print " 0 - calculates <reachable-starting-form-ids> subgraph "
        print " 1 - calculates <only-nodes-of-ids> subgraph "
        mode = 0
        print "Using default:",mode
        
    print "Loading graph from",fin
    id2ids = dict( yield_file_nodes(fin) )
    print len(id2ids),"lines loaded"
    print len(get_graph_nodes(id2ids)), "nodes loaded"
    #print "loaded graph:",id2ids
    
    print "Loading list of ids from",ids_path
    ids = [id.strip() for id in open(ids_path).xreadlines() if id.strip()!='']
    print len(ids),"lines loaded"
    #print "loaded ids:",ids

    if mode==0:
        print "Extracting <reachable-from-nodes-of-ids> subgraph"
        id2ids = extract_subgraph(id2ids, ids)
    elif mode==1:
        print "Extracting <only-nodes-of-ids> subgraph"
        id2ids = extract_subgraph_rigid(id2ids, ids)
    else:
        print "Wrong mode number (0/1 allowed)!"
        sys.exit(-2)
        
    print len(get_graph_nodes(id2ids)), "nodes kept"
    #ff = open("/tmp/kept_nodes.txt", "w")
    #for cc in sorted(get_graph_nodes(id2ids)): ff.write(str(cc)+"\n")            
    
    print "Printing out subgraph"#,id2ids
    write_file_id2ids(fout, list(id2ids.iteritems()))



def invert_graph_edges_file(fin,fout,argv):
    print "Loading graph from",fin
    id2ids = dict( yield_file_nodes(fin) )
    print len(id2ids),"lines loaded"
    print len(get_graph_nodes(id2ids)), "nodes loaded"
    #print "loaded graph:",id2ids

    print "Inverting edges"
    id2ids = invert_graph_edges(id2ids)
    print len(id2ids),"lines in output"
    print len(get_graph_nodes(id2ids)), "nodes"

    print "Printing out subgraph"#,id2ids
    write_file_id2ids(fout, list(id2ids.iteritems()), cast_container=set)

def make_doubleway_edges_graph_file(fin, fout, argv):
    print "Loading graph from",fin
    id2ids = dict( yield_file_nodes(fin) )
    print len(id2ids),"lines loaded"
    print len(get_graph_nodes(id2ids)), "nodes loaded"
    
    print "Converting graph to both-ways-edges graph."
    id2ids = extract_doublelinked_graph(id2ids)    
    print "Validating result:", is_doublelinked_graph(id2ids)    
    
    print "Printing out graph"#,id2ids
    write_file_id2ids(fout, list(id2ids.iteritems()))
    
def print_graph_analysis(fin,fout,argv):
    print "Loading graph from",fin
    id2ids = dict( yield_file_nodes(fin) )
    print len(id2ids),"lines (nodes with outgoing edges) loaded"

    id2numids = dict( (id,len(ids)) for id,ids in id2ids.iteritems())
    print "min outedges in line=",min(id2numids.values())
    print "avg outedges in line=",avg(id2numids.values())
    print "std outedges in line=",std(id2numids.values())
    print "max outedges in line=",max(id2numids.values())

    print len(get_graph_nodes(id2ids)), "nodes loaded"    
    
    partitions = divide_reachable_graphs(id2ids)
    partitions_len = [len(p) for p in partitions]  
    print len(partitions),"graph partitions"
    print "min partition size=",min(partitions_len)
    print "avg partition size=",avg(partitions_len)
    print "std partition size=",std(partitions_len)
    print "max partition size=",max(partitions_len)
    print "sum partition= size",sum(partitions_len)
    print "histogram:", sorted(list(hist(partitions_len).iteritems()))
   
    
    
    
def random_graph_file(fin,fout,argv):
    try:
        minnodes = int(argv[0])        
    except:
        print "Arg expected: minnodes"
        sys.exit(-1)
    try:
        maxnodes = int(argv[1])        
    except:
        print "Arg expected: maxnodes"
        sys.exit(-1)
    try:
        minout = int(argv[2])        
    except:
        print "Arg expected: min-outgoing-edges-per-node"
        sys.exit(-1)
    try:
        maxout = int(argv[3])        
    except:
        print "Arg expected: max-outgoing-edges-per-node"
        sys.exit(-1)
    print "minnodes=",minnodes
    print "maxnodes=",minnodes
    print "minout=",minout
    print "maxout=",minout

    id2ids = random_graph(minnodes, maxnodes, minout, maxout)
    print "Printing out graph"#,id2ids
    write_file_id2ids(fout, list(id2ids.iteritems()))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    fin = sys.stdin
    fout = sys.stdout
    sys.stdout = sys.stderr
    
    print "The program reads from stdin, processes graph according to command, and prints out to stdout."
    print "Typical graph format is in every line: srs-node-id:dst-node-id1,dst-node-id2,...,dst-node-idN"
    
    subroutines = {}    
    subroutines["-subgraph"] = ("[mode=0/1] extracts subgraph of a given graph (according to given list of nodes-ids)", extract_subgraph_rigid_file)
    subroutines["-dl"] = ("converts all edges in graph to double-way edges", make_doubleway_edges_graph_file)
    subroutines["-stats"] = ("prints out several graph's statistics", print_graph_analysis)    
    subroutines["-rand"] = ("[minnodes][maxnodes][minout][maxout] prints out random graph for given params", random_graph_file)
    subroutines["-inve"] = ("inverts edges' directions in graph", invert_graph_edges_file)
    

    try:
        cmd = sys.argv[1]
        print "Cmd =", cmd
        routine = subroutines[cmd][1]
        print "Subroutine =",routine         
    except:
        print "At least one argument expected: command"
        print "Supported commands:"
        for cmd,(desc,func) in subroutines.iteritems():
            print cmd,desc
        sys.exit(-1)
    
    routine(fin, fout, sys.argv[2:])
    
    
    
