# UFO-Search-Engine

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
# UFO-Search-Engine


index.py is our index builder

Indexer 



``` sh
    Functions:

    def main():

        Variable:

            f (file): take input file ufo_reports_with_coordinates.csv
            my_analyzer (analyzer): analyzer is the preprocessing for document 
            schema (Schema): inverted index schema
            ix (index): inverted ndex file, which is also a folder


```


Search engine

search_by_query.py
Functions:


``` sh
        def printtfidf(results): 
            print all tfidf search result

            arguments: 
                results (list): tfidf result, a list of index

        def printpagerank(nxresult):
            print all page ranking search result


            arguments: 
                nxresult (list): page ranking result, a list of index


        def printquery_expansion(expansionresults, newquery):
            print expanded query search result

            arguments: 
                expansionresults (list): page ranking result, a list of index
                newquery (list): list of expanded term 



        def visualize(G, nxresult):
            visualizing the page ranking result in 
            G (graph): cosine similarity graph 
            nxresult (list): page ranking result, a list of index



        def main():
            taking queries and get search result
            Variable:
                queries (list): list of queries
                searcher (searcher): query searcher
                qp (QueryParser): QueryParser
                whooshresults (list): tfidf result
                G (graph): to do page ranking
                similarity (array): cosine similarity table

```


Web craweler 


index_scrape_save.py scrape website by shape

``` sh

    function: 

        toCSV(linkSet, shape): save herf to csv
            linkSet (list): list of herf
            shape (string): shape

        shapeLinkList(shape): tell you if the shape is valid or not, if so, locate unique href
            shape (string): shape
```


nu_scrape.py scrape the target pages defined by index_scrape_save.py for each shape
function: 

``` sh
   

        def regFix(someText): regular expression to normalize all text
            someText (string): input text
            return newText (string): normalized text
            
        def parse_response(url_response): return the text for each field in html
            url_response (response): url_response
            return ([date, time1, location, shape1, duration, text])


        def enumerate_lxml(shape_fromlist): go thru all the links return doc
            return df (datafram): document  

```
        

Some libraries should be installed before you run the code. NLTK, Whoosh, Networkx, sklearn.

Part of Evaluation is been done in result_evaulation.csv
