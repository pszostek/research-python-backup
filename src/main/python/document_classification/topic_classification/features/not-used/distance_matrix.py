'''
Created on Nov 4, 2011

@author: mlukasik
'''
from distance_measure import dist

def gen_dist_matrix(records, how_many):
    """Builds distance matrix between the records O(n^2); how_many indicates, how many first elements are going to be compared to themselves"""
    dist_matrix = [[-1]*how_many]*how_many

    for i in range(how_many):#len(records)):
        print "generating row", i
        #if len(records[i]['ti']) > 0:
        for j in range(i+1, how_many):
            dist_matrix[i][j] = sum(dist(records[i], records[j]))
    #print dist_matrix
    return dist_matrix