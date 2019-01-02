#-*- coding: utf-8 -*-

import os
import sys
import codecs
import re

import sem.importers
from sem.storage import Document, SEMCorpus, Annotation
from sem.exporters import BratExporter

lang2months = { # firt element is empty so index method returns values from 1 to 12
    u"fr": [u"", u"janvier", u"février", u"mars", u"avril", u"mai", u"juin", u"juillet", u"août", u"septembre", u"octobre", u"novembre", u"décembre"],
    u"en": [u"", u"january", u"febuary", u"march", u"april", u"may", u"june", u"july", u"august", u"september", u"october", u"november", u"december"]
}

def main(infilename,
         outdir=u".", lang="fr"):
    
    months = lang2months[lang]
    try:
        infilename = infilename.decode(sys.getfilesystemencoding())
    except:
        pass
    
    numbers = re.compile("([0-9]+)", re.U + re.I)
    
    corpus = SEMCorpus.from_xml(infilename)
    link_filename = os.path.join(os.path.dirname(infilename), os.path.basename(infilename)[:7] + "-urls.txt")
    with codecs.open(link_filename, "rU", "utf-8") as link_file:
        l = [line.strip() for line in link_file if line.strip()]
    documents = corpus.documents
    documents.sort(key=lambda x: l.index(x.name))
    
    try:
        os.makedirs(outdir)
    except:
        pass
    
    couples = {u"NER": u"NER"}
    exporter = BratExporter()
    prev_timestamp = u""
    nth_timestamp = 1
    with codecs.open(os.path.join(outdir, "%s" %(os.path.basename(link_filename))), "w", "utf-8") as O:
        for nth, document in enumerate(documents, 1):
            dates = [annotation for annotation in document.annotation("NER") if annotation.value == "Date"]
            dates = [date for date in dates if len(document.content[date.lb : date.ub].strip().split()) == 3]
            try:
                parts = document.content[dates[0].lb : dates[0].ub].split()
                parts[0] = int(numbers.findall(parts[0])[0])
            except:
                parts = document.content[dates[1].lb : dates[1].ub].split()
                parts[0] = int(numbers.findall(parts[0])[0])
            parts[1] = months.index(parts[1].lower())
            parts[2] = int(parts[2])
            timestamp = u"%04i_%02i_%02i" %(parts[2], parts[1], parts[0])
            if timestamp == prev_timestamp:
                nth_timestamp += 1
            else:
                nth_timestamp = 1
            prev_timestamp = timestamp
            docname = u"%s-%03i" %(timestamp, nth_timestamp)
            O.write("%s\t%s\n" %(docname, document.name))
            actual_outdir = os.path.join(outdir, str(parts[2]), u"%02i" %parts[1])
            try:
                os.makedirs(actual_outdir)
            except:
                pass
            with codecs.open(os.path.join(actual_outdir, docname + ".txt"), "w", "utf-8") as txt:
                txt.write(document.content)
            with codecs.open(os.path.join(actual_outdir, docname + ".ann"), "w", "utf-8") as ann:
                ann.write(exporter.document_to_unicode(document, couples))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser("...")
    parser.add_argument("infilename",
                        help="the input file (SEM XML)")
    parser.add_argument("-o", "--outdir", default=".",
                        help="the output directory (default: %(default)s)")
    parser.add_argument("-l", "--lang", default="fr",
                        help="the language for months (default: %(default)s)")
    
    args = parser.parse_args()
    main(args.infilename,
         outdir=args.outdir)
    sys.exit(0)
