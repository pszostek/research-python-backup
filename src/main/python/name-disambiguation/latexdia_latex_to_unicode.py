#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Classes describing regexes, which in turn describe the letters in latex and how to extract them from latexdia_unicode_to_latex.py dictionary. Created based on bolikowski.txt file.
author: mlukasik
"""

import re
from latexdia_unicode_to_latex import unicode_to_latex

def create_latex_to_unicode_dictionary():
	"""Call this method in order to get a dictionary Latex diacretic -> utf diacretic"""
	latex_to_unicode = {}
	#for each latex code
	for k, v in unicode_to_latex.iteritems():
		append_to_dict_if_matched(v, k, latex_to_unicode)
	append_to_dict_outside_latex_diacretic(latex_to_unicode)
	return latex_to_unicode

class latex_letter(object):
	"""Base class describing latex letters, how they are shown in the unicode_to_latex dictionary, and how they should be shown in context of cedram db"""
	latex_regexes = []
	
	@staticmethod
	def append_to_dict_if_matched(word, latex_to_unicode):
		print "append_to_dict_if_matched not implemented - this is an abstract class!"
		abstract()
		
class ld1(latex_letter):
	"""One type of latex letters: 2 characters, of which second is meaningful"""
	latex_regexes = [re.compile(r"\\(.){(.)}"), re.compile(r"\\(.){\\(.)}"), re.compile(r"\\(.){(.)?}")]
	
	@staticmethod
	def append_to_dict_if_matched(word, k, latex_to_unicode):
		for latex_diacretic in ld1.latex_regexes:
			if latex_diacretic.search(word) <> None:
			
				diacretic = list(latex_diacretic.search(word).groups())
				if len(diacretic)>0:
				#some of the fields may be empty
					for i in range(len(diacretic)):
						if diacretic[i] == None:
							diacretic[i] = " "
					
					latex_to_unicode[r"\\"+diacretic[0]+diacretic[1]] = k
					#latex_to_unicode[r"\"+diacretic[0]+diacretic[1]] = k instead of this, because Python does not allow this:
					latex_to_unicode[r"\%(ch1)c%(ch2)c" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
					latex_to_unicode[r"\\"+diacretic[0]+r"{"+diacretic[1]+r"}"] = k
					latex_to_unicode[r"\\"+diacretic[0]+r"{\\"+diacretic[1]+r"}"] = k
					
					#latex_to_unicode[r"\"+diacretic[0]+r"{"+diacretic[1]+r"}"] = k
					#latex_to_unicode[r"\"+diacretic[0]+r"{\"+diacretic[1]+r"}"] = k
					#instead of the above, because Python does not allow this:
					latex_to_unicode[r"\%(ch1)c{%(ch2)c}" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
					latex_to_unicode[r"\%(ch1)c{\%(ch2)c}" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
					#because of Kre{\u\i}n :
					latex_to_unicode[r"{\%(ch1)c\%(ch2)c}" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
					#because of Sidon-Telyakovski\u\i\ theorem
					latex_to_unicode[r"\%(ch1)c\%(ch2)c" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
					latex_to_unicode[r"\%(ch1)c %(ch2)c" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
		
class ld2(latex_letter):
	"""One type of latex letters: 1 char"""
	latex_regexes = [re.compile(r"\\(.) ")]
	
	@staticmethod
	def append_to_dict_if_matched(word, k, latex_to_unicode):
		for latex_diacretic in ld2.latex_regexes:
			if latex_diacretic.search(word) <> None:
				diacretic = list(latex_diacretic.search(word).groups())
				#Pawe{\l}czyk, Pawe{\l}czyk
				latex_to_unicode[r"\\%(ch1)c " % {'ch1' : diacretic[0]}] = k
				latex_to_unicode[r"\%(ch1)c " % {'ch1' : diacretic[0]}] = k
				latex_to_unicode[r"{\%(ch1)c}" % {'ch1' : diacretic[0]}] = k
		
class ld3(latex_letter):
	"""One type of latex letters: 2 meaningful characters"""
	latex_regexes = [re.compile(r"\\(.)(.) ")]

	@staticmethod
	def append_to_dict_if_matched(word, k, latex_to_unicode):
		for latex_diacretic in ld3.latex_regexes:
			if latex_diacretic.search(word) <> None:
				diacretic = list(latex_diacretic.search(word).groups())
				#S{\ae}ther
				#latex_to_unicode[r"\\%(ch1)c%(ch2)c" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
				latex_to_unicode[r"\%(ch1)c%(ch2)c " % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k
				latex_to_unicode[r"{\%(ch1)c%(ch2)c}" % {'ch1' : diacretic[0], 'ch2' : diacretic[1]}] = k

def append_to_dict_if_matched(v, k, latex_to_unicode):
	"""Applying append_to_dict_if_matched of each class in this file"""
	for ld in [ld1, ld2, ld3]:
		ld.append_to_dict_if_matched(v, k, latex_to_unicode)

def append_to_dict_outside_latex_diacretic(latex_to_unicode):
	"""Hand written (outside from the latex dict) with cutting the latin letters"""
	for special_letter in ['e', 'E', 'i', 'I', 'n', 'N', 'o', 'O', 's', 'z', 'Z']:
		for func in ['d', 'D']:
			latex_to_unicode[r"\%(ch1)c{" % {'ch1': func} +special_letter+"}"] = special_letter	
			latex_to_unicode[r"\%(ch1)c " % {'ch1': func} +special_letter] = special_letter	
		
	for special_letter in ['c', 'C', 'r', 'R', 'z', 'Z']:
		latex_to_unicode[r"\u{"+special_letter+"}"] = special_letter	
	
	for special_letter in ['g', 'a']:
		latex_to_unicode[r"\v{"+special_letter+"}"] = special_letter	
	
	for special_letter in ['g', 'G', 'n']:
		latex_to_unicode[r"\'"+special_letter] = special_letter	
	
	for special_letter in ['z', 'r', 's', 'S', 'u', 'a', 'g']:
		latex_to_unicode[r"\v {"+special_letter+"}"] = special_letter
	
	for special_letter in ['o', 'u', 'a']:
		latex_to_unicode[r"\B{"+special_letter+"}"] = special_letter
		latex_to_unicode[r"\B "+special_letter] = special_letter
		latex_to_unicode[r"\B {"+special_letter+"}"] = special_letter
	
	latex_to_unicode[r"\v "] = ""
	
	latex_to_unicode[r"\`n"] = "n"
	latex_to_unicode[r"\.a"] = "a"
	latex_to_unicode[r"\=g"] = "g"
	latex_to_unicode[r"\~g"] = "g"
	latex_to_unicode[r"\^Z"] = "Z"
	latex_to_unicode[r"{\Dj}"] = "j"
	latex_to_unicode[r"\l{}"] = "l"
	latex_to_unicode[r"\l"] = "l"
	latex_to_unicode[r"{\Dj}"] = "J"
	latex_to_unicode[r"\ogonek{e}"] = "e"
	
	latex_to_unicode[r" \& "] = u"&" #because it appears in the txt 
	latex_to_unicode[r"\ "] = " " #because it appears in the txt
	
