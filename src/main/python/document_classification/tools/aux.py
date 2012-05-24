

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
