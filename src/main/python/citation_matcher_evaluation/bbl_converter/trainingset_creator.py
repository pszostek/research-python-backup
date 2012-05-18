import string
import re
from util import decode_utf, untexify, read_citations, format_ref
from functools import partial
from citationset import CitationSet

jpc_text = '''Onieva, L.; Lozano, S.; Larra\~{n}eta Astola, J.~C.; Ruiz~Usano, R. {\em
  Questiio} {\\bf 1987}, pages 117--133.'''

abbrv_text = '''B.~Abdellaoui, V.~Felli, and I.~Peral.
\\newblock A remark on perturbed elliptic equations of caffarelli-kohn-nirenberg
  type.
\\newblock {\\em Revista Matem\\'{a}tica Complutense}, pages 339--351, 2005.'''

acm_text = '''{\\sc Abascal~Fern\\'{a}ndez, E., and Landaluce~Calvo, M.~I.}
\\newblock An\\'{a}lisis factorial multiple como tecnica de estudio de la
  estabilidad de los resultados de un an\\'{a}lisis de componentes principales.
\\newblock {\\em Questiio\\/} (2002), 109--122.'''

alpha_text = '''Jose~A. Alvarez, Teresa Alvarez, and Manuel Gonz\\'{a}lez.
\\newblock Gap and perturbation of non-semi-fredholm operators.
\\newblock {\\em Extracta Mathematicae}, pages 139--141, 1989.'''

apalike_text = '''Abascal~Fern\\'{a}ndez, E., and Landaluce~Calvo, M.~I. (2002).
\\newblock An\\'{a}lisis factorial multiple como tecnica de estudio de la
  estabilidad de los resultados de un an\\'{a}lisis de componentes principales.
\\newblock {\\em Questiio}, pages 109--122.'''

ieeetr_text = '''B.~Rodriguez-Salinas, ``El teorema de radon-nikodym para las medidas con
  valores en un espacio localmente convexo.,'' {\\em Revista de la Real Academia
  de Ciencias Exactas Fisicas y Naturales}, 1980.'''

pccp_text = '''W.~P. Wiper, D.~Rios~Insua, and R.~Hierons, {\\em Revista de la Real Academia
  de Ciencias Exactas Fisicas y Naturales}, 1998, pp. 323--328.'''

plain_text = '''Boumediene Abdellaoui, Veronica Felli, and Ireneo Peral.
\\newblock A remark on perturbed elliptic equations of caffarelli-kohn-nirenberg
  type.
\\newblock {\\em Revista Matem\\'{a}tica Complutense}, pages 339--351, 2005.'''

ppcf_text = '''{\\sc Abascal~Fern\\'{a}ndez, E.} and {\\sc Landaluce~Calvo, M.~I.} (2002).
\\newblock {\\em Questiio} , 109--122.'''

revcompchem_text = '''L.~Onieva, S.~Lozano, J.~C. Larra\\~{n}eta Astola, and R.~Ruiz~Usano, {\\em
  Questiio}, pages 117--133 (1987). Metodo primal dual para modelos de
  planificacion con costes concavos y limitaciones de capacidad.'''

def flatten(list):
    return [item for sublist in list for item in sublist]

def parse(text, pattern, parsers):
    tags = {'title':'article-title'}
    text = ' '.join(text.split())
    regex = re.compile(pattern)
    m = regex.match(text)
    if m == None:
        print text
        pass
    groups = sorted([(m.start(k), m.end(k), k, v) for k,v in m.groupdict().items() if v != None],
                    lambda x, y: cmp(x[0], y[0]))
    result = []
    last = 0
    for s, e, n, v in groups:
        tagname = tags[n] if n in tags else n
        result.append(text[last:s] if last < s else '')
        result.append(parsers[n](v) if n in parsers else r'<%s>' % tagname + v.strip() + r'</%s>' % tagname)
        last = e
    result.append(text[last:])
    return ''.join(filter(lambda s: len(s) > 0, result))

