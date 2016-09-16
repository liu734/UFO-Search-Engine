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
#import maths
import os, os.path
from whoosh import index
from whoosh.fields import Schema, TEXT

from whoosh.index import open_dir
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT, DATETIME
from whoosh.index import create_in

from whoosh.qparser import QueryParser

from whoosh.query import *
from whoosh.analysis import LowercaseFilter
from whoosh.analysis import StopFilter
from whoosh.analysis import RegexTokenizer


def main():
    
    
    
    dt={}
    latlong={}
    desc={}
    shape={}
    state={}
    
    index=0
    
    with open('ufo_reports_with_coordinates.csv', 'rU') as f:
        
        reader = csv.DictReader(f)
        for row in reader:
            
            
            if row['OccurrenceDate'] !='' and row['LatLong']!='' and row['Description'] !='' and row['State']!='' and ',' in row['LatLong']:
            
                try:
                    dt[index]=time.strptime(row['OccurrenceDate']+' '+row['Time'], "%m/%d/%y %H:%M")
                    
                    dt[index]=datetime.datetime.fromtimestamp(time.mktime(dt[index]))
                    
                    latlong[index]=unicode(row['LatLong'], errors='replace')
                    
                    
                    desc[index]=unicode(row['Description'], errors='replace')
                    state[index]=unicode(row['State'], errors='replace')
                    
                    index+=1
                except:
                    a=''
    my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter()

    schema = Schema(index=ID(stored=True), state=TEXT(stored=True), desc=TEXT(stored=True, analyzer=my_analyzer), dt=DATETIME(stored=True), latlong=TEXT(stored=True))



    if not os.path.exists("index"):
        os.mkdir("index")
    ix = create_in("index", schema)
    ix = open_dir("index")

    writer = ix.writer()


    for i in range(len(desc)):
        writer.add_document(index=unicode(i), state=state[i],desc=desc[i], dt=dt[i], latlong=latlong[i])

    writer.commit()



if __name__ == '__main__':
    main()