#!/usr/bin/env python

import re
import sys

def build_records(source):
	record = {}
	for line in source:
		key, value = line.strip().split('  ', 1)
		if key == 'an' and record != {}:
			yield record
			record = {}
		record[key] = value
	if record != {}:
		yield record

def filter_records(records, prefix = ''):
	for record in records:
		if not 'au' in record:
			continue
		authors = record['au'].split('; ')
		surnames = (author.split(',', 1)[0] for author in authors)
		if any(surname.startswith(prefix) for surname in surnames):
			yield record

def map_records(records):
	rdict = {}
	for record in records:
		rid = record['an']
		rdict[rid] = record
	return rdict

def gather_cids(records):
	for record in records:
		authors = record['au'].split('; ')
		for i in xrange(len(authors)):
			yield '%s#%d' % (record['an'], i)

def ratio_value(setA, setB, n = -0.1):
	if len(setA) == 0 or len(setB) == 0:
		return 0.0
	ratio = 1.0 * len(setA & setB) / len(setA | setB)
	if ratio > 0.0:
		return ratio
	else:
		return n

def discrete_value(statement, p = 1.0, n = -1.0):
	if statement:
		return p
	else:
		return n

########################################
### Calculations of various features ###
########################################

def calc_surnames(recA, recB, iA, iB):
	surnameA = recA['au'].split('; ')[iA].split(',')[0]
	surnameB = recB['au'].split('; ')[iB].split(',')[0]
	return discrete_value(surnameA == surnameB)

def calc_initials(recA, recB, iA, iB):
	nameA = recA['au'].split('; ')[iA]
	nameB = recB['au'].split('; ')[iB]
	if ',' not in nameA or ',' not in nameB:
		return 0.0
	initialsA = re.sub('[^A-Z]', '', nameA.split(',')[1])
	initialsB = re.sub('[^A-Z]', '', nameB.split(',')[1])
	return discrete_value(initialsA == initialsB)

def calc_years(recA, recB, threshold = 70):
	if 'py' not in recA or 'py' not in recB:
		return 0.0
	yA = int(recA['py'])
	yB = int(recB['py'])
	diff = 1.0 - 2.0 * abs(yA - yB) / threshold
	if diff > 1.0:
		diff = 1.0
	if diff < -1.0:
		diff = -1.0
	return diff

def calc_ccontribs(recA, recB):
	if 'au' not in recA or 'au' not in recB:
		return 0.0
	authA = recA['au'].split('; ')
	surA = set(author.split(',', 1)[0] for author in authA)
	authB = recB['au'].split('; ')
	surB = set(author.split(',', 1)[0] for author in authB)
	return discrete_value(surA & surB, 1.0, -0.1)

def calc_keywords(recA, recB):
	if 'ut' not in recA or 'ut' not in recB:
		return 0.0
	kwA = set(recA['ut'].split('; '))
	kwB = set(recB['ut'].split('; '))
	return ratio_value(kwA, kwB)

def calc_codes(recA, recB):
	if 'cc' not in recA or 'cc' not in recB:
		return 0.0
	cA = set(recA['cc'][1:].split(' '))
	cB = set(recB['cc'][1:].split(' '))
	return ratio_value(cA, cB)

def calc_same(recA, recB, iA, iB):
	if 'ai' not in recA or 'ai' not in recB:
		return 0.0
	aiA = recA['au'].split('; ')[iA]
	aiB = recB['au'].split('; ')[iB]
	if aiA == '-' or aiB == '-':
		return 0.0
	return discrete_value(aiA == aiB)

########################################

def calculate_features(cidA, cidB, records, negOutFreq = 1):
	negCount = 0
	for i in xrange(len(cids)):
		for j in xrange(len(cids)):
			if i > j:
				cidA, cidB = cids[i], cids[j]
				recA = records[cidA.split('#')[0]]
				recB = records[cidB.split('#')[0]]
				iA = int(cidA.split('#')[1])
				iB = int(cidB.split('#')[1])
				same = calc_same(recA, recB, iA, iB)
				if same == 0.0:
					continue
				if same == -1.0:
					negCount += 1
					if negCount % negOutFreq != 0:
						continue

				surnames = calc_surnames(recA, recB, iA, iB)
				initials = calc_initials(recA, recB, iA, iB)
				years = calc_years(recA, recB)
				ccontribs = calc_ccontribs(recA, recB)
				keywords = calc_keywords(recA, recB)
				codes = calc_codes(recA, recB)
				row = map(str, [cidA + '#' + cidB, surnames, initials, years, ccontribs, keywords, codes, same])
				print ';'.join(row)


if __name__ == '__main__':
	prefix = ''
	if len(sys.argv) > 1:
		prefix = sys.argv[1]
	negOutFreq = 1000
	if len(sys.argv) > 2:
		negOutFreq = int(sys.argv[2])
	records = build_records(sys.stdin)
	records = filter_records(records, prefix)
	records = list(records)
	cids = list(gather_cids(records))
	records = map_records(records)
	calculate_features(cids, cids, records, negOutFreq)
