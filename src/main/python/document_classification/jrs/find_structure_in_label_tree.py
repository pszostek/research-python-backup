'''
Created on Mar 24, 2012

@author: mlukasik
'''

def get_label_mappings_downwards(base_dict, res_dict, curr_depth, curr_node_id, curr_node_val):
    '''
    Save to res_dict the following information:
    (Leaf_id, depth) -> a node from which leaf_id is at 'depth' depth
    '''
    #print "[get_label_mappings] curr_depth, curr_node_id: ", curr_depth, curr_node_id
    if len(curr_node_val) == 0:
        #the end:
        #print "[get_label_mappings] leaf reached: ", curr_node_id
        res_dict[(curr_node_id, curr_depth)] = curr_node_id
        return 1, [curr_node_id]
    else:
        leaf_nodes = []
        #we need to go deeper:
        for child_id, child_node in curr_node_val.iteritems():
            #print "[get_label_mappings] considering child_id: ", child_id
            depth_aquired, received_leaf_nodes = get_label_mappings_downwards(base_dict, res_dict, 
                                                          curr_depth+1, child_id, child_node)
            #print "[get_label_mappings] received depth_aquired, received_leaf_nodes: ", depth_aquired, received_leaf_nodes
            
            for received_leaf_node in received_leaf_nodes:
                res_dict[(received_leaf_node, curr_depth)] = curr_node_id
            leaf_nodes+=received_leaf_nodes
            
            #print "[get_label_mappings] leaf_nodes: ", leaf_nodes
            #print "[get_label_mappings] res_dict: ", res_dict
            
        return depth_aquired+1, leaf_nodes

def get_label_mappings2(res_dict):
    from collections import defaultdict
    label_mappings = defaultdict(lambda: {})
    for key, value in res_dict.iteritems():
        label_mappings[key[1]][key[0]] = value
    return dict(label_mappings)

class A():
    d = {}
    def get_value(self, x):
        #print "[A]: get_value on x:", x, " with d:", self.d
        return self.d.get(x, x)

def get_label_mappings_functionlist(label_mappings):
    label_mapping_list = []
    #print "list(label_mappings.iteritems())", list(label_mappings.iteritems())
    for (counts, value) in sorted(label_mappings.iteritems(), key=lambda x: x[0], reverse=False):
        #print "counts", counts
        #print "value", value
        a = A()
        a.d = value
        label_mapping_list.append(a.get_value)#lambda x: value.get(x, x))
    return label_mapping_list[1:]

def find_leaves(key, d, leaves):
    if len(d)==0:
        leaves.add(key)
    else:
        for key, value in d.iteritems():
            find_leaves(key, value, leaves)

def find_not_continue_deepening(key, d, not_continue_deepening_elements, leaves):
    if len(d)==0:
        not_continue_deepening_elements.add(key)
    else:
        tobeadd = True
        for subkey, value in d.iteritems():
            if subkey not in leaves:
                tobeadd = False
            find_not_continue_deepening(subkey, value, not_continue_deepening_elements, leaves)
        if tobeadd:
            not_continue_deepening_elements.add(key)

def get_labeltree_data(base_dict):
    '''
    Extracts 3 data structures that are needed by hierarchical classification.
    '''
    res_dict = {}
    get_label_mappings_downwards(base_dict, res_dict, 0, 'ROOT', base_dict)
    #print "[res_dict]:", res_dict
    
    
    label_mappings = get_label_mappings2(res_dict)
    #print '[label_mappings]: ', label_mappings
    label_mapping_list = get_label_mappings_functionlist(label_mappings)
    
    leaves = set()
    find_leaves(None, base_dict, leaves)
    #print '[leaves]:', leaves, len(leaves)
    
    not_continue_deepening_elements = set()
    find_not_continue_deepening(None, base_dict, not_continue_deepening_elements, leaves)

    #print '[continue_deepening_elements]: ', continue_deepening_elements
    return label_mapping_list, not_continue_deepening_elements, leaves

base_dict = {'a80': {'a79': {'a76': {'59': {}, '51': {}}, 'a74': {'27': {}, 'a70': {'62': {}, 'a69': {'a38': {'68': {}, '53': {}}, 'a67': {'a59': {'a55': {'a50': {'56': {}, '28': {}}, 'a54': {'44': {}, '13': {}}}, 'a49': {'a47': {'a39': {'a33': {'5': {}, '14': {}}, '61': {}}, '4': {}}, '43': {}}}, 'a65': {'a57': {'25': {}, '63': {}}, '34': {}}}}}}}, 'a78': {'a77': {'a75': {'a72': {'a68': {'82': {}, '41': {}}, 'a71': {'a64': {'73': {}, 'a56': {'19': {}, '52': {}}}, 'a66': {'a58': {'69': {}, 'a53': {'a43': {'32': {}, 'a31': {'a23': {'77': {}, 'a4': {'72': {}, '22': {}}}, '17': {}}}, '70': {}}}, 'a61': {'a44': {'76': {}, 'a42': {'18': {}, 'a41': {'75': {}, 'a40': {'a37': {'39': {}, 'a35': {'a32': {'a28': {'26': {}, 'a25': {'a15': {'a13': {'a9': {'33': {}, '36': {}}, 'a11': {'a8': {'1': {}, 'a6': {'a3': {'a2': {'a1': {'a0': {'3': {}, '45': {}}, '29': {}}, '54': {}}, '37': {}}, '16': {}}}, '6': {}}}, 'a12': {'a7': {'2': {}, '66': {}}, '23': {}}}, '20': {}}}, 'a29': {'8': {}, 'a27': {'a22': {'a20': {'a17': {'a14': {'46': {}, '50': {}}, 'a10': {'9': {}, 'a5': {'47': {}, '42': {}}}}, '64': {}}, 'a19': {'31': {}, '58': {}}}, '67': {}}}}, 'a34': {'a30': {'15': {}, 'a26': {'a21': {'11': {}, 'a16': {'10': {}, '49': {}}}, 'a18': {'79': {}, '35': {}}}}, '38': {}}}}, '65': {}}}}}, '21': {}}}}}, 'a63': {'55': {}, 'a60': {'a51': {'a45': {'24': {}, '48': {}}, 'a36': {'74': {}, 'a24': {'71': {}, '78': {}}}}, 'a52': {'a46': {'80': {}, '40': {}}, 'a48': {'60': {}, '57': {}}}}}}, '7': {}}, 'a73': {'12': {}, '81': {}}}}, 'a62': {'83': {}, '30': {}}}
#print label_mapping_list
label_mapping_list, not_continue_deepening_elements, leaves = get_labeltree_data(base_dict)