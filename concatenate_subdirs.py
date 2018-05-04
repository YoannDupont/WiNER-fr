#-*- coding: utf-8 -*-

import os
import sys
import codecs

from sem.storage import Document, Annotation
from sem.exporters import BratExporter

from concatenate_dir import make_data, NUM_NEWLINES

def main(indirnames, outfilename, default_shift=0):
    dirs = []
    for indirname in indirnames:
        dirs.extend([os.path.join(indirname, name) for name in sorted(os.listdir(indirname)) if os.path.isdir(os.path.join(indirname, name))])
    
    contents = []
    annotations = []
    shift = 0
    for dirname in dirs:
        cur_contents, cur_annotations, cur_shift = make_data(dirname, default_shift=shift)
        contents.extend(cur_contents)
        annotations.extend(cur_annotations)
        shift = cur_shift
    
    document = Document("_doc_", content=(u"\n"*NUM_NEWLINES).join(contents))
    document.add_annotation(Annotation("NER", annotations=annotations))
    exporter = BratExporter()
    with codecs.open(outfilename+".ann", "w", "utf-8") as O:
        O.write(exporter.document_to_unicode(document, {"ner":"NER"}))
    with codecs.open(outfilename+".txt", "w", "utf-8") as O:
        O.write(document.content)

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
