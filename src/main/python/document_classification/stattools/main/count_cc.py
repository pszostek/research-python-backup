"""Counts occurrences of code categories in zbl files."""
#Zlicza wystepowanie kategorii w danych ZBL.

import zbl_io, io
import sys, os

def filter_XXY_categories(ccs):
    """Removes illegal cc values."""
    return [cc for cc in ccs if not (cc.endswith('XX') or cc.endswith('xx')) ]

def filter_no_categories(ccs):
    """Empty filtering of cc categories."""
    return ccs

def count_categories(src, filter_categories = filter_no_categories):
    """Takes stream/generator of ZBL records and counts categories occurrence (returns dictionary{category name: its count})."""
    count = {}
    for record in src:
        if not record.has_key('cc'):
            #print "[WARN] Skipping record:",record
            continue
        ccstr   = record['cc'].strip().replace('*', '')
        ccs     = filter_categories( cc.strip() for cc in ccstr.split(' ') )
        for cc in ccs:
            if count.has_key(cc):
                count[cc] = count[cc] + 1
            else:
                count[cc] = 1
    return count

if __name__ == "__main__":

    args = sys.argv
    if len(sys.argv) != 3:
        print "[ERROR] Exactly two arguments are expected: input-zbl-file-path output-count-path-prefix"
        exit(-1)
    zblInPath       = args[1]
    statsOutPath    = args[2]


    #zliczenie
    zbl_src = zbl_io.read_zbl_records(open(zblInPath))
    count = count_categories(zbl_src, filter_XXY_categories)

    #zapis do pliku
    #f = open(statsOutPath, "w")
    #for cc in count:
    #    f.write(cc+" "+str(count[cc])+"\n")
    #f.close()
    io.fwrite_vector(statsOutPath+"_labels.svector", count.keys())
    io.fwrite_vector(statsOutPath+"_count.ivector", count.values())

