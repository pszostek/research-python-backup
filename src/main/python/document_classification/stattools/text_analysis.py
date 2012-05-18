"""Different analysis on strings."""

import math

def lev(s1, s2):
    """Downloaded from:
    http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python"""
    if len(s1) < len(s2):
        return lev(s2, s1)
    if not s1:
        return len(s2)
 
    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]



def build_word_histogram(word):
    """Returns dictionary {letter:number of occurrences} built for a word."""
    hist = {}
    for letter in word:
        hist[letter] = hist.get(letter, 0) + 1
    return hist

def word_histograms_diff_total(hist1, hist2):
    """Calculates total sum of differences between two histograms (dictionaries {element: count})"""
    total = sum(math.fabs(hist1.get(key)-hist2.get(key, 0)) for key in hist1)
    total = total + sum(hist2.get(key) for key in hist2 if not hist1.has_key(key)) 
    return int(total)
        
def word_hist_diff_total(word1, word2):
    """See: build_word_histogram and word_histograms_diff_total"""
    hist1 = build_word_histogram(word1)    
    hist2 = build_word_histogram(word2)
    return word_histograms_diff_total(hist1, hist2)
        