def name_parser(s):
    abbrv_name = r'(((?<=\s)|\A)[A-Za-z]\.)'
    long_string = r'((?:\w|[-])(?:\w|[-])+)'

    def name_tokens(list):
        afretsplit = []
        hadAbbrv = any(map(lambda s: re.match(abbrv_name, s), list))
        hadLast = False
        for token in reversed(list):
            if re.match(abbrv_name, token, flags=re.UNICODE):
                afretsplit.append(('given-names', token))
            elif re.match(long_string, token, flags=re.UNICODE):
                if not hadLast or hadAbbrv:
                    hadLast = True
                    afretsplit.append(('surname', token))
                else:
                    afretsplit.append(('given-names', token))
            elif re.match(r'\A\s*\Z', token, flags=re.UNICODE):
                afretsplit.append(('whitespace', token))
            else:
                afretsplit.append(('other', token))
        afretsplit.reverse()
        return afretsplit

    def merge(named_tokens):
        merged = [named_tokens[0]]
        for tag, string in named_tokens[1:]:
            if tag == merged[-1][0]:
                merged[-1] = (tag, merged[-1][1] + string)
            else:
                merged.append((tag, string))
        
        
        return merged

    def supermerge(merged):
        supermerged = [merged[0]]
        i = 1
        while i < len(merged):
            if merged[i][0] == 'whitespace' and merged[i+1][0] == supermerged[-1][0]:
                supermerged[-1] = (merged[i+1][0], supermerged[-1][1] + 
                                                   merged[i][1] + merged[i+1][1])
                i += 2
            else:
                supermerged.append(merged[i])
                i += 1
        
        
        return supermerged

    def unify_surname(supermerged):
        renamed = []
        hadSurname = False
        for t, s in reversed(supermerged):
            if t == 'surname':
                if hadSurname:
                    renamed.append(('given-names', s))
                else:
                    hadSurname = True
                    renamed.append((t, s))
            else:
                renamed.append((t, s))
        renamed.reverse()
        return renamed

    def list2xml(renamed):
        result = []
        for t, s in renamed:
            if t in ['whitespace', 'other']:
                result.append(s)
            else:
                result.append('<%s>%s</%s>' % (t, s, t))
        
        
        return result

    s = untexify(decode_utf(s))
    list = filter(lambda s: len(s) > 0, 
                  flatten(map(lambda s: re.split(long_string, s, flags=re.UNICODE), 
                              re.split(abbrv_name, s, flags=re.UNICODE))))
    
    named_tokens = name_tokens(list)
    merged = merge(named_tokens)
    supermerged = supermerge(merged)
    renamed = unify_surname(supermerged)
    renamed = supermerge(renamed)
    result = list2xml(renamed)
    
    return ''.join(result)

def authors_parser(s, reseparator):
    decorate = lambda s: '<string-name>' + name_parser(s) + '</string-name>' if len(s.strip()) > 0 else ''
    cells = s.split(' and ')
    if len(cells) > 1:
        s0 = ', '.join(map(decorate, map(string.strip, re.split(reseparator, cells[0])))).strip()
        s1 = decorate(cells[1].strip())
        return s0 + ' and ' + s1
    else:
        return decorate(cells[0].strip())

authors_parser_comma = partial(authors_parser, reseparator=r',')
authors_parser_dotcomma = partial(authors_parser, reseparator=r'(?<=\.),')
authors_parser_bracketcomma = partial(authors_parser, reseparator=r'(?<=\}),')

def parse_abbrv(text):
    return parse(text, r'(?P<authors>.+?). \\newblock (?P<title>.+?) \\newblock \{\\em (?P<source>.+?)\}(?:, pages (?P<fpage>.+?)--(?P<lpage>.+?))?, (?P<year>.+?)\.', {'authors': authors_parser_comma})

