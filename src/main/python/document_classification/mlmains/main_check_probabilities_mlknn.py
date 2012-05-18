'''
Created on Mar 5, 2012

@author: mlukasik
'''
def PRINTER(x):
    print x

def inspect_counts(counts):
    '''
    Print counts of each number of occurences of each class in the neighbourhood.
    '''
    for code, value in counts.iteritems():
        PRINTER('[inspect_counts]: code: '+str(code))
        for no, cnts in value.iteritems():
            PRINTER('[inspect_counts]: no: '+str(no))
            PRINTER('[inspect_counts]: count of them: '+str(cnts))
        PRINTER('[inspect_counts]:-------------------------')

def compare_counts(c, c_prim):
    '''
    Compare the counts, for each code and each number of neighbours
    print consecutive counts in c and c_prim. 
    '''
    for code, value in c.iteritems():
        PRINTER('[inspect_counts]: code: '+str(code))
        for no, cnts in value.iteritems():
            PRINTER('[inspect_counts]: no: '+str(no))
            PRINTER('[inspect_counts]: c, c_prim: '+str(cnts)+" "+str(c_prim[code][no]))
        PRINTER('[inspect_counts]:-------------------------')      

if __name__ == '__main__':
    import sys
    try:
        load_classifier_path = sys.argv[1]
    except:
        print 'Argument expected: path to a classifier'
        sys.exit(1)
    #PRINTER("Input arguments:")
    #PRINTER("load_classifier_path: "+str(load_classifier_path))
        
    sys.path.append(r'../')
    from tools.pickle_tools import read_pickle
    classifier = read_pickle(load_classifier_path)
    
    #print "Finding out about the counts c and c_prim
    #PRINTER("-----------C-----------")
    #inspect_counts(classifier.c)
    #PRINTER("-----------C_PRIM-----------")
    #inspect_counts(classifier.c_prim)
    
    PRINTER("-----------COMPARE COUNTS-----------")
    compare_counts(classifier.c, classifier.c_prim)