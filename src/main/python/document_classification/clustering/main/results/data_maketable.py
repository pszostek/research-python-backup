

import sys,os

SEPARATOR = "\t"

def print_header(fout, columns):
    fout.write("#\t")
    for col in columns:
        fout.write(str(col)+"\t")
    fout.write("\n")

def print_data(fout, table, columns):
  for rowlabel, rowdata in table.iteritems():
        fout.write(str(rowlabel)+"\t")
        for col in columns:
            fout.write( str(rowdata.get(col,"?"))+"\t" )
        fout.write("\n")

def print_table(fout, table, columns):
    print_header(fout, columns)
    print_data(fout, table, columns)
  

def extract_table(lines, row_label_cols, col_label_cols, val_col, separator = SEPARATOR):
    table = {}
    columns = set() #=columns' labels
    for line in lines:
        line = line.strip()
        if line == "": continue
        cols = line.split(separator)

        row_label = reduce(lambda l1,l2: l1+separator+l2, (cols[colno] for colno in row_label_cols) )
        col_label = reduce(lambda l1,l2: l1+separator+l2, (cols[colno] for colno in col_label_cols) )
        val = cols[val_col]

        table_row = table.get(row_label, {}) 
        table_row[col_label] = val
        table[row_label] = table_row
        columns.add(col_label)
    return table, columns

if __name__=="__main__":
    fin = sys.stdin
    fout = sys.stdout
    sys.stdout = sys.stderr
    print "Reads file where every line is in format: col1[tab]col2[tab]...[tab]colN and prints out table." 
    print "Some columns are treated as rows' labels and some as columns' labels."
    
    try:
        row_label_cols = list(int(c) for c in sys.argv[1].split(',') )
        print "Numbers of columns to be interpreted as row labels:",row_label_cols
    except:        
        print "Numbers of columns to be interpreted as row labels expected as an argument of the program."
        sys.exit(-1)        

    try:
        col_label_cols = list(int(c) for c in sys.argv[2].split(',') )
        print "Numbers of columns to be interpreted as column labels:",col_label_cols
    except:        
        print "Numbers of columns to be interpreted as column labels expected as an argument of the program."
        sys.exit(-1)        

    try:
        val_col = int(sys.argv[3])
        print "The column with the value:", val_col
    except:
        print "The column with the value expected as an argument of the program."
        sys.exit(-1)

    table, columns = extract_table(fin.xreadlines(), row_label_cols, col_label_cols, val_col)
    print_table(fout, table, columns)

