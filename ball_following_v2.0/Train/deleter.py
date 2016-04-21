import os
from glob import glob

try:
    for fl, fp in zip(glob("raw/*.png"),glob("raw/*.dat")):
        os.remove(fl)
        os.remove(fp)
except OSError, e:
    print ("Error: %s - %s." % (e.filename,e.strerror))
