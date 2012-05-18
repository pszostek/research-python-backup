'''
Created on Apr 9, 2012

@author: mlukasik
'''
            
def find_all_labels(records, get_labels_of_record):
    '''
    Find all labels in the data.
    
    List of labels is returned, where each distinct label occurs exactly once.
    '''
    all_labels = set()
    for record in records:
        #print '[find_all_labels]: record:', record, 'set(self.get_labels_of_record(record)):', set(self.get_labels_of_record(record))
        all_labels = all_labels | set(get_labels_of_record(record))
    return list(all_labels)