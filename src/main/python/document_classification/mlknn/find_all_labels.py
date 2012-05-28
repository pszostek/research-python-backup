'''
Created on Apr 9, 2012

@author: mlukasik
'''
            
def find_all_labels(records, get_labels_of_record):
    '''
    Find all labels in the data.
    
    List of labels is returned, where each distinct label occurs exactly once.
    
    Sample use:
    >>> sorted(find_all_labels([('a', 1), ('b', 2), ('c', 1), ('d', 3)], lambda x: [x[1]]))
    [1, 2, 3]
    >>> sorted(find_all_labels([('a', 1), ('b', 2), ('c', 1), ('c', 3)], lambda x: [x[0]]))
    ['a', 'b', 'c']
    '''
    all_labels = set()
    for record in records:
        all_labels = all_labels | set(get_labels_of_record(record))
    return list(all_labels)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
