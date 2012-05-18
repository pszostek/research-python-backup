'''
Created on Nov 17, 2011

@author: mlukasik

Store records object to a specified file.
'''
import pickle
    
def store_py_records(records, oname):
    print "storing pckl"
    with open(oname, 'w') as out:
        pickle.dump(records, out)

def store_txt_records(records, oname):
    print "storing txt"
    with open(oname, 'w') as out:
        for rec in records:
            out.write("===RECORD===\n")
            for k, v in rec.iteritems():
                out.write(k+": "+str(v)+"\n")