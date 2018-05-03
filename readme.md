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

The aim of this tagset is to be covering yet as simple as possible. There are lots of disagreements as soon as semantics are involved. Our stance is that semantics should belong as much as possible to the disambiguation phase.

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
