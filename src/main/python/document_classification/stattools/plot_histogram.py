#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 21, 2012

@author: mlukasik
'''
from matplotlib import pyplot

#kodow msc na dokument:
d = {16: 1,
12: 2,
14: 2,
13: 4,
11: 6,
10: 18,
9: 27,
8: 70,
7: 142,
6: 385,
5: 1026,
4: 2663,
3: 5671,
2: 6881,
1: 3376}
"""

#wystapien danego kodu msc na liczbe takich kodow
d = {71 : 1,
74 : 1,
76 : 1,
83 : 1,
91 : 1,
92 : 1,
96 : 1,
102 : 1,
103 : 1,
110 : 1,
112 : 1,
117 : 1,
119 : 1,
120 : 1,
122 : 1,
126 : 1,
129 : 1,
130 : 1,
138 : 1,
144 : 1,
145 : 1,
157 : 1,
162 : 1,
174 : 1,
185 : 1,
205 : 1,
216 : 1,
228 : 1,
233 : 1,
264 : 1,
53 : 2,
56 : 2,
63 : 2,
64 : 2,
69 : 2,
77 : 2,
80 : 2,
82 : 2,
84 : 2,
86 : 2,
87 : 2,
88 : 2,
93 : 2,
97 : 2,
98 : 2,
107 : 2,
114 : 2,
123 : 2,
142 : 2,
66 : 3,
68 : 3,
70 : 3,
75 : 3,
95 : 3,
124 : 3,
60 : 4,
61 : 4,
62 : 4,
65 : 4,
78 : 4,
116 : 4,
47 : 5,
50 : 5,
54 : 5,
59 : 5,
90 : 5,
55 : 6,
57 : 6,
72 : 6,
81 : 6,
39 : 7,
44 : 7,
45 : 7,
48 : 7,
52 : 7,
46 : 8,
49 : 8,
51 : 8,
58 : 8,
33 : 10,
37 : 11,
35 : 12,
41 : 12,
42 : 12,
43 : 13,
38 : 14,
31 : 15,
30 : 16,
36 : 16,
32 : 18,
34 : 18,
29 : 19,
40 : 20,
27 : 21,
28 : 26,
26 : 27,
24 : 29,
25 : 29,
23 : 36,
20 : 40,
22 : 40,
21 : 45,
17 : 50,
19 : 57,
16 : 62,
14 : 66,
18 : 68,
15 : 72,
12 : 94,
13 : 100,
11 : 127,
10 : 133,
8 : 148,
9 : 151,
7 : 212,
5 : 262,
6 : 265,
4 : 325,
3 : 414,
2 : 626,
1 : 1172}
l = reduce(lambda x, y: x+y, [[j]*i for i, j in d.iteritems()])

"""

"""
#print "l:", l
n, bins, patches = pyplot.hist(l, bins = 50, log=True, rwidth = 1.0)#, histtype='bar')

#pyplot.axis([0, 1200, 1, 10000])
pyplot.xlabel("Liczba wystapien kodu w korpusie.")
pyplot.ylabel("Liczba roznych kodow MSC.")
#pyplot.title("Ilosci kodow MSC o danej liczbie wystapien w korpusie.")
pyplot.show()

"""
import numpy as np
import matplotlib.pyplot as plt
print "d:", d
counts = range(min(d.iterkeys()), max(d.iterkeys())+1)
print "counts:", counts
num_of_docs = map(lambda x: d.get(x, 0), counts)
#alphab = ['A', 'B', 'C', 'D', 'E', 'F']
#frecuencies = [23, 44, 12, 11, 2, 10]

#pos = counts
pos = np.arange(len(counts))
width = 1.0     # gives histogram aspect to the bar diagram

ax = plt.axes()
ax.set_xticks(pos + (width / 2))
ax.set_xticklabels(counts)

plt.bar(pos, num_of_docs, width, color='b', log=True)

pyplot.xlabel("Liczba kodow opisujacych dokument.")
#pyplot.xlabel("Liczba kodow o takiej wlasnosci.")
pyplot.ylabel("Liczba dokumentow.")
#pyplot.ylabel("Liczba wystapien kodow w korpusie.")
#pyplot.title("Liczby kodow o danej licznie wystapien.")

plt.show()
