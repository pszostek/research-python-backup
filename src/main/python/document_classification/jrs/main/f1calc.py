import sys


if __name__ == "__main__":
    #"F1-calculator"
    
    try:        
        TN = int(sys.argv[1]) 
        FP = int(sys.argv[2])
        FN = int(sys.argv[3])
        TP = int(sys.argv[4])
    except:
        print "four arguments expected: TN, FP, FN, TP"
        sys.exit(-1)
        
        

    try:
        precision   = float(TP) / (TP+FP)
    except:
        precision   = 0.0
    try:
        recall      = float(TP) / (TP+FN)
    except:
        precision   = 0.0
    try:
        f1          = 2.0*precision*recall / (precision+recall)
    except:
        f1          = 0.0
        
    print "f1=",f1
    print "prec=",precision
    print "recall=",recall
