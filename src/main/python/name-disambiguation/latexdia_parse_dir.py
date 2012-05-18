#!/usr/bin/env python
"""Walks directory and for every file that is matching pattern converts TeX diactrics to UTF-8 (executes latexdia_parse)."""

import fnmatch
import sys, os
import re
import latexdia_parse


def walk_recursively(root_path, pattern, operator):
    """Walks recursively over directory and executes operator.next_file(file) on every file."""
    for root, dirs, files in os.walk(root_path):
        for filename in fnmatch.filter(files, pattern):
            operator.next_file( os.path.join(root, filename) )
            
def extract_file_name_ext(basename):
    """Returns pair (filename-without-extension, extension) from basename.
    
    Sample use:
    >>> extract_file_name_ext("ajoj.txt")
    ('ajoj', 'txt')
    >>> extract_file_name_ext("ajoj.xml.txt")
    ('ajoj.xml', 'txt')
    >>> extract_file_name_ext("ajoj")
    ('ajoj', '')
    """
    parts = basename.split(".")
    if len(parts) > 1:
        filename = reduce(lambda x,y: x+'.'+y, (parts[i] for i in xrange(0, len(parts)-1)) )
        extension = parts[len(parts)-1]
    else:
        filename = basename
        extension = ""
    return (filename, extension)        
        
            
class LatexdiaExecOperator():    
    
    def __init__(self, prefix, suffix):        
        self.prefix = prefix
        self.suffix = suffix
        self.file_counter = 0
    
    def next_file(self, src_path):        
        dir = os.path.dirname(src_path)
        fname = extract_file_name_ext(os.path.basename(src_path))[0]               
         
        dst_path =  os.path.join(dir, self.prefix+fname+self.suffix)                
        print "[",self.file_counter,"]Converting", src_path, "to", dst_path
        latexdia_parse.parse_file(src_path, dst_path)
        self.file_counter = self.file_counter + 1
        
                
            
if __name__ == '__main__':
    print "The program walks directory and for every file that is matching pattern converts TeX diactrics to UTF-8."
    
    import doctest
    doctest.testmod()
    
    try:        
        dir_path = sys.argv[1]
    except:
         print "First argument expected: directory-path"
         sys.exit(-1)
    try:        
        pattern = sys.argv[2]
    except:
         print "Second argument expected: pattern (for example: *.xml)"
         sys.exit(-1)         
    try:
        prefix = sys.argv[3]
    except:
        prefix = ""
    try:
        suffix = sys.argv[4]
    except:
        suffix = ".xml.utf"
         
         
    print "Walking directory:", dir_path
    print "Processing files matching pattern:", pattern         
    walk_recursively(dir_path, pattern, LatexdiaExecOperator(prefix, suffix))