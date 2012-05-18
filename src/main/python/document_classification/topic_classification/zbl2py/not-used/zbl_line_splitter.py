'''
Created on Nov 3, 2011

@author: mlukasik
'''

class ZblLineSplitter(object):
    '''
    Line splitter.
    '''
    FIRST_LEVEL_SEPARATOR = "\t;\t"
    SECOND_LEVEL_SEPARATOR = "\t,\t"
    
    @staticmethod
    def split_line(l):
        """split a line according to the splitting char-sequences. Append it to the rec dictionary: the key is the sequence of chars from the beggining to the first space
        returns the key that has now been added to the dictionary rec"""
        llist = l.replace("\n", "").split(" ")
        
        first_level = filter(lambda x: len(x), " ".join(llist[1:])[1:].split(ZblLineSplitter.FIRST_LEVEL_SEPARATOR))#first level split
        res2 = [filter(lambda x: len(x), i.split(ZblLineSplitter.SECOND_LEVEL_SEPARATOR)) for i in first_level] #second level split
        
        return (llist[0], res2)