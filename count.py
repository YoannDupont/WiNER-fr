import codecs

from sem.storage import Document
from sem.importers import brat_file
from sem.exporters import CoNLLExporter
from sem.modules import SegmentationModule
from sem.storage.annotation import Tag, Annotation, get_top_level
import collections

import re
spaces = re.compile("\s+", re.M)

def main(infiles):
    tokenizer = SegmentationModule("fr")
    token_count = 0
    nonspace_count = 0
    entity_counts = collections.Counter()
    entity2set = collections.defaultdict(set)
    for infile in infiles:
        document = brat_file(infile)
        tokenizer.process_document(document)
        token_count += len(document.segmentation("tokens"))
        nonspace_count += len(spaces.sub("", document.content))
        for entity in document.annotation("NER"):
            entity_counts[entity.value] += 1
            entity2set[entity.value].add(document.content[entity.lb : entity.ub].lower())
    print("number of documents\t{}".format(len(infiles)))
    print(f"token count\t{token_count}")
    print(f"character count\t{nonspace_count}")
    print()
    print("entity name\tcount\tunique count")
    for entity, count in sorted(entity_counts.items(), key=lambda x:(x[0],-x[1])):
        ucount = len(entity2set[entity])
        print(f"{entity}\t{count}\t{ucount}")
    count = sum(entity_counts.values())
    ucount = sum(len(s) for s in entity2set.values())
    print(f"global\t{count}\t{ucount}")
    #print len(get_top_level(document.annotation("NER")))

if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser("Compute some useful counts on BRAT annotated corpus.")
    parser.add_argument("infiles", nargs="+",
                        help="the input files")
    
    args = parser.parse_args()
    main(**vars(args))
