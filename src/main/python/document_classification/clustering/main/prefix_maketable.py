

import sys,os
import data_maketable

def extract_table(lines, separator = "\t"):
    table = {}
    columns = set()
    for line in lines:
        if line.strip() == "": continue
        dimensions = line.split(separator)
        row = table.get(dimensions[0], {})
        row[dimensions[1]] = dimensions[2].strip()
        table[dimensions[0]] = row
        columns.add(dimensions[1])
    return table, columns

if __name__=="__main__":
    print "Reads file where every line is in format: row-label[tab]col-label[tab]value and prints out table."
    fin = sys.stdin
    fout = sys.stdout

    table, columns = extract_table(fin.xreadlines())
    data_maketable.print_table(fout, table, columns)