def parse_acm(text):
    return parse(text, r'\{\\sc (?P<authors>.+?)\}\.? \\newblock (?P<title>.+?) \\newblock \{\\em (?P<source>.+?)\\/\} \((?P<year>.+?)\)(?:, (?P<fpage>.+?)--(?P<lpage>.+?))?\.', {'authors': authors_parser_dotcomma})

def parse_alpha(text):
    return parse(text, r'(?P<authors>.+?)\. \\newblock (?P<title>.+?) \\newblock \{\\em (?P<source>.+?)\}(?:, pages (?P<fpage>.+?)--(?P<lpage>.+?))?, (?P<year>.+?)\.', {'authors': authors_parser_comma})

def parse_apalike(text):
    return parse(text, r'(?P<authors>.+?) \((?P<year>.+?)\)\. \\newblock (?P<title>.+?) \\newblock \{\\em (?P<source>.+?)\}(?:, pages (?P<fpage>.+?)--(?P<lpage>.+?))?\.', {'authors': authors_parser_dotcomma})

def parse_ieeetr(text):
    return parse(text, r'(?P<authors>.+?), ``(?P<title>.+?),\'\' \{\\em (?P<source>.+?)\}(?:, pp.~(?P<fpage>.+?)--(?P<lpage>.+?))?, (?P<year>.+?)\.', {'authors': authors_parser_comma})

def parse_jpc(text):
    def authors_parser(s):
        return '; '.join(map(lambda s: '<string-name>' + name_parser(s) + '</string-name>', s.split(';')))
    return parse(text, r'(?P<authors>.+?) \{\\em (?P<source>.+?)\} \{\\bf (?P<year>.+?)\}(?:, pages (?P<fpage>.+?)--(?P<lpage>.+?))?\.', {'authors': authors_parser})
    
def parse_pccp(text):
    return parse(text, r'(?P<authors>.+?), \{\\em (?P<source>.+?)\}, (?P<year>.+?)(?:, pp. (?P<fpage>.+?)--(?P<lpage>.+?))?\.', {'authors': authors_parser_comma})

def parse_plain(text):
    return parse(text, r'(?P<authors>.+?)\. \\newblock (?P<title>.+?) \\newblock \{\\em (?P<source>.+?)\}(?:, pages (?P<fpage>.+?)--(?P<lpage>.+?))?, (?P<year>.+?)\.', {'authors': authors_parser_comma})

def parse_ppcf(text):
    return parse(text, r'(?P<authors>.+?) \((?P<year>.+?)\)\. \\newblock \{\\em (?P<source>.+?)\} (?:, (?P<fpage>.+?)--(?P<lpage>.+?))?\.', {'authors': authors_parser_bracketcomma})

def parse_revcompchem(text):
    return parse(text, r'(?P<authors>.+?), \{\\em (?P<source>.+?)\}(?:, pages (?P<fpage>.+?)--(?P<lpage>.+?))? \((?P<year>.+?)\)\. (?P<title>.+)', {'authors': authors_parser_comma})

def get_mixed_citations(filename, parsing_fun):
    for (no,ref,val) in read_citations(filename):
        yield (no, format_ref(ref) + untexify(parsing_fun(decode_utf(val)))) 

indir = r'C:\Users\matfed\Desktop\training\bbls\\'

files = [(r'abbrv.bbl', parse_abbrv),
         (r'acm.bbl', parse_acm),
         (r'alpha.bbl', parse_alpha),
         (r'apalike.bbl', parse_apalike),
         (r'ieeetr.bbl', parse_ieeetr),
         (r'jpc.bbl', parse_jpc),
         (r'pccp.bbl', parse_pccp),
         (r'plain.bbl', parse_plain),
         (r'ppcf.bbl', parse_ppcf),
         (r'revcompchem.bbl', parse_revcompchem)]

set = CitationSet()
for i, (filename, parsing_fun) in enumerate(files, 1):
    for k, v in get_mixed_citations(indir + filename, parsing_fun):
        set.add(str(int(k) + i * 10000), v)
set.write_nlm(r'C:\Users\matfed\Desktop\training.xml')
pass