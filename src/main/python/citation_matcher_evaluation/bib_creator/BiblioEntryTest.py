import unittest
from unittest import TestSuite
from BiblioEntry import combineAuthors

class BiblioEntryTest(unittest.TestCase):
    def test_combineAuthors(self):
        self.assertEqual(combineAuthors(["1","2","3"]), "1 and 2 and 3")
        self.assertEqual(combineAuthors(["1","2"]), "1 and 2")
        self.assertEqual(combineAuthors(["1"]), "1")
        self.assertEqual(combineAuthors([]), "")

if __name__ == '__main__':    
     unittest.main()