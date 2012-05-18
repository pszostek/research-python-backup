'''
Created on Mar 11, 2012

@author: mlukasik
'''
import unittest
from weightedrandomlabel_classifier import WeightedRandomLabelClassifier

class Test(unittest.TestCase):


    def testAll(self):
            import sys
            sys.path.append(r'../')
            from data_io.zbl_io import MULTIVAL_FIELD_SEPARATOR
            from data_io.zbl_record_generators import mc2lmc_tomka_blad
            
            lrecords = []
            lrecords.append({'ab': 0, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
            lrecords.append({'ab': 1, 'ut': "", "ti": "", "mc":"b"+MULTIVAL_FIELD_SEPARATOR+"d"})
            lrecords.append({'ab': 2, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"b"})
            lrecords.append({'ab': 3, 'ut': "", "ti": "", "mc":"e"+MULTIVAL_FIELD_SEPARATOR+"f"})
            lrecords.append({'ab': 4, 'ut': "", "ti": "", "mc":"a"})
            lrecords.append({'ab': 5, 'ut': "", "ti": "", "mc":"a"+MULTIVAL_FIELD_SEPARATOR+"g"+MULTIVAL_FIELD_SEPARATOR+"h"})
            lrecords.append({'ab': 6, 'ut': "", "ti": "", "mc":"g"})
            
            def frecords():
                for i in lrecords:
                    yield i
            
            get_labels_of_record = mc2lmc_tomka_blad
            classify_oracle = mc2lmc_tomka_blad
            wrc = WeightedRandomLabelClassifier(frecords, get_labels_of_record, classify_oracle)
            
            self.assertEqual(dict(wrc.label2count)['a'], 4)
            for lrec in lrecords:
                self.assertEqual(type(wrc.classify(lrec)), list)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testAll']
    unittest.main()