"""Processing of XML files where every tag is in a single line."""

import re

def remove_xml_tags(text):    
    """Filters out xml tags from text.
    
    Sample use:
    >>> remove_xml_tags('<def>Jesli <hi rend="bold">lubisz</hi> koty?</def>')
    'Jesli lubisz koty?'
    """
    parts = text.split('<')
    parts[0] = '>'+parts[0]
    return reduce(lambda p1,p2: p1+p2, (p.split('>')[1] for p in parts) )
    

def extract_tag_attr(line, attrname):
    """Extracts attribute value from xml tag.
    
    Sample use:
    >>> extract_tag_attr('<cit type="dicteg">', 'type')
    'dicteg'
    """
    pattern = re.compile(attrname+'=\\".*\\"')
    line = pattern.findall(line)[0]    
    value_begin = line.find('"')+1
    value_end = line.find('"', value_begin)
    return line[value_begin: value_end]

def extract_tag_attr_q(line, attrname): 
    """Faster version of extract_tag_attr.
    
    Sample use:
    >>> extract_tag_attr_q('<cit type="dicteg">', 'type')
    'dicteg'
    """
    value_begin = line.find('"', line.find(attrname+"="))+1
    value_end = line.find('"', value_begin)
    return line[value_begin: value_end]

def extract_tag_value(line, tagname):
    """Extracts value from xml tag.
    
    Sample use:
    >>> extract_tag_value('<def><hi rend="bold">Panstwo</hi> to chlebodawcy w stosunku do sluzby.</def>', 'def')
    '<hi rend="bold">Panstwo</hi> to chlebodawcy w stosunku do sluzby.'
    """
    value_begin = line.find('>', line.find(tagname))+1
    value_end = line.find('</'+tagname, value_begin)
    return line[value_begin: value_end]

def find_tag_first_stronger(lines, tagname):
    """Returns line number where tag of tagname occurs first time.
    
    Sample use:
    >>> find_tag_first(['<entry>','<sense n="2" xml:id="raz.2">','<def>sytuacja, zdarzenie</def>','<sense n="1">','<def>Slowem <hi rend="bold">raz</hi> oznaczamy sytuacje...</def>'], 'sense')
    1
    """
    for i,line in enumerate(lines):
        if line.count('<'+tagname+' ') > 0:
            return i
    return -1

def find_tag_first(lines, tagname):
    """Returns line number where tag of tagname occurs first time.
    
    Sample use:
    >>> find_tag_first(['<entry>','<sense n="2" xml:id="raz.2">','<def>sytuacja, zdarzenie</def>','<sense n="1">','<def>Slowem <hi rend="bold">raz</hi> oznaczamy sytuacje...</def>'], 'sense')
    1
    """
    for i,line in enumerate(lines):
        if line.count(tagname) > 0:
            return i
    return -1

def find_tag_last(lines, tagname):
    """Returns line number where tag of tagname occurs last time.
    
    Sample use:
    >>> find_tag_last(['<entry>','<sense n="2" xml:id="raz.2">','<def>sytuacja, zdarzenie</def>','<sense n="1">','<def>Slowem <hi rend="bold">raz</hi> oznaczamy sytuacje...</def>','</sense>','</sense>','</entry>'], '/sense')
    6
    """
    lines = list(lines)    
    return len(lines)-find_tag_first(reversed(lines), tagname)-1

def extract_section_borders(lines, tagname, firstline = 0):  
    """Returns pair (firstline, endline) of a first found xml section (...<tagname> ... </tagname>...).
    
    If you do not want to search from the first line, set firstline argument to some other value. 
    """  
    depth = 0
    first_line = -1
    for i in xrange(firstline, len(lines)):
        line = lines[i]
        if line.count('<'+tagname+' ') > 0 or line.count('<'+tagname+'>') > 0:
            if depth==0:
                first_line = i
            depth = depth + 1
        elif line.count('</'+tagname+' ') > 0 or line.count('</'+tagname+'>') > 0:
             depth = depth - 1 
             if depth==0:                 
                return (first_line, i+1)
    return (-1,-1)

def is_line_opened_tag(line, tagname):
    """
    Checks if the line is an opened tag.
    Sample use:
    >>> is_line_opened_tag('<aaa>', 'aaa')
    True
    >>> is_line_opened_tag('<aaa/>', 'aaa')
    False
    
    """
    return '<'+tagname in line and '/>' not in line

def get_tag_blocks(lines, tagname):
    """
    Returns a list of consecutive fields of specified tagnames found in lines.
    
    Sample use:
    >>> get_tag_blocks(['<entry>','<sense n="2" xml:id="raz.2">','<def>sytuacja, zdarzenie</def>','</sense>','<sense n="1">','<def>Slowem <hi rend="bold">raz</hi> oznaczamy sytuacje...</def>','</sense>'], 'sense')
    [['<sense n="2" xml:id="raz.2">', '<def>sytuacja, zdarzenie</def>', '</sense>'], ['<sense n="1">', '<def>Slowem <hi rend="bold">raz</hi> oznaczamy sytuacje...</def>', '</sense>']]
    """
    tag_list = []
    
    first_seg_srch = 0
    seg_ind = find_tag_first_stronger(lines[first_seg_srch:], tagname)
    while True:
        first_seg, second_seg = extract_section_borders(lines, tagname, seg_ind)
        tag_list.append(lines[first_seg:second_seg])
        
        first_seg_srch = second_seg
        seg_ind = find_tag_first_stronger(lines[first_seg_srch:], tagname)
        #if there is no segment found, break:
        if seg_ind == -1:
            break
        seg_ind += first_seg_srch#because we calculated with shifts
        if seg_ind > len(lines):
            break
    return tag_list

def get_closed_tag_blocks(lines, tagname):
    """
    Returns a list of consecutive fields of specified tagnames found in lines, 
    only the opening tags are considered.
    
    Sample use:
    >>> get_closed_tag_blocks(['<entry>','<sense n="2" xml:id="raz.2">','<def>sytuacja, zdarzenie</def>','</sense>','<sense n="1">','<def>Slowem <hi rend="bold">raz</hi> oznaczamy sytuacje...</def>','</sense>'], 'sense')
    ['<sense n="2" xml:id="raz.2">', '<sense n="1">']"""
    tag_list = []
    
    first_seg_srch = 0
    while True:
        seg_ind = find_tag_first_stronger(lines[first_seg_srch:], tagname)
        if seg_ind == -1:
            break
        
        tag_list.append(lines[seg_ind+first_seg_srch])
        first_seg_srch = seg_ind+first_seg_srch+1#because we calculated with shifts
        if first_seg_srch > len(lines):
            break
    return tag_list

if __name__ == "__main__":
    import doctest
    doctest.testmod()   