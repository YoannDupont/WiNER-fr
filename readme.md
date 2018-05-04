# WiNER (Wikinews for Named Entity Recognition) Corpus

WiNER is a corpus for Named Entity Recognition. It uses Wikinews texts as a base. WiNER is a free corpus.

The current named entity tagset is:

- Date (absolute dates.)
- Event (conferences, sports events, annual events, celebration days, named climatic events, etc.)
- Hour (absolute hours. If present, they include time zones, UTC, GMT, etc.)
- Location (countries, towns, regions, addresses, astophysicals objects, hydrophysical objects, etc.)
- Organization (non profit organizations, companies, medias, etc.)
- Person (human individuals, without their title or function. They can be actual people or fictional characters.)
- Product (physical objects, brands, softwares.)

The tagset was defined using various campaigns or resources: [MUC-6](http://www.aclweb.org/anthology/C96-1079), [CoNLL-2003](https://arxiv.org/pdf/cs/0306050.pdf), [Named Entity annotated French Treebank](https://hal.inria.fr/file/index/docid/703108/filename/taln12ftbne.pdf) and [Quaero](http://www.quaero.org/media/files/bibliographie/quaero-guide-annotation-2011.pdf) . Every type defined in this tagset is directly taken from one of those.

The aim of this tagset is to be covering yet as simple as possible.

# Nesting of named entities

Named Entities may be nested. Some examples:

- "Yearly Conference YEAR" is an event within which "YEAR" is a date.
- "PERSON_NAME University" is an organization within which "PERSON_NAME" is a Person.
- "University of LOCATION" is an organization within which "LOCATION" is a Location.
- "Company COUNTRY" is an organization within which "COUNTRY" is a Location.

# The texts

Texts were extracted from Wikinews. The documents contain the title and the content of the article. We do not include captions, sources, or any other content of the original page.

Some texts are to be removed:

- a document were there is only one sentence to introduce a list of scores of some sports event.

# The documents

Annotated documents are stored using the BRAT format: one ".txt" file for the raw content and one ".ann" file for the annotations. Files may be numerous, so they are sorted using this folder hierarchy:

```bash
├── year
│   ├── month1
│   │    ├── *.ann
│   │    └── *.txt
│   ├── month2
│   │    ├── *.ann
│   │    └── *.txt
│   ├── year-month1-urls.txt
│   └── year-month2-urls.txt
```
Where "year-month-urls.txt" is a list of key/value pairs where keys are the file names and the values are the URLs of the corresponding Wikinews articles.

# License

Wikinews texts are licensed under [Creative Commons Attribution 2.5](https://creativecommons.org/licenses/by/2.5/) unless stated otherwise on the Wikinews website.

Annotations are licensed under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) .

# Resources

- [Wikinews](https://en.wikinews.org/wiki/Main_Page)
- [french Wikinews](https://fr.wikinews.org/wiki/Accueil)

# References of other projects

- MUC-6
```latex
@inproceedings{grishman1996message,
  title={Message understanding conference-6: A brief history},
  author={Grishman, Ralph and Sundheim, Beth},
  booktitle={COLING 1996 Volume 1: The 16th International Conference on Computational Linguistics},
  volume={1},
  year={1996}
}
```
- CoNLL 2003
```latex
@inproceedings{tjong2003introduction,
  title={Introduction to the CoNLL-2003 shared task: Language-independent named entity recognition},
  author={Tjong Kim Sang, Erik F and De Meulder, Fien},
  booktitle={Proceedings of the seventh conference on Natural language learning at HLT-NAACL 2003-Volume 4},
  pages={142--147},
  year={2003},
  organization={Association for Computational Linguistics}
}
```
- Named Entity annotated French Treebank
```latex
@inproceedings{sagot2012annotation,
  title={Annotation r{\'e}f{\'e}rentielle du Corpus Arbor{\'e} de Paris 7 en entit{\'e}s nomm{\'e}es},
  author={Sagot, Beno{\^\i}t and Richard, Marion and Stern, Rosa},
  booktitle={Traitement Automatique des Langues Naturelles (TALN)},
  volume={2},
  year={2012}
}
```
- Quaero
```latex
@inproceedings{grouin2011proposal,
  title={Proposal for an extension of traditional named entities: From guidelines to evaluation, an overview},
  author={Grouin, Cyril and Rosset, Sophie and Zweigenbaum, Pierre and Fort, Kar{\"e}n and Galibert, Olivier and Quintard, Ludovic},
  booktitle={Proceedings of the 5th Linguistic Annotation Workshop},
  pages={92--100},
  year={2011},
  organization={Association for Computational Linguistics}
}
```
