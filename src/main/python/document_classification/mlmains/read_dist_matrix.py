
from __future__ import division
from itertools import izip

import sys
sys.path.append(r'../')
from data_io.matrix_io import fread_smatrix


filename = sys.argv[1]

(rows, cols, data) = fread_smatrix(filename)

print "(rows, cols, data):", (rows, cols, data)