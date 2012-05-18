'''
Created on Feb 22, 2012

@author: mlukasik
'''
def PRINTER(x):
    print x

def check_internal_data(hierarhical_mlknn):
    #----------------Functions needed to call tree_dfs_explorer---------------#
    def stop_condition(result_data, input_data, curr_depth, max_depth):
        if curr_depth == max_depth:
            #PRINTER("[MlHierarchical: stop_condition]: either curr_labels is empty or curr_depth reached max:"+str(curr_labels)+", "+str(curr_depth))
            return True
    def process_node(node, input_data, curr_depth):
        PRINTER("[MlHierarchical: process_node]: inspecting classifier on level: "+str(curr_depth))
        PRINTER("[MlHierarchical: process_node]: printing first 2 records...")
        
        i = 0
        for rec in node.content.frecords:
            PRINTER('[classify_stupid_no_exclude]: frecords '+str(rec))
            i+=1
            if i==2:
                break
            
        return None
        
    def iterate_through_children(node, result_data):
        for label in node.children.iterkeys():
            PRINTER("[MlHierarchical: iterate_through_children]: looking for classification as: "+str(label)+".")
            yield node.children[label]
    def postprocess_result_data(x):
        pass
    #----------------End of Functions needed to call tree_dfs_explorer---------------#
    
    import sys
    sys.path.append(r'../')
    from tools.tree_dfs_explorer import tree_dfs_explorer
    tree_dfs_explorer(None, hierarhical_mlknn.mltree, hierarhical_mlknn.max_depth, 0, stop_condition,
                  process_node, iterate_through_children, postprocess_result_data)
