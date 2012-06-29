import re
import codecs
import os

def decode_utf(s):
    s = s.replace(r"\'{E}",u'\u00c9')
    s = s.replace(r"\'{A}",u'\u00c1')
    s = s.replace(r"\'{a}",u'\u00e1')
    s = s.replace(r"\'{O}",u'\u00d3')
    s = s.replace(r'\"{O}',u'\u00d6')
    s = s.replace(r'\"{o}',u'\u00f6')
    s = s.replace(r'\~{n}',u'\u00f1')
    return s

    utf = re.compile(r'\\utf8{(\d+)}')
    last = 0
    result = []
    for m in utf.finditer(s):
        result.append(s[last:m.start()])
        last = m.end()
        result.append(unichr(int(m.group(1))))
    result.append(s[last:])   
    return "".join(result)

def untexify(s):
    mathin = re.compile(r'(^|[^\\])\\[\[\]]')
    while True:
        (s, n) = mathin.subn(r'\1 ', s)
        if n == 0: break

    brackets = re.compile(r'(^|[^\\])[{}\[\]]')
    while True:
        (s, n) = brackets.subn(r'\1', s)
        if n == 0: break

    commands = re.compile(r'(^|[^\\])\\\S+')
    while True:
        (s, n) = commands.subn(r'\1', s)
        if n == 0: break
    
    slashes = re.compile(r'(^|[^\\])\\')
    while True:
        (s, n) = slashes.subn(r'\1', s)
        if n == 0: break
    s = s.replace('\\\\', '\\')
    s = s.replace('~', ' ')
    return s

def read_citations(filename):
    testId = os.path.splitext(os.path.basename(filename))[0]
    file = codecs.open(filename, encoding='utf8')
    contents = file.read()
    file.close()
    begin = r'\begin{thebibliography}'
    end = r'\end{thebibliography}'
    bibitem = r'\bibitem'

    i = contents.find(bibitem, contents.index(begin))
    j = contents.rindex(end)

    items = contents[i:j].split(bibitem)[1:]

    citations = []

    for it in items:
        i = it.find('[')
        j = it.find(']')
        k = it.find('{')
        l = it.find('}')
        ref = ""
        if -1 < i and i < j and i < k:
            ref = it[i + 1:j]
            k = it.find('{', j)
            l = it.find('}', j)
        key = it[k + 1:l]
        value = " ".join(it[l + 1:].split())
        citations.append((key, ref, value))
    return citations

def format_ref(ref):
    return '[' + untexify(decode_utf(ref)).strip() + '] ' if len(ref) > 0 else ''

