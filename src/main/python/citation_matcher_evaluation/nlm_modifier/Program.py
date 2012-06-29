import os
import glob
from xml.etree.ElementTree import ElementTree

def process_file(filename):
    id = os.path.splitext(os.path.basename(filename))[0]
    tree = ElementTree(file=filename)
    elem = tree.find('./front/article-meta/article-id')
    elem.text = id
    tree.write(filename)

indir = r"C:\Users\matfed\Desktop\training\todb"

for f in glob.glob(os.path.join(indir, "*.xml")):
    process_file(f)
