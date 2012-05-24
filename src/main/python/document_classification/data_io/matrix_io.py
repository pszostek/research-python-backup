"""IO for matrices, vectors, clusters' descriptors and others used for data exchange."""
import logging
import os,sys
from itertools import izip

def __read_tabs__(f):
    rowsStr = f.readline().replace('\n', '')
    rows = [x for x in rowsStr.split('\t') if len(x) > 0]
    return rows


def __read_ftabs__(f, cast_method=float):
    rowsStr = f.readline()
    rowsStr = rowsStr.replace('\n', '')
    rows = [cast_method(x) for x in rowsStr.split('\t') if len(x) > 0]
    return rows
    
def __read_itabs__(f):
    return __read_ftabs__(f, cast_method=int)

def __write_tabs__(f, lst):
    row_text = reduce(lambda e1,e2: e1+"\t"+e2, (str(e) for e in lst) )    
    f.write(row_text+"\n")    

def fread_smatrix(path, datareader=__read_ftabs__, rowlength=lambda rowno,numcols: 100000, maxrows=100000000):
    """Reads from file similarity matrix data."""
    f = open(path)    
    rows = __read_tabs__(f)
    cols = __read_tabs__(f)
    data = []
    for rowno,rowlabel in enumerate(rows):
        if rowno>=maxrows: break
        if rowno%500==0: logging.info("[fread_smatrix] "+str(rowno)+"rows loaded.")        
        row = datareader(f)
        data.append(row[:rowlength(rowno, len(row))])
    f.close()
    return (rows, cols, data)


def fread_smatrix_L(path, datareader=__read_ftabs__, maxrows=100000000):
    """Reads from file lower similarity matrix data."""
    return fread_smatrix(path, datareader, lambda rowno,numcols: rowno+1, maxrows)

def fread_smatrix_data(path, datareader=__read_ftabs__):
    """Reads from file similarity matrix data."""
    (rows, cols, data) = fread_smatrix(path, datareader)
    return data

def fread_smatrix_labels(path):
    """Reads from file similarity matrix rows' & columns' names."""
    f = open(path)    
    rows = __read_tabs__(f)
    cols = __read_tabs__(f)
    f.close()

    return (rows, cols)

def fwrite_smatrix(matrix, rows, cols, path):
    """Writes to file similarity matrix."""
    f = open(path, "w")
    __write_tabs__(f, rows)
    __write_tabs__(f, cols)    
    for rowdata in matrix:
        __write_tabs__(f, rowdata)
    f.close()

def fread_ivector(path):
    """Reads from file vector of integers."""
    f = open(path)
    lines = f.readlines()
    f.close()
    return [int(float(x.strip())) for x in lines]
    
def fread_svector(path):
    """Reads from file vector of strings."""
    f = open(path)
    lines = f.readlines()
    f.close()
    return [line.strip() for line in lines]

def fwrite_vector(path, vector):
    """Stores to file vector of data."""
    f = open(path, "w")
    for e in vector:
        f.write(str(e)+"\n")
    f.close()


def fwrite_clusters(clustdesc, path):
    """Writes to file information about clustering: list of pairs (etiquette, list of indexes)"""
    f = open(path, "w")
    for clust in clustdesc:
        f.write(clust[0]+"\t")
        for ix in clust[1]:
            f.write(str(ix)+"\t")
        f.write("\n")
    f.close()

def fread_clusters(path):
    """Reads from file information about clustering: list of pairs (etiquette, list of indexes)"""
    f = open(path, "r")
    clustdesc = []
    for line in f.readlines():
        cols = line.replace("\t\n","").split("\t")
        etiq = cols[0]
        ixs  = [int(str) for str in cols[1:len(cols)]]
        clustdesc.append( (etiq, ixs) )
    f.close()
    return clustdesc

def create_matrix(numrows, numcols, value = 0):
    return [ [value for i in range(0,numcols)] for j in range(0,numrows) ]

def set_diagonal(matrix, value):
    for ix in xrange(len(matrix)):
        matrix[ix][ix] = value
    return matrix

def sub_matrix(matrix, rowixs, colixs):
    """Generates new sub-matrix of given matrix."""
    return [ [matrix[r][c] for c in colixs] for r in rowixs ]

def serialize_matrix(matrix):
    """Returns matrix in single list: serializes row by row."""
    lst = []
    for row in matrix:
        lst.extend(row)
    return lst 

def extract_matrix_labels_file(fin, fout, argv):
    """From fin reads matrix and to fout prints rows' names."""
    labels = __read_tabs__(fin)
    for label in labels:
        fout.write(str(label))
        fout.write("\n")
    
def keep_submatrix_ids_file(fin, fout, argv):
    try:
        ids_path = argv[0] 
    except:
        print "Argument expected: path to a file with list of ids"
        sys.exit(-1)
        
    ids = set( line.strip() for line in open(ids_path).xreadlines() if len(line.strip())>0 )
    print "",len(ids),"ids loaded =",str(ids)[:100]
    
    rows = __read_tabs__(fin)    
    cols = __read_tabs__(fin)    
    __write_tabs__(fout, (row for row in rows if row in ids))
    __write_tabs__(fout, (col for col in cols if col in ids))
    
    col_ixs = list(ix for ix,col in enumerate(cols) if col in ids)        
    for row in rows:
        row_data = __read_tabs__(fin)
        if not row in ids: continue
        __write_tabs__(fout, (row_data[ix] for ix in col_ixs) )
    
def test_simmatrix_file(fin, fout, argv):    
    rows = __read_tabs__(fin)    
    cols = __read_tabs__(fin)    
    
    if len(rows)!=len(cols):
        print "Similarity matrix must be squared!"
        return 
    for row,col in izip(rows,cols):
        if row!=col:
            print "Row and col names must agree!"
            return
                
    for rowno,row in enumerate(rows):
        row_data = __read_ftabs__(fin)
        for colno,e in enumerate(row_data):
            if e<0.0 or e>1.0:
                print "Incorrect value=",e," in row=",rowno,"colno=",colno
        
    print "Validation done."


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
    fin = sys.stdin
    fout = sys.stdout
    sys.stdout = sys.stderr
    
    print "The program reads from stdin, processes matrix according to command, and prints out to stdout."
    
    subroutines = {}    
    subroutines["-labels"] = ("Extract rows (=labels) from matrix", extract_matrix_labels_file)
    subroutines["-filterids"] = ("[file-with-node-id-in-every-line] keeps submatrix with nodes of ids from list (file)", keep_submatrix_ids_file)
    subroutines["-simvalid"] = ("validates similarity matrix",test_simmatrix_file)

    try:
        cmd = sys.argv[1]
        print "Cmd =", cmd
        routine = subroutines[cmd][1]
        print "Subroutine =",routine         
    except:
        print "At least one argument expected: command"
        print "Supported commands:"
        for cmd,(desc,func) in subroutines.iteritems():
            print cmd,desc
        sys.exit(-1)
    
    routine(fin, fout, sys.argv[2:])
