'''
Created on Nov 23, 2011

@author: mlukasik
'''
from sklearn import tree
import numpy as np

class TreeSingleTagWordsClassifier(object):
    """Classify using a decision tree. 
    """
    def __init__(self, label, frecords, featurenames, picture_name = "treepicture.dot"):
        """
        """
        self.label = label
        self.clf = tree.DecisionTreeClassifier() 
        self.featurenames = featurenames
        
        X = np.array(map(lambda x: x[0], frecords))
        Y = np.array(map(lambda x: int(label in x[1]), frecords))
        self.clf.fit(X, Y)
        
        #comment this out if you don't want to print the tree
        out = open(picture_name, 'w')
        print featurenames
        out = tree.export_graphviz(self.clf, out_file=out, feature_names=featurenames)
        out.close()
    
    def classify(self, sample):
        #this doesn't seem to be a good way, because no classifier returns True:
        return self.clf.predict(sample)
