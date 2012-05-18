'''
Created on April, 10, 2011

@author: mlukasik
'''

def find_closest_points_sorted(sample, records, excluding, k, distance):
    """
    Find k closest records and return sorted list of them in a sorted way: from closest to furthest; 
    time complexity: O(log(k)*len(records) + klog(k))
    
    A heap is used, to store the k best matches, when iterating through data.
    
    sample - a record, neighbours of which we are lokking for
    records - a generator over records 
    excluding - list of records not to consider
    k - number of closest points to find
    distance - a function distance(record1, record2) -> distance between them
    """
    import heapq
    best_matches = []
    elems_cnt = 0
    
    for r in records:
        if not excluding or r not in excluding:
            curr_err = distance(r, sample)
            if elems_cnt < k:
                heapq.heappush(best_matches, (-curr_err, r))
                elems_cnt += 1
                
            elif -best_matches[0][0] > curr_err:
                #remove the biggest error and add the new element
                heapq.heappushpop(best_matches, (-curr_err, r))
    
    best_matches = sorted(best_matches, key=lambda x: x[0], reverse=True)
    #print '[find_closest_points_sorted] best_matches:', best_matches
    return map(lambda x: x[1], best_matches)
