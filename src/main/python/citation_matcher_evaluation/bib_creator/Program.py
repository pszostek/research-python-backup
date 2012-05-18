import os
import sys
import glob
from BiblioEntry import BiblioEntry
from BiblioEntrySet import BiblioEntrySet

filename = r"C:\Users\ICM\Desktop\ELibM-probka\urn_math-thar.ujf-grenoble.fr_ELibM_1175.01006.xml"

indir = r"C:\Users\ICM\Desktop\training\best"
outdir = r'C:\Users\ICM\Desktop\training\auxes'

filenames = glob.glob(os.path.join(indir, "*.xml"))
entries = BiblioEntrySet(map(lambda f: BiblioEntry(f), filenames), outdir)

entries.createBib()
for style in ['alpha', 'abbrv', 'ieeetr', 'plain', 'apalike', 'acm', 'jpc', 'pccp', 'ppcf', 'revcompchem']:
    entries.createAux(style)