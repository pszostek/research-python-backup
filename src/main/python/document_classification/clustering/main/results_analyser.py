"""Parses build_msc_tree results and extracts simulation results."""

import sys,os

RESULT_STR = "RESULT"
METHOD_STR = "method ="
ZBL_STR = "zbl ="
SIMMATRIX_STR = "simmatrix ="
RESULTS_STR = "=>" 

def parse_results_line(line):
    method_ix = line.find(METHOD_STR)
    zbl_ix = line.find(ZBL_STR)
    clustering_str = line[method_ix+len(METHOD_STR): zbl_ix].strip()
    
    sim_start_ix = line.find(".",line.find(SIMMATRIX_STR))+1
    sim_end_ix = line.find(RESULTS_STR)
    similarity_str = line[sim_start_ix: sim_end_ix].strip()

    similarity_indexes = []
    values = line[sim_end_ix+len(RESULTS_STR):].strip()
    values_parts = values.split("),")
    for i in xrange(0, len(values_parts), 2):
        clusters = values_parts[i]
        simixs = values_parts[i+1]
        method_name = clusters[clusters.find('\'')+1: clusters.find('\'', clusters.find('\'')+1)]
        clusters_lm = clusters[clusters.find("((")+2:]   
        simixs_parts = simixs.replace(")","").replace("}","").replace(" ","").split(",")
        simixs_value = '%.3f' % float(simixs_parts[0])#.replace('\'',"").replace(".",",")
        simixs_std = '%.3f' % float(simixs_parts[1])#.replace('\'',"").replace(".",",")
        similarity_indexes.append( (method_name, clusters_lm, simixs_value, simixs_std) )
        
    return similarity_str, clustering_str, similarity_indexes  
        
def format_linkage_str(linkage):
    if linkage == "s":
       linkage = "single"
    elif  linkage == "c" or linkage == "m":
        linkage = "complete"
    elif  linkage == "a":
        linkage = "avg"
    elif linkage.startswith("avgw"):
        linkage = linkage.replace("w", "-")
    return linkage
        
def format_clustering_str(clustering_str):        
    clustering_parts = clustering_str.split("-")
    if clustering_parts[0] == "3lupgma":
        clustering_parts[0] = "upgma 3levels"
    elif  clustering_parts[0] == "3lkmedoids":
        clustering_parts[0] = "kmedoids 3levels"
    return format_linkage_str(clustering_parts[1])+"\t"+format_linkage_str(clustering_parts[2])+"\t"+clustering_parts[0]
    
def format_similarity_str(similarity_str, mapping = {}):
    similarity_parts = similarity_str.split(".")
    for key,value in mapping.iteritems():
        if similarity_parts[0].startswith(key):
            similarity_parts[0] = similarity_parts[0].replace(key,value)
    if similarity_parts[1] == "angular":
        similarity_parts[1] = "Cosine"
    elif similarity_parts[1] == "tv":
        similarity_parts[1] = "Tversky"
    return similarity_parts[0]+"\t"+similarity_parts[1]

def format_similarity_indexes(similarity_indexes):
    return reduce(lambda l1,l2: l1+"\t"+l2, (s[1]+"\t"+s[2]+"\t"+s[3] for s in similarity_indexes))



if __name__=="__main__":
    fin     = sys.stdin
    fout    = sys.stdout
    sys.stdout = sys.stderr
    print "Parses build_msc_tree results and extracts simulation results."    
    
    mapping = {}
    for arg in sys.argv[1:]:
        split_pos = arg.find(":")
        key = arg[:split_pos]
        value = arg[split_pos+1:]
        mapping[key]   = value    
    print "mapping=",mapping
    
    processed = 0
    for line in fin.xreadlines():
        if not line.count(RESULT_STR)>0: continue                
        similarity_str, clustering_str, similarity_indexes = parse_results_line(line)
        fout.write(format_clustering_str(clustering_str)+"\t"+format_similarity_str(similarity_str, mapping)+"\t"+format_similarity_indexes(similarity_indexes))
        fout.write("\n")
        processed = processed + 1
        
    print processed," lines processed"