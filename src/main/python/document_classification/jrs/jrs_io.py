
import numpy 
from numpy import matrix
import logging

#notation: matrix - list of list, f - handle to the file e.g. f = open('path.txt')


def file_append_line(path, line):
    f = open(path, "a")
    f.write(line+"\n")
    f.close()

def extract_submatrix(matrix, rows_first, rows_end, cols_first, cols_end):
    """Returns submatrix of a given matrix."""
    submatrix = []
    for r in xrange(rows_first, rows_end):
        submatrix.append( matrix[r][cols_first:cols_end] )
    return submatrix

def copy_matrix(matrix):
    """Returns copy of a given matrix."""
    copy = []
    for row in matrix:
        copy.append(list(e for e in row))
    return copy

def load_data(f, cast_method = int, numrows = 1000000, skip_rows = 0):
    """Loads numerical data from file (e.g. matrix from file). 
        
    Single line in file describes single row.
    Values in line should be separated by one of white-characters (e.g. tab,space).
    Values are cast using cast_method and then returned in list of lists structure."""      
    data = []
    for i,line in enumerate(f.xreadlines()):
        if i>=numrows: break
        if i<skip_rows: continue
        if i%1000 == 0: logging.info("[jrs_io.load_data]"+str(i)+"rows loaded...")
        row = [cast_method(x) for x in line.split()]
        data.append(row)
    return data

def store_data(fout, distances):
    for row in distances:
        last_ix = len(row)-1
        for eix in xrange(last_ix):
            fout.write(str(row[eix]))
            fout.write("\t")
        fout.write(str(row[last_ix]))
        fout.write("\n")


def store_labels(f, labels):
    for i,ll in enumerate(labels):
        try:        
            ll_str = reduce(lambda x,y: x+','+y, (str(l) for l in sorted([int(l) for l in ll]) ) )
        except:
            ll_str = ""
            #print "[store_labels] failure in row",i," (probably empty row)"            
        f.write(ll_str+'\n')      

def load_labels(f, cast_method = int, separator=','):
    """Returns list of lists (labels) loaded from file f.
    
    Single row (must be in format: l1,l2,l3,l4,l5,\n where li means i-th label) 
    is converted to single list of labels.     
    Then list are packed in another lists.
    Values are cast using cast_method and then returned in list of lists structure.    
    """ 
    data_labels = []   
    for line in f.xreadlines():
        labels = list( cast_method(label) for label in line.strip().split(separator) if len(label)>0 )
        data_labels.append(labels)
    return data_labels   
    
def data_maxvalue(datam):  
    """Returns max value from matrix datam."""
    maxvalue = -1000000000  
    for row in datam:
        maxvalue = max(maxvalue, max(row))
    return maxvalue

def data_minvalue(datam):  
    """Returns min value from matrix datam."""
    minvalue = 1000000000  
    for row in datam:
        minvalue = min(minvalue, min(row))
    return minvalue


def load_data_m(f, data_type = int): #NUMPY OUTPUT
    """Loads numerical data from file (e.g. matrix from file). 
        
    Single line in file describes single row.
    Values in line should be separated by one of white-characters (e.g. tab,space).
    Values are cast using cast_method and then returned in numpy.matrix."""    
    txt = f.read()
    txt = txt.replace('\n',';');
    return matrix(txt, dtype=data_type)



#f = open('/home/tkusm/jrs/trainingData.csv')

