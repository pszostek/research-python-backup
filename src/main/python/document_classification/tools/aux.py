

import hashlib
import os
from os import path

def quick_md5(text):
    """Returns MD5 hash of given text."""
    m = hashlib.md5()
    m.update(text)    
    return m.digest()

def exists(path):
    """Returns True iff path points out existing object."""
    return os.path.exists(path)

def extract_keys(list_of_dictionaries):
    """Returns set of all keys found in list of dictionaries."""
    all_keys = set()
    for d in list_of_dictionaries:
        all_keys.update(d.keys())
    return all_keys

def extract_values(list_of_dictionaries, key):    
    """Returns list of all values found in list of dictionaries for given key."""
    return list(d[key] for d in list_of_dictionaries if key in d)