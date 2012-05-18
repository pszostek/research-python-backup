
import random

def random_label(label2count):
    """Returns randomly selected label.
    
    label2count - dictionary {label:count} (used to estimate probabilities)
    """
    total = float(sum(label2count.values()))
    randval = random.random()
    pos = 1.0
    label2count_list = list(label2count.iteritems())
    for label,count in label2count_list:
        pos = pos - count/total
        if pos<=randval:
            return label        
    return label2count_list[0][1]
    

def random_multilabel(label2count, k, can_repeat = False):
    """Returns list of k randomly selected labels.
    
    label2count - dictionary {label:count} (used to estimate probabilities)
    can_repeat - if can_repeat == False then after label is selected is removed from (copy of) label2count
    """
    label2count = dict(label2count.iteritems()) #make copy
    labels = []
    for i in xrange(k):
        label = random_label(label2count)
        labels.append(label)
        if not can_repeat:
            label2count.pop(label)
    return labels
    
if __name__ == "__main__":
    label2count = {'a': 100, 'b': 200, 'c': 150, 'd': 250}
    total = sum(label2count.values())
    post_label2count = {}
    for i in xrange(total):
        label = random_label(label2count)
        post_label2count[label] = post_label2count.get(label,0)+1
    print "Pre label2count:", label2count
    print "Post label2count:", post_label2count 