#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Parse files to latin letters unicode or utf-8"""

from latexdia_latex_to_unicode import create_latex_to_unicode_dictionary
import sys
import datetime
import string
import codecs

def parse_file(src_path, dst_path):
	""" Parses src file to latin letters unicode or utf-8."""
	latex_to_unicode = create_latex_to_unicode_dictionary()
	with open(src_path) as fload:
		fsave = codecs.open(dst_path, "w", "utf-8", errors="ignore")
		for l in fload:
			l_new = l.decode('utf-8', 'ignore')
			for k, v in latex_to_unicode.items():
				l_new = string.replace(l_new, k, v)
	  		fsave.write(l_new)
	  	fsave.close()

if __name__ == '__main__':
	parse_file(sys.argv[1], sys.argv[2])

