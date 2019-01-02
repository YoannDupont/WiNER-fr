#-*- coding: utf-8 -*-

import urllib
import codecs
import sys
import os
import time

from xml.etree import cElementTree as ET

import sem.importers
from sem.storage import Document, SEMCorpus

lang2months = { # firt element is empty so index method returns values from 1 to 12
    u"fr": [u"", u"janvier", u"février", u"mars", u"avril", u"mai", u"juin", u"juillet", u"août", u"septembre", u"octobre", u"novembre", u"décembre"]
}

def main(year, month, lang="fr"):
    try:
        month = month.decode(sys.getfilesystemencoding())
    except:
        pass
    base_url = u"https://%s.wikinews.org" %(lang)
    month_url = u"https://%s.wikinews.org/wiki/Wikinews:%s/%s" %(lang, year, urllib.quote(month.encode("utf-8")))
    month_index = lang2months[lang].index(month)

    content = urllib.urlopen(month_url).read()

    root = ET.fromstring(content)

    urls = []
    for element in root.iter("div"):
        if element.attrib.get("class", "") == "journee":
            for a in element.iter("a"):
                href = urllib.unquote(a.attrib["href"].rsplit("?")[0]).decode("utf-8")
                urls.append(base_url + href)

    try:
        os.makedirs(os.path.join(u"by_month", year))
    except:
        pass
    
    with codecs.open(os.path.join(u"by_month", year, u"{}-{:02}-urls.txt".format(year, month_index)), "w", "utf-8") as O:
        for url in urls:
            O.write(url + u"\n")
    
    corpus = SEMCorpus()
    for nth, url in enumerate(urls, 1):
        print "(%i/%i)" %(nth, len(urls))
        try:
            print url
        except:
            print repr(url)
        try:
            corpus.add_document(sem.importers.from_url(url, wikinews_format=True))
            #corpus[-1].name = corpus[-1].name.replace('"', '&quot;')
        except:
            pass
        
        time.sleep(1.0)
    with codecs.open(os.path.join(u"by_month", year, u"%s-%02i-%s.sem.xml" %(year, month_index, month)), "w", "utf-8") as O:
        corpus.write(O)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser("...")
    parser.add_argument("year",
                        help="the year")
    parser.add_argument("month",
                        help="the month")
    parser.add_argument("-l", "--lang", default=u"fr",
                        help="the language of the articles (default: %(default)s)")
    
    args = parser.parse_args()
    main(args.year, args.month, lang=args.lang)
    sys.exit(0)
