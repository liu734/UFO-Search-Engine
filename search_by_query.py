


import xml.etree.ElementTree as ET
import nltk
import re
import os, sys
import string
from nltk.stem import *
import collections
import json
import sys
import csv
import datetime
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from sklearn.metrics.pairwise import linear_kernel
import networkx
import networkx as nx
import json
import matplotlib.pyplot as plt
import os, os.path
from whoosh import index




from whoosh.fields import Schema, TEXT

from whoosh.index import open_dir
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT, DATETIME
from whoosh.index import create_in

from whoosh import qparser
from whoosh.qparser import QueryParser

from whoosh.query import *


from geopy.distance import vincenty



def printtfidf(results):
    print "Top 10 Ranked Document by TFIDF (our baseline)"
    print results[0:10]


def printpagerank(nxresult):
    print "Top 10 ranking by nx pageranking"
    print [ int(x[0]) for x in nxresult[0:10]]


def printquery_expansion(expansionresults, newquery):
    print "Top 10 Ranked Document by Query Expansion with Query Expanded to "+str(newquery)
    print [int(x['index']) for x in expansionresults][0:10]



def visualize(G, nxresult):
    
    
    top10nodes=[x[0] for x in nxresult[:10]]
    nottop10nodes=[x[0] for x in nxresult[10:]]

    pos=nx.shell_layout(G)
    
    nx.draw_networkx_nodes(G,pos, nodelist=top10nodes,node_color='r',node_size=100,alpha=0.8)
    nx.draw_networkx_nodes(G,pos,nodelist=nottop10nodes,node_color='b',node_size=20,alpha=0.8)
        
        
    edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())
        
    nx.draw_networkx_edges(G,pos,edge_color=weights,edge_cmap=plt.cm.Blues)

    #plt.show()



def main():
    
    ix = open_dir("index")
    searcher = ix.searcher()
    
    

    docid=1
    if len(sys.argv)>=2:
        input=sys.argv[1]
    
    
    else:
        print 'You need to type a file name\nType python search.py filename'
        exit()
    

    queries=[]

    with open(input, 'r') as f:
        for line in f:
            queries.append(line)


    qp = QueryParser("desc", schema=ix.schema)

    qp.add_plugin(qparser.WildcardPlugin())
    qp.add_plugin(qparser.PrefixPlugin())
    qp.add_plugin(qparser.RegexPlugin())


    f= open('testresult.txt', 'w')


    for query in queries:
        myquery = qp.parse(query)
        
        
        searcher = ix.searcher()

        results = searcher.search(myquery, limit=400)

        print "\nYou are searching:"
        all_terms=list(myquery.iter_all_terms())
        print query.strip()
        print 'number of hits'
        print (len(results))


        if (len(results))==0:
            continue
        whooshresults =[int(x['index']) for x in results]

    # hits


        myresults=[x['index'] for x in results]

        vectorizer = TfidfVectorizer(encoding="latin-1", stop_words='english')

        corpus=[x['desc'] for x in results]

        dt=[x['dt'] for x in results]

        latlong=[x['latlong'] for x in results]


#pageranding part

        X = vectorizer.fit_transform(corpus)

        X= X.toarray()

        similarity=cosine_similarity(X,X)

        G = nx.Graph()
        for i in range(len(myresults)):
            G.add_node(myresults[i])



        for i in range(len(similarity)):
            for j in range(i+1,len(similarity[i])):
                
                delta=abs(dt[i]-dt[j])
                
                loci=latlong[i][1:-1].split(',')
                locj=latlong[j][1:-1].split(',')
                
                
                loci=(loci[0],loci[1])
                locj=(locj[0],locj[1])
                
                #if similarity[i][j]>=0.1:
                #    G.add_edge(myresults[i],myresults[j], weight=similarity[i][j])
                
                if similarity[i][j]>=0.18 and delta<datetime.timedelta(days=7) and vincenty(loci, locj).miles<100:
                    G.add_edge(myresults[i],myresults[j], weight=(similarity[i][j]))

        nxresult=sorted(nx.pagerank(G, alpha=0.85).items(), key=lambda x:-x[1])


        #query expansion

        keywords = [keyword for keyword, score in results.key_terms("desc", docs=30, numterms=(len(all_terms)+1))]



        #get expanded query

        keywords=[('desc', x) for x in keywords]
        newterms=[x for x in keywords if x not in all_terms]
        newterms=newterms+all_terms
        newterms=[x[0]+':'+x[1] for x in newterms]
        newterms=' '.join(newterms)

        #expanded query
        print 'Do you want search?'
        print newterms



        newquery = qp.parse(newterms)

        print newquery

        searcher = ix.searcher()
                    
        expansionresults = searcher.search(newquery, limit=1000)


        nxdesc=[]
        for j in nxresult[0:10]:
            doc=searcher.document(index=j[0])
            nxdesc.append(j[0]+'\t'+doc['desc'])





        printpagerank(nxresult)
        printtfidf(whooshresults)
        printquery_expansion(expansionresults, newquery)

        visualize(G,  nxresult)




        #writing output

        f.write('\n\n'+query)
        
        f.write("\n\nTop 10 query expansion results baseline result\n")
        f.write(('\n'.join([x['index']+'\t'+x['desc'] for x in results][0:10])).encode('utf8'))
        
        f.write("\n\nTop 10 ranking by nx pageranking\n")
        f.write(('\n'.join(nxdesc)).encode('utf8'))
        
        f.write("\n\nTop 10 query expansion results\n")
        f.write(('\n'.join([x['index']+'\t'+x['desc'] for x in expansionresults][0:10])).encode('utf8'))


    f.close()






if __name__ == '__main__':
    main()