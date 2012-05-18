"""
@author: mlukasik
16.11.11

Makes a snapshot of a source directory into a given directory,
copying only files of types specified.

Argument 1: source dir
Argument 2: destination (name for a dir).
Argument 3: filetypes that we want to be copied (e.g. py, cpp, m)

Example use:

python [name of this program] documents document_copy py cpp m
""" 

def force_dot_beginning(x):
    '''
    Puts '.' at the beginning of x if it isn't there yet
    '''
    if x.startswith('.'):
        return x
    return '.'+x

import sys
import os
import shutil

sourceDir = sys.argv[1]
destinationDir = sys.argv[2]
filetypes = sys.argv[3:]

filetypes = map(force_dot_beginning, filetypes)
#os.mkdir(destinationDir)
for root, dirs, files in os.walk(sourceDir, topdown=True):
    
    #print "root:", root, " dirs: ", dirs, " files: ", files
    #build destination subdirectory
    sroot = root.replace(sourceDir, destinationDir)
    os.mkdir(sroot)
    
    for filename in files:
        if reduce(lambda x, y: x or y, [filename.endswith(filetype) for filetype in filetypes]):
            pathNameFrom = os.path.join(root, filename)
            pathNameTo = os.path.join(sroot, filename)
            shutil.copyfile(pathNameFrom, pathNameTo)
