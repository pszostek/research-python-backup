import os
import codecs

class BiblioEntrySet(object):
    def __init__(self, entries, out):
        self.bibfile = 'biblio'
        self.abspath = out
        self.entries = entries

    def createBib(self):
        with codecs.open(os.path.join(self.abspath, self.bibfile + '.bib'), 'w', encoding="utf8") as out:
            for e in self.entries:
                out.write(e.getBibitemString() + "\r\n")

    def createAux(self, style):
        with codecs.open(os.path.join(self.abspath, style + '.aux'), 'w', encoding="utf8") as out:
            out.write("\\relax\r\n")
            for e in self.entries:
                out.write(e.getCitationString() + "\r\n")
            out.write("\\bibstyle{%s}\r\n" % style)
            out.write("\\bibdata{%s}\r\n" % self.bibfile)