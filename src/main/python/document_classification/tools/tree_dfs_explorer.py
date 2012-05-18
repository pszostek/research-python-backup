'''
Created on Feb 2, 2012

@author: mlukasik
'''

def PRINTER(x):
    #print '[tree]', x#logging.info(x)
    pass

def tree_dfs_explorer(input_data, node, max_depth, curr_depth, stop_condition,
                      process_node, go_downwards, postprocess_result_data):
    '''
    Process tree in a recursive way and gather result data.

    stop_condition(result_data, input_data, curr_depth, max_depth) - when to stop the search
    process_node(node, input_data, curr_depth) - specifies what to do to generate results from current node
    go_downwards(node, result_data) - extract child node
    postprocess_result_data(result) - performs final instructions on result
    
    '''
    PRINTER('[tree_dfs_explorer]: call on depth:'+str(curr_depth))
    #process node
    result_data = process_node(node, input_data, curr_depth)
    if not result_data:
        PRINTER('[tree_dfs_explorer]: no result label returned!')
        return []
    
    result = []
    
    PRINTER('[tree_dfs_explorer]: child_nodes iteration...')
    for result_datum in result_data:
        #if this is the final level, return the result
        if stop_condition(result_datum, input_data, curr_depth, max_depth):
            PRINTER('[tree_dfs_explorer]: stop condition passed! Adding: '+str(result_datum))
            result.append([result_datum])
        else:
            child_node = go_downwards(node, result_datum)
            #PRINTER('[tree_dfs_explorer]: child_node:'+str(child_node))
            result.append(tree_dfs_explorer(input_data, child_node, max_depth, curr_depth+1, stop_condition,
                          process_node, go_downwards, postprocess_result_data))
    
    PRINTER('[tree_dfs_explorer]: result before postprocess: '+str(result))
    result = postprocess_result_data(result)
    PRINTER('[tree_dfs_explorer]: result after postprocess: '+str(result))
    
    return result

if __name__ == "__main__":
    pass
