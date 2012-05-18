'''
Created on Dec 29, 2011

@author: mlukasik
'''
import unittest
import sys
sys.path.append(r'../')
from randomly_divide import randomly_divide

class Test(unittest.TestCase):


    def test(self):
        test, train = randomly_divide(10, 3)
        self.assertEqual(len(set(test)), 7)
        self.assertEqual(len(set(train)), 3)
        self.assertEqual(len(set(test)|set(train)), 10)
        self.assertEqual(len(set(test)|set(train)), 10)
        self.assertEqual(max(list(set(test)|set(train))), 9)
        self.assertEqual(min(list(set(test)|set(train))), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()