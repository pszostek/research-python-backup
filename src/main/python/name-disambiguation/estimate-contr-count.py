#!/usr/bin/env python

import re
import sys

def count_contributors(source, prefix = ''):
	counter = 0
	for line in source:
		if not line.startswith('au'):
			continue
		names = line[4:].split('; ')
		surnames = [name.split(',')[0] for name in names]
		if any(surname.startswith(prefix) for surname in surnames):
			counter += len(surnames)
	return counter

if __name__ == '__main__':
	prefix = ''
	if len(sys.argv) > 1:
		prefix = sys.argv[1]
	count = count_contributors(sys.stdin, prefix)
	print count
