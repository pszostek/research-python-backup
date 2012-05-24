
def store_group2wids_list(f, group2wids_list):
    for group, wixs in group2wids_list:
        f.write(str(group)+":")
        wixs_line = reduce(lambda i1,i2: i1+","+i2, ( str(ix)+"-"+str(weight) for ix,weight in wixs) )
        f.write(wixs_line)     
        f.write("\n")
        
def load_group2wids_list(f):
    group2wids_list = []
    for line in f.xreadlines():
        parts = line.split(":")
        group = parts[0]
        elem_pairs = parts[1].split(",")
        wixs = list( (elem_pair.split("-")[0], float(elem_pair.split("-")[1]) ) for elem_pair in elem_pairs )
        group2wids_list.append( (group, wixs) )
    return group2wids_list
            
