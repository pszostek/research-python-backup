'''
Created on Dec 29, 2011

@author: mlukasik
'''
import unittest
from zbl_record_generators import gen_record_prefixed, gen_record_fromshifts, gen_record_filteredbylabels

class Test(unittest.TestCase):

    def testGenRecordPrefixed(self):    
        def gen_record():
            for i in xrange(10, 20):
                yield {'mc': '\t;\t'.join(str(i)+str(i+1) for i in xrange(i))} 
                
        self.assertEqual(list(gen_record_prefixed(gen_record, 2)), [{'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11\t;\t12'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11\t;\t12\t;\t13'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11\t;\t12\t;\t13\t;\t14'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11\t;\t12\t;\t13\t;\t14\t;\t15'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11\t;\t12\t;\t13\t;\t14\t;\t15\t;\t16'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11\t;\t12\t;\t13\t;\t14\t;\t15\t;\t16\t;\t17'},
                                                    {'mc': '01\t;\t12\t;\t23\t;\t34\t;\t45\t;\t56\t;\t67\t;\t78\t;\t89\t;\t91\t;\t10\t;\t11\t;\t12\t;\t13\t;\t14\t;\t15\t;\t16\t;\t17\t;\t18'}])


    def testGenRecordFromshifts(self):
        def gen_record():
            for i in xrange(20):
                yield i 
                
        self.assertEqual(list(gen_record_fromshifts(gen_record, [0, 5, 8, 10, 12, 17, 19])), [0, 5, 8, 10, 12, 17, 19])

    def testGenRecordFilteredbylabels(self):
        def gen_record():
            for i in xrange(1, 10):
                yield {'mc': '\t;\t'.join([str(i), str(i+1)])}
        
        self.assertEqual(list(gen_record_filteredbylabels(gen_record, set([str(1), str(5)]))), [{'mc': str(1)}, {'mc': str(5)}, {'mc': str(5)}])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()