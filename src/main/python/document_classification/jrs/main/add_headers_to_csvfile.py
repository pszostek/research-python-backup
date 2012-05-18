#! /usr/bin/env python

import sys

if __name__=="__main__":
    print "Argument expected: path to CSV file."


    for path in  sys.argv[1:]:    
             
        print "Loading",path
        f = open(path)             
        lines = f.readlines()
        print "numlines:",len(lines)
        print "numcols:",len(lines[0].split(','))
        f.close()
        
        print "Overwritting",path
        f = open(path, "w")
        for i in xrange(len(lines[0].split(','))-1):
            f.write("f"+str(i)+",")
        f.write("c\n")
        for line in lines:
            f.write(line.strip()+"\n")
        f.close()