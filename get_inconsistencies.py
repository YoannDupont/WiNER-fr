#-*- coding: utf-8 -*-

import os
import sys
import codecs

from sem.storage import Document, Annotation
from sem.exporters import BratExporter

def main(indirnames, outfilename, default_shift=0):
    dirs = []
    for indirname in indirnames:
        dirs.extend([os.path.join(indirname, name) for name in sorted(os.listdir(indirname)) if os.path.isdir(os.path.join(indirname, name))])
    
    lower2tag = {}
    for dirname in dirs:
        names = [f for f in os.listdir(dirname) if f.endswith(".ann")]
        for name in names:
            filename = os.path.abspath(os.path.join(dirname, name))
            for line in codecs.open(filename, "rU", "utf-8"):
                parts = line.strip().split(u"\t")
                if parts != []:
                    tag = parts[1].split()[0]
                    low = parts[-1].lower()
                    if low not in lower2tag:
                        lower2tag[low] = {}
                    if tag not in lower2tag[low]:
                        lower2tag[low][tag] = set()
                    lower2tag[low][tag].add(filename)
    with codecs.open(outfilename, "w", "utf-8") as O:
        O.write(u"%s\t%s\t%s\n" %("text (lower)", "tag", "filename"))
        for low, tags in lower2tag.items():
            if len(tags) > 1:
                for tag in tags:
                    for filename in sorted(tags[tag]):
                        O.write(u"%s\t%s\t%s\n" %(low, tag, filename))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser("Concatenate the BRAT files of a list of directories. For each directory, BRAT files will be searched in all of its subdirectories.")
    parser.add_argument("indirnames", nargs="+",
                        help="the input directories")
    parser.add_argument("outfilename",
                        help="the output file name")
    
    args = parser.parse_args()
    main(args.indirnames, args.outfilename)
    sys.exit(0)
