'''
Created on Jan 25, 2012

@author: mlukasik
'''
from tree_node import Node

def PRINTER(x):
    #print x#logging.info(x)
    pass

def tree_dfs_builder(records, node_builder, children_splitter, max_depth, curr_depth, child_id, continue_deepening):
    """
    Build a tree in a dfs manner.
    
    records - list of elements that we are working on a current level
    
    node_builder(records, curr_depth, child_id) - procedure that builds content of a node based on a subset of records
    
    children_splitter(records, curr_depth, child_id) - how to split the elements amongst the children
    
    max_depth - when this depth is reached, then stop building further depths
    
    curr_depth - current depth of a current node
    
    child_id - identifier, which lets node_builder and children_splitter distinguish the important data in the records that are being passed;
                it's up to the user how to use this information
    
    continue_deepening(child_id) - function that answers to a question whether a child_id should be further divided
    """
    
    PRINTER("[tree_dfs_builder]: depth: "+str(curr_depth)+" child_id: "+str(child_id))
    PRINTER("[tree_dfs_builder]: creating a root node...")
    node = Node()
    node.content = node_builder(records, curr_depth, child_id)
    #PRINTER("[tree_dfs_builder]: node.content"+str(node.content))
    
    #PRINTER("[tree_dfs_builder]: for each child of a child: "+str(child_id)+" "+str(continue_deepening(child_id)))
    if curr_depth == 0 or (curr_depth < max_depth and continue_deepening(child_id)):
        PRINTER("[tree_dfs_builder]: splitting child data for child_id: "+str(child_id))
        child_data = children_splitter(records, curr_depth, child_id)
        #PRINTER("[tree_dfs_builder]: child_data"+str(child_data))
        node.children = {}
        #for each child=classification code on that level
        for child_id in child_data.iterkeys():
            #PRINTER("[tree_dfs_builder]: child_id"+child_id)
            node.children[child_id] = tree_dfs_builder(child_data[child_id], node_builder, children_splitter, max_depth, curr_depth+1, child_id, continue_deepening)
            
    return node

if __name__ == "__main__":
    #TODO: PUT THIS MAIN INTO TESTS
    records = lambda: [{'content': "1", 'code': "111SEP122"},
                       {'content': "2", 'code': "123SEP142"},
                       {'content': "3", 'code': "211SEP142"},
                       {'content': "4", 'code': "311SEP132"},
                       {'content': "5", 'code': "311SEP142"},
                       {'content': "6", 'code': "123SEP122"}]
    
    def node_builder(records, curr_depth, child_id):
        return child_id, records()
    
    def children_splitter(records, curr_depth, child_id):
        from collections import defaultdict
        children = defaultdict(lambda: [])
        for child in records():
            inserted_codes = set()
            for code in child['code'].split('SEP'):
                if code.startswith(child_id) and code[:curr_depth+1] not in inserted_codes:
                    children[code[:curr_depth+1]].append(child)
                    inserted_codes.add(code[:curr_depth+1])
        return dict(children)
        
    max_depth = 3
    curr_depth = 1
    
    n = tree_dfs_builder(records, node_builder, children_splitter, max_depth, curr_depth, '')
