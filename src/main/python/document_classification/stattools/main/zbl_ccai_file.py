"""Takes zbl-file and extracts file in format: every line = cc+\t\t+ai+\n """

if __name__ == "__main__":
    print "Takes zbl-file and extracts file in format: every line = cc+\"\\t\\t\"+ai+\"\\n"

    try:
        in_path = sys.argv[1]
    except:
        print "First argument expected: input-zbl-file-path"        
        sys.exit(-1)
    try:
        out_path = sys.argv[2]
    except:
        print "Second argument expected: output-file-path"        
        sys.exit(-1)      

    f = open(in_path,'r')
    fo = open(out_path, 'w')

    cc = ""
    ai = ""

    lines = f.readlines()
    for line in lines:
	    if len(line) < 2:
		    continue
	    field = line[0]+line[1]
	    if field == 'an' and len(cc)>0 and len(ai)>0:
		    fo.write(cc+"\t\t"+ai+"\n")
	    elif field == 'cc':
		    cc = line[3:(len(line)-1)]
	    elif field == 'ai':
		    ai = line[3:(len(line)-1)]
    fo.write(cc+"\t\t"+ai+"\n")

    f.close()
    fo.close()
