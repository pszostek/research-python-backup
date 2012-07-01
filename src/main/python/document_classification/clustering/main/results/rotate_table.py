
import sys

if __name__=="__main__":
    print "The program rotates table read from file."
    try:
        src = sys.argv[1]
    except:
        print "Argument expected: the file that contain a table (columns separated with [tab] and rows with [newline])."
        sys.exit(-1)

    lines = open(src).readlines()
    tab = list(line.strip().split("\t") for line in lines if line.strip()!="")
    R = len(tab)
    C = len(tab[0])
    rtab = list( list( tab[r][c] for r in xrange(R) ) for c in xrange(C) ) #rotated

    fout = sys.stdout
    for row in rtab:
        for e in row:
            fout.write(e+"\t")
        fout.write("\n")

