from __future__ import division
from contextlib import nested
import string
import os
from disjointset import DisjointSet
from collections import defaultdict

def harmonic_mean(x, y):
    return 2 * x * y / (x + y)

citation_list = range(1, 1201)
record_list = range(1, 1001) + range(1201, 1401)

def get_correct_groups():
    citation_set = set(citation_list)
    record_set = set(record_list)
    both = citation_set & record_set
    cit_only = citation_set - both
    rec_only = record_set - both
    result = set()
    for n in both:
        result.add(frozenset(['c' + str(n),'r' + str(n)]))
    for n in cit_only:
        result.add(frozenset(['c' + str(n)]))
    for n in rec_only:
        result.add(frozenset(['r' + str(n)]))
    return result

class ResultSet:
    def __init__(self, name):
        self.name = name
        self.results = []
    def add(self, expected, answer):
        self.results.append((expected, answer))
    def get_groups(self):
        groups = {}
        global record_list, citation_list
        for r in record_list:
            groups['r' + str(r)] = DisjointSet()
        for c in citation_list:
            groups['c' + str(c)] = DisjointSet()
        for c,r in filter(lambda (x, y): -1 not in [x, y], self.results):
            cit = 'c' + str(c)
            rec = 'r' + str(r)
            groups[cit].union(groups[rec])
        rgroups = defaultdict(list)
        for k,v in groups.items():
            rgroups[v.find()].append(k)
        return set(map(frozenset, rgroups.values()))

    def count_all(self):
        return len(self.results)
    def count_correct(self):
        return sum(map(lambda (x, y): x == y, self.results))
    def compute_accuracy(self):
        return self.count_correct() / self.count_all()
    def count_existing_nonempty(self):
        return sum(map(lambda (x, y): x > -1, self.results))
    def count_matched_nonempty(self):
        return sum(map(lambda (x, y): y > -1, self.results))
    def get_correct_nonempty(self):
        return filter(lambda (x, y): x == y and x > -1, self.results)
    def count_correct_nonempty(self):
        return sum(map(lambda (x, y): x == y and x > -1, self.results))
    def compute_percision_nonempty(self):
        return self.count_correct_nonempty() / self.count_matched_nonempty()
    def compute_recall_nonempty(self):
        return self.count_correct_nonempty() / self.count_existing_nonempty()
    def compute_fmeasure_nonempty(self):
        return harmonic_mean(self.compute_percision_nonempty(), 
                             self.compute_recall_nonempty())
    def count_existing_empty(self):
        return sum(map(lambda (x, y): x == -1, self.results))
    def count_matched_empty(self):
        return sum(map(lambda (x, y): y == -1, self.results))
    def count_correct_empty(self):
        return sum(map(lambda (x, y): x == y and x == -1, self.results))
    def compute_percision_empty(self):
        return self.count_correct_empty() / self.count_matched_empty()
    def compute_recall_empty(self):
        return self.count_correct_empty() / self.count_existing_empty()
    def compute_fmeasure_empty(self):
        return harmonic_mean(self.compute_percision_empty(), 
                             self.compute_recall_empty())
    def compute_grouping_correctness(self):
        my = self.get_groups()
        correct = get_correct_groups()
        ok = correct & my
        return len(ok) / len(correct)
    def print_results(self):
        print "*** %s ***" % self.name
        print "accuracy:              %f" % self.compute_accuracy()
        print "reference percision:   %f" % self.compute_percision_nonempty()
        print "reference recall:      %f" % self.compute_recall_nonempty()
        print "reference F1:          %f" % self.compute_fmeasure_nonempty()
        print "nonexistent percision: %f" % self.compute_percision_empty()
        print "nonexistent recall:    %f" % self.compute_recall_empty()
        print "nonexistent F1:        %f" % self.compute_fmeasure_empty()
        print "grouping correctness:  %f" % self.compute_grouping_correctness()
    def get_csv(self):
        values = [self.name,
                  self.compute_accuracy(),
                  self.compute_percision_nonempty(),
                  self.compute_recall_nonempty(),
                  self.compute_fmeasure_nonempty(),
                  self.compute_percision_empty(),
                  self.compute_recall_empty(),
                  self.compute_fmeasure_empty(),
                  self.compute_grouping_correctness()]
        return ','.join(map(str, values))

class InternalMapping:
    def __init__(self, filename):
        self.mapping = {}
        with open(filename) as f:
            for line in f.readlines()[2:-2]:
                cells = map(string.strip, line.split(r'|'))
                self.mapping[cells[2]] = cells[1]
    def internalToId(self, internal):
        return int(self.mapping[internal]) if internal != 'None' else -1
    def correctToExpected(self, correct):
        return int(correct) if int(correct) <= 1000 else -1

class EmptyInternalMapping:
    def internalToId(self, internal):
        return int(internal) if internal != 'None' else -1
    def correctToExpected(self, correct):
        return int(correct) if int(correct) <= 1000 else -1

def load_icm_results(correct_file, answers_file, sourceid, internal_mapping):
    results = ResultSet(sourceid)
    answer_mapping = {}
    with open(answers_file) as answers:
        for line in answers.readlines()[2:-2]:
            cells = map(string.strip, line.split('|'))
            if cells[2] == sourceid:
                answer_mapping[int(cells[3]) - 1] = internal_mapping.internalToId(cells[4])
    with open(correct_file) as correct: 
        for i,c in enumerate(map(string.strip, correct.readlines())):
            results.add(internal_mapping.correctToExpected(c),
                        answer_mapping[i] if i in answer_mapping else -1)
    return results

def load_ujf_results(correct_file, answers_file, internal_mapping):
    results = ResultSet(os.path.splitext(os.path.basename(answers_file))[0])
    with open(correct_file) as correct: 
        with open(answers_file) as answers:
            for (c, a) in zip(map(string.strip, correct.readlines()), 
                              map(string.strip, answers.readlines())):
                results.add(internal_mapping.correctToExpected(c), 
                            internal_mapping.internalToId(a))
    return results
