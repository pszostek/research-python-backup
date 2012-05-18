import re
import os
import glob
from citationset import CitationSet
from util import decode_utf, untexify, read_citations, format_ref

def process_file(filename, outdir):
    citations = CitationSet()
    for (key, ref, val) in read_citations(filename):
        citations.add(key, format_ref(ref) + untexify(decode_utf(val)))

    testId = os.path.splitext(os.path.basename(filename))[0]
    citations.write_mapfile(os.path.join(outdir, '%s_map.txt' % testId))
    citations.write_nlm(os.path.join(outdir, '%s.xml' % testId))
    citations.write_txt(os.path.join(outdir, '%s.txt' % testId))

outdir = r'C:\Users\matfed\Desktop\test-sets'
indir = r'C:\Users\matfed\Desktop\bbls'
filenames = glob.glob(os.path.join(indir, "*.bbl"))
for f in filenames:
    process_file(f, outdir)
