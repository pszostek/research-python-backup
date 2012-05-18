'''
Created on Nov 16, 2011

@author: mlukasik
'''
from __future__ import division

class LeaveOneOut(object):
    """
    Trains classifier on train_set, allows testing
    
    TODO: zrobic tak zeby nie musiec wczytywac calego generatora do samples!!
    
    """
    def __init__(self, classifier, samples, sample_classif_func):
        self.classifier = classifier
        self.samples = list(samples)
        self.sample_classif_func = sample_classif_func
    def test(self, iters, doprint=True): 
        import random
        correctness=0
        for i in range(iters):
            i = random.randint(0, len(self.samples)-1)
            if doprint:
                print "training classifier..."
            classif = self.classifier(self.samples[:i]+self.samples[i+1:])
            classif_ans = classif.classify(self.samples[i])
            if doprint:
                print i, "classified as:", classif_ans, "when it's:", self.sample_classif_func(self.samples[i])
            true_ans = set(self.sample_classif_func(self.samples[i]))
            correctness += len(set(classif_ans) & true_ans)/len(true_ans)
            #for i_1 in self.samples:
            #    if 1 in self.sample_classif_func(i_1):
            #        print "classified as:", classif.classify(i_1[0]), "when it's:", self.sample_classif_func(i_1)
                    
            
        return correctness / iters
        
class LeaveOneOutAllCategories(LeaveOneOut):
    """Trains classifier on train_set, allows testing"""
    def __init__(self, classifier, samples, sample_classif_func):
        """
        
        classifier - a classifier working on a sample from samples
        
        samples - iterable, where each element is a 2-element tuple:
            -first element is a numerical feature vector
            -second element is a list of labels
        
        """
        self.classifier = classifier
        self.samples = list(samples)
        self.sample_classif_func = sample_classif_func
        
class KFold(object):
    """Trains classifier on train_set, allows testing; maps tags into nums internally"""
    def __init__(self, classifier, samples, sample_classif_func, k):
        self.classifier = classifier
        self.samples = samples
        self.sample_classif_func = sample_classif_func
        self.k = k
    
    def test(self, doprint=True):
        correctness=0
        
        from sklearn import cross_validation
        kf = cross_validation.KFold(n=len(self.samples), k=self.k)
        
        for train_index, test_index in kf:
            #print "Another fold"
            #print train_index, test_index
            train_ind = [self.samples[i] for i in train_index]
            test_ind = [self.samples[i] for i in test_index]
            #build classifier:
            classif = self.classifier(train_ind)
            #test it:
            for tst_sample in test_ind:
                #print "I:", i
                classif_ans = classif.classify(tst_sample[0])
                #if doprint:
                    #print classif_ans, "when it's:", self.sample_classif_func(tst_sample)
                true_ans = set(self.sample_classif_func(tst_sample))
                correctness += len(set(classif_ans) & true_ans)/len(true_ans)
                #for i_1 in self.samples:
                #    if 1 in self.sample_classif_func(i_1):
                #        print "classified as:", classif.classify(i_1[0]), "when it's:", self.sample_classif_func(i_1)
        return correctness / len(self.samples)