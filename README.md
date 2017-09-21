# nlp-util
Random utilities for NLP

## Corpus Preprocessing

| Corpus Name | Script | Description |
| :---------- | :----- | :---------- |
| ICWSM 2009 Spinn3r Blog Dataset | Spinn3r-2009-extract.py | Extract select (and clean) text |
| PPDB (Paraphrase Database) | PPDB-extract.py | Extract select paraphrases |
| MSLT (Microsoft Speech Language Translation) | MSLT-repack.sh, MSLT-extract.py | Extract monolingual/parallel data |

#### [ICWSM 2009 Spinn3r Blog Dataset](http://www.icwsm.org/data/)
```
Usage:    Spinn3r-2009-extract.py [-h] -f FILE [FILE ...] [-l LANGUAGES [LANGUAGES ...]]
                                  -e ELEMENTS [ELEMENTS ...] [-u] [-c]
Examples: python Spinn3r-2009-extract.py -f BLOGS-tiergroup-1.tar.gz -e title description -l en -u -c > output.en
Optional arguments:
  -f FILE [FILE ...], --file FILE [FILE ...]
                        Spinn3r tar.gz file(s)
  -l LANGUAGES [LANGUAGES ...], --languages LANGUAGES [LANGUAGES ...]
                        language(s) to be extracted (e.g. en)
  -e ELEMENTS [ELEMENTS ...], --elements ELEMENTS [ELEMENTS ...]
                        element(s) to be extracted (e.g. title, description)
  -u, --unescape        unescape text (e.g. "&amp;"->"&") (default: False)
  -c, --clean           clean text (drop <*>/URLs, condense spaces) (default: False)
```

#### [PPDB (Paraphrase Database)](http://paraphrase.org/#/download)
```
Usage:    PPDB-extract.py [-f FILE] [-a FEATURE] [-t THRESHOLD] [-e ENTAILMENT]
Examples: gzip -dc ppdb-2.0-s-lexical.gz | python PPDB-extract.py -e Equivalence > output
Optional arguments:
  -f FILE, --file FILE  unzipped input file(s) (glob patterns are supported)
  -a FEATURE, --feature FEATURE
                        the feature used for filtering
  -t THRESHOLD, --threshold THRESHOLD
                        the threshold used for filtering (feature value >= threshold are kept)
  -e ENTAILMENT, --entailment ENTAILMENT
                        the entailment type(s) used for filtering (regular expression)
```

#### [MSLT (Microsoft Speech Language Translation)](https://github.com/MicrosoftTranslator/MSLT-Corpus)
1. Repack MSLT text (Python has an issue in handling original zip file).
```
bash MSLT-repack.sh /absolute/path/to/MSLT_Corpus.zip
```
2. Extract parallel or monolingual data from MSLT_Corpus.tgz
```
Usage:    MSLT-extract.py -f FILE -s SOURCE [-t TARGET] [-c CATEGORY] [-o OUTPUT]
Examples: python MSLT-extract.py -f MSLT_Corpus.tgz -s fr -t en -c dev -o MSLT.fr-en
          python MSLT-extract.py -f MSLT_Corpus.tgz -s fr > MSLT.fr
Optional arguments:
  -f FILE, --file FILE  input repacked tgz file
  -s SOURCE, --source SOURCE
                        source language (e.g. fr)
  -t TARGET, --target TARGET
                        target language (e.g. en)
  -c CATEGORY, --category CATEGORY
                        dev or test? (default: dev)
  -o OUTPUT, --output OUTPUT
                        output file (used for parallel data)
```

## Statistics

| Script | Description |
| :----- | :---------- |
| word-count.py | Count words |

#### Word Count
```
Usage:   word-count.py [-i INPUT] [-w WHITE_LIST] [-b BLACK_LIST] [-s]
Example: cat file | python word-count.py -w list -s > output
Optional arguments:
  -i INPUT, --input INPUT
                        input file(s) (glob patterns are supported)
  -w WHITE_LIST, --white-list WHITE_LIST
                        only count words in the write list
  -b BLACK_LIST, --black-list BLACK_LIST
                        ignore words in the black list
  -s, --statistics      print statistics (default: False)
```