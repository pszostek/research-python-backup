'''
Created on Mar 25, 2012

@author: mlukasik
'''

import find_structure_in_label_tree
base_dict = {'a80': {'a79': {'a76': {'59': {}, '51': {}}, 'a74': {'27': {}, 'a70': {'62': {}, 'a69': {'a38': {'68': {}, '53': {}}, 'a67': {'a59': {'a55': {'a50': {'56': {}, '28': {}}, 'a54': {'44': {}, '13': {}}}, 'a49': {'a47': {'a39': {'a33': {'5': {}, '14': {}}, '61': {}}, '4': {}}, '43': {}}}, 'a65': {'a57': {'25': {}, '63': {}}, '34': {}}}}}}}, 'a78': {'a77': {'a75': {'a72': {'a68': {'82': {}, '41': {}}, 'a71': {'a64': {'73': {}, 'a56': {'19': {}, '52': {}}}, 'a66': {'a58': {'69': {}, 'a53': {'a43': {'32': {}, 'a31': {'a23': {'77': {}, 'a4': {'72': {}, '22': {}}}, '17': {}}}, '70': {}}}, 'a61': {'a44': {'76': {}, 'a42': {'18': {}, 'a41': {'75': {}, 'a40': {'a37': {'39': {}, 'a35': {'a32': {'a28': {'26': {}, 'a25': {'a15': {'a13': {'a9': {'33': {}, '36': {}}, 'a11': {'a8': {'1': {}, 'a6': {'a3': {'a2': {'a1': {'a0': {'3': {}, '45': {}}, '29': {}}, '54': {}}, '37': {}}, '16': {}}}, '6': {}}}, 'a12': {'a7': {'2': {}, '66': {}}, '23': {}}}, '20': {}}}, 'a29': {'8': {}, 'a27': {'a22': {'a20': {'a17': {'a14': {'46': {}, '50': {}}, 'a10': {'9': {}, 'a5': {'47': {}, '42': {}}}}, '64': {}}, 'a19': {'31': {}, '58': {}}}, '67': {}}}}, 'a34': {'a30': {'15': {}, 'a26': {'a21': {'11': {}, 'a16': {'10': {}, '49': {}}}, 'a18': {'79': {}, '35': {}}}}, '38': {}}}}, '65': {}}}}}, '21': {}}}}}, 'a63': {'55': {}, 'a60': {'a51': {'a45': {'24': {}, '48': {}}, 'a36': {'74': {}, 'a24': {'71': {}, '78': {}}}}, 'a52': {'a46': {'80': {}, '40': {}}, 'a48': {'60': {}, '57': {}}}}}}, '7': {}}, 'a73': {'12': {}, '81': {}}}}, 'a62': {'83': {}, '30': {}}}
#print label_mapping_list
label_mapping_list, not_continue_deepening_elements, leaves = find_structure_in_label_tree.get_labeltree_data(base_dict)

base_dict2 = {'a79': {}, 'a78': {}}
for l in leaves:
    for label_mapping in label_mapping_list:
        if label_mapping(l) == 'a79':
            base_dict2['a79'][l] = {}
            break
        elif label_mapping(l) == 'a78':
            base_dict2['a78'][l] = {}
            break

print base_dict2