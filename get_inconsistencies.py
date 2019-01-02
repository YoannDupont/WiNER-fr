#-*- coding: utf-8 -*-

import os
import sys
import codecs

def main(indirnames, outfilename, default_shift=0):
    dirs = []
    for indirname in indirnames:
        dirs.extend([os.path.join(indirname, name) for name in sorted(os.listdir(indirname)) if os.path.isdir(os.path.join(indirname, name))])
    
    lower2tag = {}
    lower2offset = {}
    tag2lower = {}
    contents = {}
    for dirname in dirs:
        names = [f for f in os.listdir(dirname) if f.endswith(".ann")]
        for name in names:
            content_name = os.path.abspath(os.path.join(dirname, name[:-3]+"txt"))
            contents[content_name] = codecs.open(content_name, "rU", "utf-8").read()
            filename = os.path.abspath(os.path.join(dirname, name))
            for line in codecs.open(filename, "rU", "utf-8"):
                parts = line.strip().split(u"\t")
                if parts != []:
                    tag = parts[1].split()[0]
                    low = parts[-1].lower()
                    subparts = parts[1].split()
                    lo = int(subparts[1])
                    hi = int(subparts[-1])
                    if low not in lower2tag:
                        lower2tag[low] = {}
                    if tag not in lower2tag[low]:
                        lower2tag[low][tag] = set()
                    lower2tag[low][tag].add(filename)
                    if low not in lower2offset:
                        lower2offset[low] = []
                    lower2offset[low].append([content_name, lo, hi])
                    if tag not in tag2lower:
                        tag2lower[tag] = set()
                    tag2lower[tag].add(low)
    
    with codecs.open(outfilename, "w", "utf-8") as O:
        O.write(u"%s\t%s\t%s\n" %("text (lower)", "tag", "filename"))
        for low, tags in lower2tag.items():
            if len(tags) > 1:
                for tag in tags:
                    for filename in sorted(tags[tag]):
                        O.write(u"%s\t%s\t%s\n" %(low, tag, filename))
    
    with codecs.open(outfilename+"1", "w", "utf-8") as O:
        for tag, lowers in tag2lower.items():
            lows = sorted(lowers)
            for i in range(len(lows)):
                for j in range(i+1, len(lows)):
                    if lows[i].startswith(lows[j]):
                        for i_offset in lower2offsets[lows[i]]:
                            for j_offset in lower2offsets[lows[j]]:
                                i_content = contents[i_offset[0]][i_offset[1] : ].lower()
                                print i_content
                                if i_content.startswith(lows[j]):
                                    print lows[i], "//", lows[j]
                    elif lows[j].startswith(lows[i]):
                        for i_offset in lower2offset[lows[i]]:
                            for j_offset in lower2offset[lows[j]]:
                                i_content = contents[i_offset[0]][i_offset[1] : ].lower()
                                if i_content.startswith(lows[j]):
                                    O.write(u"%s\t%s\t%s\n" %(lows[j], lows[i], i_offset)) 

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
