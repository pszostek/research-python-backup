"""Splits single ZBL file into several files."""
import zbl_io
import sys

if __name__ == "__main__":
    print "The program splits single ZBL file into several files of required size."
    
    try:
        in_path = sys.argv[1]
    except:
        print "First argument expected: source-file"        
        sys.exit(-1)
    try:
        part_size = int(sys.argv[2])
    except:
        print "Second argument expected: number of records per output file"        
        sys.exit(-1)        
        
    print "Source file:", in_path
    print "Records per file:", part_size
        
    part_counter = 0;        
    part_records_counter = 0
    fout = open(in_path+".part"+str(part_counter), "w")
    for record in zbl_io.read_zbl_records( open(in_path, "r") ):
        part_records_counter = part_records_counter + 1
        if part_records_counter >= part_size:
            print part_records_counter,"records stored to file", fout
            part_counter = part_counter + 1
            part_records_counter = 0            
            fout = open(in_path+".part"+str(part_counter), "w")
        zbl_io.write_zbl_record(fout, record)
        fout.write("\n")
    print part_records_counter,"records stored to file", fout
    