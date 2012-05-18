"""
Counts occurrences of code categories and pairs of categories basing on ZBL.

Source: matrix of categories coocurrences (see io module).
"""

#Zlicza wystepowanie kategorii i par kategorii w danych wygenerowanych na podstawie ZBL.
#Na wejsciu: macierz wspolwystapien kategorii

import io

import sys

def smatrix_pair_count(matrix, labels):
    """Takes symmetric co-ocurrence matrix and builds dictionary{pair_id: pair_count}"""
    pair_count   = {}
    for r in xrange(0, len(labels)):
        for c in xrange(r+1, len(labels)):
            if matrix[r][c] > 0:
                pair_count[ labels[r]+"_"+labels[c] ] = matrix[r][c]
    return pair_count

def smatrix_single_count(matrix, labels):
    """Takes symmetric co-ocurrence matrix and builds dictionary{category: its_count}"""
    return dict( ( (labels[i], matrix[i][i]) for i in xrange(len(labels))) ) #dictionary {category: its count}



if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        print "[ERROR] Exactly two arguments are expected: input-categories-coocurrence-matrix-path output-stats-path-prefix"
        exit(-1)
    matrixInPath    = args[1]
    statsOutPath    = args[2]


    #load matrix:
    matrix = io.fread_smatrix_data(matrixInPath)
    labels = io.fread_smatrix_labels(matrixInPath)[0]

    #counting
    single_count    = smatrix_single_count(matrix, labels)
    pair_count      = smatrix_pair_count(matrix, labels)

    #storing:
    io.fwrite_vector(statsOutPath+"_single_labels.svector", single_count.keys())
    io.fwrite_vector(statsOutPath+"_single_count.ivector", single_count.values())
    io.fwrite_vector(statsOutPath+"_pair_labels.svector", pair_count.keys())
    io.fwrite_vector(statsOutPath+"_pair_count.ivector", pair_count.values())

