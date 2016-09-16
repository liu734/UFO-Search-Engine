from lxml.html import fromstring
import re
# from lxml import *
import lxml.html
import time

import pandas as pd

import sys, os

import requests,  csv
from bs4 import BeautifulSoup
import random
import csv, codecs
# import wget


#modify this to whatever path you're using
link_path = "C:\Users\Joe\Documents\NW_Code\Linklists_csvs"


start_time = time.clock()
max_retry_count=20
header_push = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
}

# success = False
shape_list= list()
#getting a list of all the shapes
# for joe in link_tags:
#     shape_list.append(joe.get_text().encode('utf-8'))


shape_list = ['Unspecified', 'changed', 'Changing', 'Chevron', 'Cigar', 'Circle', 'Cone', 'Crescent', 'Cross', 'Cylinder', 'Delta', 'Diamond', 'Disk', 'Dome', 'Egg', 'Fireball', 'Flare', 'Flash', 'Formation', 'Hexagon', 'Light', 'Other', 'Oval', 'pyramid', 'Rectangle', 'Round', 'Sphere', 'Teardrop', 'Triangle', 'TRIANGULAR', 'Unknown']
finished_list = []
# test_list = ['Delta', 'changed', 'Crescent']
# shape_list_partial =['Other', 'Oval', 'pyramid', 'Rectangle', 'Round', 'Sphere', 'Teardrop', 'Triangle', 'TRIANGULAR', 'Unknown']
def getListofLinks(shape):
    url = "http://www.nuforc.org/webreports/ndxs{0}.html".format(shape)
    if shape== "Unspecified":
        url="http://www.nuforc.org/webreports/ndxs.html"

    success = False
    timeout_counter=0
    time.sleep(random.randrange(2,8,1))
    while not success:
        if timeout_counter < max_retry_count :
            try:
                response = requests.get(url,timeout=20, headers=header_push)
                success = True
                timeout_counter=0

            except:
                print 'Problem retrieving ', url, shape
                time.sleep(10)
                timeout_counter+=1
        else:
            print 'Retry count exceeded:', url
            timeout_counter=0
            break



    response = requests.get(url,timeout=10, headers=header_push )

    soup = BeautifulSoup(response.text, "html.parser")

    links_per_shape = soup.select("td a")


    link_inside = set([ tag['href'] for tag in links_per_shape ])
    return link_inside

#saves off the html link list for each shape
def toCSV(linkSet, shape):

    title = ""+shape+"LinkIndex.csv"
    with open(os.path.join(link_path, title), 'wb') as file:
    # with open(title, 'wb') as file:
        output=csv.writer(file)

        # output.writerow([linkSet.split(",")])
        for row in linkSet:
            # print row
            output.writerow([row])
    print "finished writing csv for ", shape

# bunchalinks = list()
# if name == _main_():
if __name__ == "__main__":
    for shape in shape_list:
        time.sleep(5)
        bunchalinks=getListofLinks(shape)
        toCSV(bunchalinks, shape)
    print time.clock() - start_time, "seconds"


#function to read in the csv group and associates them with their shapes
def shapeLinkList(shape):
    templist = list()
    if shape in shape_list:
        title = ""+shape+"LinkIndex.csv"

        THEPATH = os.path.join(link_path, title)

        with open(THEPATH, 'rU') as csvfile:
            shape_links_list = csv.reader(csvfile)
            for row in shape_links_list:
                templist.append(row[0])
        return templist
    else:
        print "That's a bad shape. Please try again."


