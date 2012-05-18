import os
from xml.etree.ElementTree import ElementTree

def isAscii(c):
    return ord(c) < 128

def encodeUtf(s):
    s = s.replace(u'\u00c9',r"\'{E}")
    s = s.replace(u'\u00c1',r"\'{A}")
    s = s.replace(u'\u00e1',r"\'{a}")
    s = s.replace(u'\u00d3',r"\'{O}")
    s = s.replace(u'\u00d6',r'\"{O}')
    s = s.replace(u'\u00f6',r'\"{o}')
    s = s.replace(u'\u00f1',r'\~{n}')
    return s
    #return "".join(map(lambda c: c if isAscii(c) else r'\utf8{%i}' % ord(c), s))

def getMixedText(elem):
    result = elem.text if elem.text != None else ""
    for c in elem.getchildren():
        result += getMixedText(c)
        result += c.tail if c.tail != None else ""
    return result

def safeGetText(elem, xpath):
    e = elem.findall(xpath)
    if e != None and len(e) > 0:
        return getMixedText(e[0])
    else:
        return ""

def safeGetTextSequence(elem, xpath):
    found = elem.findall(xpath)
    if found != None:
        return map(lambda x: getMixedText(x), found)
    else:
        return []

def extractAuthorName(elem):
    es = elem.findall('string-name')
    if len(es) > 0:
        return es[0].text
    es = elem.findall('name')
    if len(es) > 0:
        e = es[0]
        suf = safeGetText(e, 'suffix')
        suffix = ", " + suf if suf != "" else ""
        surname = safeGetText(e, 'surname').strip().rstrip(',')
        given = safeGetText(e, 'given-names').strip().rstrip(',')
        givennames = ", " + given if given != "" else ""
        return surname + suffix + givennames
    return ""

def combineAuthors(authors):
    return " and ".join(filter(lambda x: x != None and x != "", authors))

def escapeLatex(text):
    special = '\\[]{}$'
    for s in special:
        text = text.replace(s, '\\' + s)
    return text

class BiblioEntry(object):
    def __init__(self, filename):
        self.id = os.path.splitext(os.path.basename(filename))[0]
        tree = ElementTree(file=filename)
        elem = tree.getroot()
        self.meta = {}
        self.meta['author'] = combineAuthors(
                map(extractAuthorName, elem.findall("./front/article-meta/contrib-group/contrib[@contrib-type='author']")))
        self.meta['title'] = safeGetText(elem, "./front/article-meta/title-group/article-title")
        self.meta['journal'] = safeGetText(elem, "./front/journal-meta/journal-title-group/journal-title")
        self.meta['volume'] = safeGetText(elem, "./front/article-meta/pub-date/volume")
        self.meta['year'] = safeGetText(elem, "./front/article-meta/pub-date/year")
        fpage = safeGetText(elem, "./front/article-meta/fpage")
        lpage = safeGetText(elem, "./front/article-meta/lpage")
        if fpage != "" and lpage != "":
            self.meta['pages'] = fpage + "--" + lpage

    def getCitationString(self):
        return r"\citation{%s}" % (self.id)

    def getBibitemString(self):
        return "@article{%s,\r\n%s\r\n}" % (
            self.id, 
            ",\r\n".join(map(
                lambda (k,v): k + " = {" + encodeUtf(escapeLatex(v)) + "}" , 
                filter(lambda (k,v): len(v) > 0,self.meta.items()))))
