'''
Created on Nov 3, 2011

@author: mlukasik

Convert fields of a record into friendly format. Filter records that contain all necessary data.
'''
import sys
sys.path.append(r'../') 
from tools import text2words

def extract_categs_msc(rec):
    if 'categories' not in rec:
        return None
    
    new_categs = []
    for categ in rec['categories']:
        categ_parsed = categ[0].replace("bwmeta1.category-class.", '')
        categ_parsed = categ_parsed.split(':')    
        if categ_parsed[0] == 'MSC':
            new_categs.append(text2words.text_to_words(categ_parsed[1]))
            
    return new_categs
    
def extract_canonical_authors(rec):
    new_contribs = []
    for contrib in rec['contributors']:
        for name in contrib:
            name_parsed = name.split(':')
            if name_parsed[0] == 'canonical':
                new_contribs.append(name_parsed[1])
                
    return new_contribs

def extract_journal_publisher(rec):
    journal = ''
    publisher = ''
    for hier in rec['hierarchy']:
        for info in hier:
            info_parsed = info.split(':')
            if info_parsed[0] == 'publisher':
                publisher = info_parsed[1]
            if info_parsed[0] == 'journal':
                journal = info_parsed[1]
    
    return journal, publisher

def extract_date_reg(rec):
    date_reg = ''
    for d in rec['date']:
        d_parsed = d[0].split(':')
        if d_parsed[0] == 'registration':
            date_reg = d_parsed[1]
            
    return date_reg

def extract_keywords(rec):
    #if 'kw' not in rec:
        #print "No keywords in rec:", rec
    #    return []
        #d_parsed = d[0].split(':')
        #if d_parsed[0] == 'registration':
        #    date_reg = d_parsed[1]
    #return reduce(lambda a, b: a+b, map(lambda x: text2words.text_to_words(x[0]), rec['kw']))
    return map(lambda x: text2words.text_to_words(x[0]), rec['kw'])

def filer_record(rec):
    """ filter only MSc categories and those with titles. """
    msc_categs = extract_categs_msc(rec)
    if msc_categs and len(rec['ti']) > 0 and 'descr' in rec and 'kw' in rec:
        return True
    return False

def process_record(rec):
    """ write converted fields into the rec """
    new_rec = {}
    if 'descr' in rec:
    	new_rec['descr'] = rec['descr'][0][0].replace("Abstract:", "")
    #else:
    	#new_rec['descr'] = ""
        #print "No descriprion in record:", rec
    
    new_rec['an'] = rec['an'][0][0]
    new_rec['ti'] = rec['ti'][0][0]
    new_categs = extract_categs_msc(rec)
    new_rec['categories'] = new_categs
    new_contribs = extract_canonical_authors(rec)
    new_rec['contributors'] = new_contribs
    journal, publisher = extract_journal_publisher(rec)
    new_rec['journal'] = journal
    new_rec['publisher'] = publisher
    date_reg = extract_date_reg(rec)
    new_rec['date_reg'] = date_reg
    keywords = extract_keywords(rec)
    new_rec['keywords'] = keywords
    
    return new_rec   
