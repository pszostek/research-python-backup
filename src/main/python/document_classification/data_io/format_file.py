"""Takes file and fixes formatting line by line."""

import re
import sys, os

#patterns to be filtered {pattern:replace_string}:
INVALID_PATTERNS = { '\s*\\\\n\s*\\\\n\s*': '', '\\\\n':'', '\s\s+\s':' '}

def compile_patterns(patterns):
    """Takes list of strings (=patterns) and returns list of regexp objects."""
    regexps = []
    for pattern in patterns:
        regexps.append(re.compile(pattern))
    return regexps

def filter_patterns(str, regexps, replace_strings):
    """Filters in str (replaces with replace_strings) all substrings 
    that matches any of patterns from list of regexps.
    
    Sample use:
    >>> filter_patterns('lubieAxBciastkaAxyCiAyBcole', [re.compile('A.B'), re.compile('A..C')], ['',''] )
    'lubieciastkaicole'
    >>> filter_patterns('aaAxByCbb', [re.compile('A.B'), re.compile('B.C')], ['',''] )
    'aayCbb'
    >>> filter_patterns('aaAxBByCbb', [re.compile('A.B'), re.compile('B.C')], ['',''] )
    'aabb'
    >>> filter_patterns('aaAxBByCbb', [re.compile('A.B'), re.compile('B.C')], ['X','Y'] )
    'aaXYbb'
    >>> filter_patterns("aa \\n   \\n bb", [re.compile('\\n\\s*\\n')], [''] )
    'aa  bb'
    """
    while True:
        matches = []
        total_matches = 0
        for regexp in regexps:
            regexp_matches = regexp.findall(str)            
            matches.append( regexp_matches )
            total_matches = total_matches + len(regexp_matches)
            
        if total_matches == 0:
            break
        
        for (regexp_matches, replace_string) in zip(matches, replace_strings):
            for match in regexp_matches:
                str = str.replace(match, replace_string)
    return str
                    

if __name__ == "__main__":
    print "Program takes file and line by line fixes formatting according to rules."

    import doctest
    doctest.testmod()       
    
    try:
        in_path = sys.argv[1]
    except:
        print "First argument expected: source-file"        
        sys.exit(-1)
    try:
        out_path = sys.argv[2]
    except:
        print "Second argument expected: output-file"        
        sys.exit(-1)
    print "in_path =", in_path
    print "out_path =", out_path
        
    invalid_regexps = compile_patterns(INVALID_PATTERNS.keys())
        
    fin = open(in_path, 'r')        
    fout = open(out_path, 'w')
    for line in fin.xreadlines():
        line = filter_patterns(line, invalid_regexps, INVALID_PATTERNS.values())
        fout.write(line)
    fin.close()
    fout.close()
