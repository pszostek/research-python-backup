'''
Created on Nov 17, 2011

@author: mlukasik
'''
def highlevel2lowlevel(frecords, split_value):
    """
    Convert Low level MSC codes into High level
    
    frecords - iterable, where each element is a 2-element tuple:
            -first element is a numerical feature vector
            -second element is a list of labels
    """
    for rec in frecords:
        yield (rec[0], map(lambda s: s[:2],rec[1].split(split_value)))
