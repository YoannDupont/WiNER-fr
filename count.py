import codecs

from sem.storage import Document
from sem.importers import brat_file
from sem.exporters import CoNLLExporter
from sem.modules import SegmentationModule
from sem.storage.annotation import Tag, Annotation, get_top_level

def main(infile):
    document = brat_file(infile)
    tokenizer = SegmentationModule("fr")
    tokenizer.process_document(document)
    print len(document.segmentation("paragraphs"))
    print len(document.segmentation("sentences"))
    print len(document.segmentation("tokens"))
    #print len(get_top_level(document.annotation("NER")))

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser("Converts BRAT files to 2-columns CoNLL")
    parser.add_argument("infile",
                        help="the input files")
    
    args = parser.parse_args()
    main(**vars(args))
