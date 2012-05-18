from vector_metrics import *
from jrs_io import *
import sys,os

#notation: matrix == list of lists

def alloc_matrix(numrows, numcols, val):
    """Creates matrix filled with value val."""
    matrix = []
    for r in xrange(numrows):
        row = []
        for c in xrange(numcols):
            row.append(val)
        matrix.append(row)
    return matrix

def build_distm(datam, distance_calculator):
    """Takes matrix of data and returns matrix of distances between elements."""
    numrows = len(datam)
    distm = alloc_matrix(numrows, numrows, 0.0)    
    for r1 in xrange(numrows):
        print "calculating distance: row =",r1
        for r2 in xrange(r1, numrows):
            d = distance_calculator(datam[r1], datam[r2])
            distm[r1][r2] = d
            distm[r2][r1] = d
    return distm

def store_distm(outpath, distm):
    """Stores matrix of distances between elements into the file."""
    f = open(outpath, "w")
    for row in distm:
        last_element_i = len(row)-1
        for ei in xrange(last_element_i):
            f.write(str(row[ei]))
            f.write('\t')
        f.write(str(row[last_element_i]))
        f.write("\n")        
            
if __name__ == "__main__":
    print "The program calculates distances between objects of JRS-2012-Contest data..."
    try: 
        fpath   = sys.argv[1]
        method  = int(sys.argv[2])
        outpath = sys.argv[3]
    except:
        print "Data file expected as a first parameter!"
        print "Distance method (1/2/3/4) expected as a second parameter!"
        print "Output file expected as third parameter!"
        sys.exit(-1)
        
        
    print "Loading from",fpath,"..."
    datam = load_data(open(fpath), int)
    print len(datam),"rows loaded..."
    print len(datam[0]),"cols loaded..."
    print "Data range =",data_minvalue(datam),"-",data_maxvalue(datam),"..."
    
    if method == 1:
        print "Calculating cosine distance matrix..."
        distm = build_distm(datam, cosine_dist)
    else:
        print "Calculating euclid^2 distance matrix..."
        distm = build_distm(datam, euclid2_dist)
    
    print "Storing to",outpath,"..."
    store_distm(outpath, distm)
     
    print "Done."
    