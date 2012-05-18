

         
def testnodes(nodes, numnodes):
    for i in xrange(numnodes):
        if not str(i+1) in nodes:
            #print i+1
            return False
    return True

def extract_leaves(node, leaves):
    for name,subtree in node.iteritems():
        if len(subtree)>0:
            extract_leaves(subtree, leaves)
        else:
            leaves.append(name)
    return leaves

def get_max_depth(node):
    maxval = 0    
    for name,subtree in node.iteritems():
        maxval = max(maxval, 1+get_max_depth(subtree) )
    return maxval
                           
def extract_subtrees(node, depth_counter, subtrees):        
        if depth_counter <= 1:
            for name,subtree in node.iteritems():
                subtrees[name] = subtree
        else:
            for name,subtree in node.iteritems():
                if len(subtree) == 0:
                    subtrees[name] = {}
                else:
                    extract_subtrees(subtree, depth_counter-1, subtrees)
        return subtrees                    

def tree_flattening(tree, min_depth = 3, reduce_levels = 3):
    subtrees = {}         
    extract_subtrees(tree, reduce_levels, subtrees)
    
    flattree = {}
    for subtree_name, subtree in subtrees.iteritems():
        if len(subtree) == 0:
            flattree[subtree_name] = {}  
        elif get_max_depth(subtree)<min_depth:
            leaves = []
            extract_leaves(subtree, leaves)
            for leave in leaves:
               flattree[leave] = {}             
        else:
            flattree[subtree_name] = tree_flattening(subtree)        
        
    return flattree

if __name__=="__main__":
    #tree = {'a80': {'a79': {'a76': {'59': {}, '51': {}}, 'a74': {'27': {}, 'a70': {'62': {}, 'a69': {'a38': {'68': {}, '53': {}}, 'a67': {'a59': {'a55': {'a50': {'56': {}, '28': {}}, 'a54': {'44': {}, '13': {}}}, 'a49': {'a47': {'a39': {'a33': {'5': {}, '14': {}}, '61': {}}, '4': {}}, '43': {}}}, 'a65': {'a57': {'25': {}, '63': {}}, '34': {}}}}}}}, 'a78': {'a77': {'a75': {'a72': {'a68': {'82': {}, '41': {}}, 'a71': {'a64': {'73': {}, 'a56': {'19': {}, '52': {}}}, 'a66': {'a58': {'69': {}, 'a53': {'a43': {'32': {}, 'a31': {'a23': {'77': {}, 'a4': {'72': {}, '22': {}}}, '17': {}}}, '70': {}}}, 'a61': {'a44': {'76': {}, 'a42': {'18': {}, 'a41': {'75': {}, 'a40': {'a37': {'39': {}, 'a35': {'a32': {'a28': {'26': {}, 'a25': {'a15': {'a13': {'a9': {'33': {}, '36': {}}, 'a11': {'a8': {'1': {}, 'a6': {'a3': {'a2': {'a1': {'a0': {'3': {}, '45': {}}, '29': {}}, '54': {}}, '37': {}}, '16': {}}}, '6': {}}}, 'a12': {'a7': {'2': {}, '66': {}}, '23': {}}}, '20': {}}}, 'a29': {'8': {}, 'a27': {'a22': {'a20': {'a17': {'a14': {'46': {}, '50': {}}, 'a10': {'9': {}, 'a5': {'47': {}, '42': {}}}}, '64': {}}, 'a19': {'31': {}, '58': {}}}, '67': {}}}}, 'a34': {'a30': {'15': {}, 'a26': {'a21': {'11': {}, 'a16': {'10': {}, '49': {}}}, 'a18': {'79': {}, '35': {}}}}, '38': {}}}}, '65': {}}}}}, '21': {}}}}}, 'a63': {'55': {}, 'a60': {'a51': {'a45': {'24': {}, '48': {}}, 'a36': {'74': {}, 'a24': {'71': {}, '78': {}}}}, 'a52': {'a46': {'80': {}, '40': {}}, 'a48': {'60': {}, '57': {}}}}}}, '7': {}}, 'a73': {'12': {}, '81': {}}}}, 'a62': {'83': {}, '30': {}}}
    tree = {'31': {}, 'a80': {'a79': {'a76': {'a64': {'a32': {'20': {}, '36': {}}, 'a58': {'33': {}, '7': {}}}, 'a71': {'a42': {'a14': {'18': {}, '70': {}}, '2': {}}, 'a69': {'a37': {'1': {}, 'a19': {'3': {}, '66': {}}}, 'a56': {'a51': {'26': {}, '16': {}}, 'a47': {'a33': {'a28': {'37': {}, '29': {}}, 'a15': {'54': {}, '23': {}}}, '45': {}}}}}}, 'a3': {'77': {}, '6': {}}}, 'a78': {'a77': {'a74': {'a73': {'a72': {'a59': {'28': {}, 'a7': {'68': {}, '53': {}}}, 'a68': {'a65': {'a53': {'5': {}, 'a25': {'76': {}, 'a10': {'62': {}, '51': {}}}}, 'a44': {'a22': {'56': {}, 'a11': {'a1': {'73': {}, '52': {}}, '27': {}}}, 'a38': {'a23': {'a9': {'13': {}, 'a2': {'44': {}, '40': {}}}, '61': {}}, '4': {}}}}, 'a55': {'a50': {'63': {}, '59': {}}, 'a45': {'a26': {'25': {}, '14': {}}, '34': {}}}}}, 'a70': {'a66': {'a52': {'19': {}, 'a41': {'a29': {'a16': {'a0': {'46': {}, '50': {}}, '64': {}}, 'a12': {'8': {}, '38': {}}}, '67': {}}}, 'a62': {'a57': {'a36': {'a5': {'9': {}, '41': {}}, '42': {}}, 'a48': {'47': {}, 'a31': {'a24': {'39': {}, 'a4': {'75': {}, '65': {}}}, '58': {}}}}, 'a6': {'72': {}, '22': {}}}}, 'a63': {'82': {}, 'a34': {'55': {}, 'a21': {'15': {}, '43': {}}}}}}, 'a54': {'a18': {'24': {}, '48': {}}, 'a43': {'a30': {'a20': {'a8': {'57': {}, '74': {}}, '80': {}}, '60': {}}, 'a27': {'a13': {'71': {}, '79': {}}, '78': {}}}}}, 'a67': {'a60': {'a46': {'11': {}, '10': {}}, 'a40': {'21': {}, '49': {}}}, '35': {}}}, 'a75': {'a39': {'a17': {'69': {}, '81': {}}, '12': {}}, 'a61': {'30': {}, 'a49': {'17': {}, 'a35': {'32': {}, '83': {}}}}}}}}

          
    flattree = tree_flattening(tree, min_depth = 4, reduce_levels = 3)  
    print flattree
    
    
    flat_leaves = extract_leaves(flattree, leaves = [])
    print flat_leaves
    print testnodes(flat_leaves, 83)