#-*- coding: utf-8 -*-

import os
import sys
import codecs

from sem.importers import brat_file
from sem.storage import Document, Annotation, Tag
from sem.exporters import BratExporter
from sem.storage.annotation import get_top_level

NUM_NEWLINES = 4

def make_data(indirname, default_shift=0, top_level=True):
    files = [f for f in sorted(os.listdir(indirname)) if f.endswith(".ann")]
    annotations = []
    contents = []
    shift = default_shift
    for filename in files:
        full_path = os.path.join(indirname, filename)
        document = brat_file(full_path)
        if top_level:
            annotations.extend([Tag(a.value, a.lb+shift, a.ub+shift) for a in get_top_level(document.annotation("NER"))])
        else:
            annotations.extend([Tag(a.value, a.lb+shift, a.ub+shift) for a in document.annotation("NER")])
        contents.append(document.content)
        shift += NUM_NEWLINES + len(document.content)
    
    return contents, annotations, shift

def main(indirname, outfilename, default_shift=0, top_level=False):
    contents, annotations, shift = make_data(indirname, default_shift=default_shift, top_level=top_level)
    
    document = Document("_doc_", content=(u"\n"*NUM_NEWLINES).join(contents))
    document.add_annotation(Annotation("NER", annotations=annotations))
    exporter = BratExporter()
    with codecs.open(outfilename+".ann", "w", "utf-8") as O:
        O.write(exporter.document_to_unicode(document, {"ner":"NER"}))
    with codecs.open(outfilename+".txt", "w", "utf-8") as O:
        O.write(document.content)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser("Concatenate the different BRAT files contained in a directory.")
    parser.add_argument("indirname",
                        help="the input directory")
    parser.add_argument("outfilename",
                        help="the output file name")
    parser.add_argument("-t", "--top-level", action="store_true",
                        help="Get top level annotations")
    
    args = parser.parse_args()
    main(args.indirname, args.outfilename, top_level=args.top_level)
    sys.exit(0)
