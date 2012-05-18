'''
Created on Nov 14, 2011

@author: mlukasik
'''
#SVM:
from sklearn import svm
import numpy as np
from categs2numeric import get_categs_dict

class SvmWordsClassifier(object):
    """Classify using multi-label svm. 
    """
    def __init__(self, frecords):
        """
        """
        self.clfs = {}
        categ2recs = get_categs_dict(frecords)
        print "num of SVMs to be constructed:", len(categ2recs)
        i=0
        for categ in categ2recs.iterkeys():
            i+=1
            print i
            clf = svm.SVC() 
            X = np.array(map(lambda x: x[0], frecords))
            Y = np.array(map(lambda x: categ in x[1], frecords))
            clf.fit(X, Y)
            self.clfs[categ] = clf
            #if i==2:
            #    break
    
    def classify(self, sample, closest=3):
        #this doesn't seem to be a good way, because no classifier returns True:
        return filter(lambda x: self.clfs[x].predict(sample), self.clfs.iterkeys())
        
        """#instead, let's use probabilistic estimation:
        probas = [(self.clfs[k].predict_proba(sample).tolist(), k) for k in self.clfs.iterkeys()]
        print probas
        if closest < math.log(len(probas)):
            selected = []
            while len(selected)<closest:
                curr_sel = -1
                curr_val = -sys.maxint - 1
                for i in range(len(probas)):
                    print 
                    if curr_val<probas[i][0] and i not in selected:
                        curr_sel = i
                        curr_val = probas[i][0]
                selected.append(curr_sel)
            return selected
        else:
            probas.sort(cmp=None, key=lambda x: x[0], reverse=True)
            return [x[1] for x in probas[:closest]]
        """
        
class SvmSingleTagWordsClassifier(object):
    """
    Classify using single-label svm. 
    
    This is adjustment of SVM to the needs of topic_classification package.
    """
    def __init__(self, frecords, label):
        """
        
        frecords - iterable, where each element is a 2-element tuple:
            -first element is a numerical feature vector
            -second element is a list of labels
        
        label - the label which is to be amongst the labels in second element of each of the records. Afterall it is a binary classifier.
        """
        self.label = label
        self.clf = svm.SVC() 
        X = np.array(map(lambda x: x[0], frecords))
        Y = np.array(map(lambda x: label in x[1], frecords))
        self.clf.fit(X, Y)
        
    def classify(self, sample):
        """Sample is a feature vector
        """
        return self.clf.predict(sample)
    