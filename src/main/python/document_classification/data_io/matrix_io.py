"""IO for matrices, vectors, clusters' descriptors and others used for data exchange."""
import logging


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
    for e in lst:
        f.write(str(e)+"\t")
    f.write("\n")

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
