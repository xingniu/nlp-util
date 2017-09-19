# nlp-util
Random utilities for NLP

## Corpus Preprocessing

| Corpus Name | Script | Description |
| :---------- | ------ | :---------- |
| ICWSM 2009 Spinn3r Blog Dataset | Spinn3r-2009-extract.py | Extract select (and clean) text |
| PPDB (Paraphrase Database) | PPDB-extract.py | Extract select paraphrases |

#### [ICWSM 2009 Spinn3r Blog Dataset](http://www.icwsm.org/data/)
```
Usage:    python Spinn3r-2009-extract.py -f FILE -e ELEMENT [OPTION...]
Examples: python Spinn3r-2009-extract.py -f BLOGS-tiergroup-1.tar.gz -e title description -l en > output.en
Options:
-f --file        tar.gz files
-e --elements    elements to be extracted (e.g. title, description)
-l --languages   languages to be extracted (e.g. en)
-u --unescape    unescape text (e.g. "&amp;"->"&")
-c --clean       clean text (drop <*>/URLs, condense spaces)
```

#### [PPDB (Paraphrase Database)](http://paraphrase.org/#/download)
```
Usage:    python PPDB-extract.py [OPTION...]
Examples: gzip -dc ppdb-2.0-s-lexical.gz | python PPDB-extract.py -e Equivalence > output
Options:
-f --file         unzipped input file (glob patterns are supported)
-a --feature      the feature used for filtering
-t --threshold    the threshold used for filtering (>= threshold are kept)
-e --entailment   the entailment type used for filtering (RE)