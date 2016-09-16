# UFO-Search-Engine

#Liu, Jingye(jingye)
#Lee, Younghoon (younggns)
#Klein, Joseph (armennen)

The UFO-Search Engine is software and a command line program to search for UFO witness in our UFO documnet index.

Prominent features include:
index.py is taking our dataset into inverted index.
search_by_query.py will take txt file as input and search for the queries with the txt file line by line


To run index.py
index.py will take the as input, which depends on 

``` sh
$ python index.py
```
index.py will store the inverted index into a directory index

To search_by_query.py

``` sh
$ python search_by_query.py sample_queries.txt

```
Queries in sample_queries.txt should sperated by lines.

this is a sample of list of queries in sample_queries.txt

``` sh
fast fireball
area 51
little green alien
```

Some libraries should be installed before you run the code. NLTK, Whoosh, Networkx, sklearn.

Part of Evaluation is been done in result_evaulation.csv


To run web crawler 

``` sh
index_scrape_save.py

```

``` sh
$ python nu_scrape.py

```

Libraries required to run nu_scrape.py:fromstring, lxml, time, pandas, sys, os, requests, csv, Beautiful Soup, random, codecs, re, time, tqdm, libxml2dom