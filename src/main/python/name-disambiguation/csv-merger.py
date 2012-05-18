#!/usr/bin/env python
"""Joins files with features. Requires a list of files, each containing:
id1 v1
id2 v2
id3 v2
etc..."""
import sys

def readFullLine(iterables):
	"""izip rewritten here; It's just that izip doesn't want to work with lists"""
	iterables = map(iter, iterables)
	while iterables:
		yield tuple(map(next, iterables))

if __name__ == '__main__':
	#for a in izip(readLine(sys.argv[1]), readLine(sys.argv[2])): #for i in range(1, len(sys.argv))):
	#	print a
	#for a in izip((readLine(sys.argv[i]) for i in range(1, len(sys.argv)))):
	#	print a
	for line in readFullLine([open(sys.argv[i]) for i in range(1, len(sys.argv))]):
		line_parsed = [l.split() for l in line]
		line_res = line_parsed[0][0]+" "+line_parsed[0][1]
		for i in range(1, len(line_parsed)):
			line_res += " "+line_parsed[i][1]
		print line_res
