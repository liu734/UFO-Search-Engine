import re
import lxml

import time
# from lxml import etree
import pandas as pd

from lxml import html
import sys, os, codecs

import requests, csv
# from bs4 import BeautifulSoup
import random

from index_scrape_save import shapeLinkList
from tqdm import tqdm
# import cStringIO
# import StringIO
import libxml2dom

# parser = etree.HTMLParser()
start_time = time.clock()
max_retry_count=3
header_push = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
}
# timeout_counter=0
success = False
shape_list= list()
#getting a list of all the shapes
# for joe in link_tags:
#     shape_list.append(joe.get_text().encode('utf-8'))

#done list Unspecified (9509 seconds or 2.84 sec/entry), changed, changing 10215.4637291 seconds, Crescent, Chevron
#
shape_list = ['Unspecified', 'changed', 'Changing', 'Chevron', 'Cigar', 'Circle', 'Cone', 'Crescent', 'Cross', 'Cylinder', 'Delta', 'Diamond', 'Disk', 'Dome', 'Egg', 'Fireball', 'Flare', 'Flash', 'Formation', 'Hexagon', 'Light', 'Other', 'Oval', 'pyramid', 'Rectangle', 'Round', 'Sphere', 'Teardrop', 'Triangle', 'TRIANGULAR', 'Unknown']
test_list2 = ['Other']
test_list1 =['Light']
test_list= ['Oval', 'pyramid', 'Rectangle', 'Round', 'Sphere', 'Teardrop', 'Triangle', 'TRIANGULAR', 'Unknown']

#You'll want to change this
clean_path= "C:/Users/Joe/Documents/NW_Code/Cleaned_csvs" #final preprocessed data (mostly)


headers = ['OccurrenceDate','Time','Location','Shape', 'Duration', 'Description']



# def enumerate_nested_links(shape_fromlist):
#     values = []
#     timeout_counter=0
#     number_of_pages=0

#     # for shape in list_of_shapes:
#         #set of inner links

#     # innerLinks = getListofLinks(shape_fromlist)
#     #calling function to return set of links
#     innerLinks = shapeLinkList(shape_fromlist)
#     length= len(innerLinks)
#     # time.sleep(1)
#     time.sleep(random.randrange(3,6,1))
#     for page in tqdm(innerLinks):
#         number_of_pages+=1

#         #page is [u'002/S02935.html']
#         #url needs to be :http://www.nuforc.org/webreports/002/S02935.html
#         url = "http://www.nuforc.org/webreports/{0}".format(page)

#         #Thanks to https://github.com/tmwsiy2012/playground/blob/4a79ccf94260eb3c6159c47f7745cc7ffba17794/ufo_data_scraper/test_scraper.py for several lines of code
#         success = False
#         while not success:
#             if timeout_counter < max_retry_count :
#                 try:
#                     response = requests.get(url,timeout=10, headers=header_push)
#                     success = True
#                     timeout_counter=0

#                 except:
#                     print 'Problem retrieving ', url, shape_fromlist, number_of_pages
#                     time.sleep(10)
#                     timeout_counter+=1
#             else:
#                 print 'Retry count exceeded:', url
#                 timeout_counter=0
#                 break
#         # response = requests.get(url)


#         soup = BeautifulSoup(response.text, "html.parser")
#         # print soup

#         for row in soup.findAll('tbody'):

#             # [u'Occurred : 11/30/1997 18:00  (Entered as : 11/30/97 1800)', u'Reported: 12/2/1997 00:12', u'Posted: 3/11/2003', u'Location: Sacramento, CA', u'Shape: Flare', u'Duration:30 seconds']
#             this =row.tr.td.findAll(text=True)

#             #the occurrence taking out the "(Entered as..." stuff.
#             # GOAL: --> Occurred : 11/30/1997 18:00
#             occ= this[0].split(" (")
#             #removing the "Occurred : " stuff
#             #Note: we are taking their word for it here but if we want all of the info for when the Entered info is informative, this is where we change the code
#             dateTime = occ[0].split(": ")

#             # 11/30/1997 18:00
#             dateTime= dateTime[1].rstrip()
#             location = "NA"
#             shape1 = "NA"
#             duration = "NA"
#             description = "NA"
#             cal_date= "NA"
#             time1= "NA"

#             if len(dateTime.split())>1 and len(dateTime)>3:
#                 # hasdateTime=True
#                 cal_date = dateTime.split()[0]
#                 time1 = dateTime.split()[1]
#             if len(dateTime.split())<=1 and len(dateTime)<=3:


#                 #use the reported date and time instead
#                 reported_date_raw = this[1].split(": ")
#                 reported_date = reported_date_raw[1].split()
#                 cal_date= reported_date[0]
#                 if len(reported_date)>1:
#                     time1 = reported_date[1]

#             if len(this[3].split(":"))>1:
#                 # location1 = this[3].split(":")[1]
#                 # location = this[3].split(": ")[1]
#                 # if re.sub(r'Location:\W?','', this[3]) != " ":

#                 location = re.sub(r'Location:\W?','', this[3])

#             if len(this[4].split(": "))>1:
#                 shape1 = this[4].split(": ")[1]



#             if len(this[5].split(":"))>1:
#                 duration = this[5].split(":")[1]


#             if len(row.findAll('tr'))>1:
#                 tr=row.findAll('tr')[1]

#                 # description = tr.td.find(text=True)
#                 description = tr.get_text().strip("\n")
#                 # print description


#             values.append([cal_date, time1, location, shape1, duration, description])
#             # print number_of_pages, " complete so far"
#             # with tqdm(total=length) as pbar:
#             #     pbar.update(number_of_pages)
#             time.sleep(3)

#     df = pd.DataFrame(values)
#     print "Finished with", shape
#     return df
def regFix(someText):
    someText = someText.textContent  #use textContent
    allwords=re.compile(r"(Location|Occurred|Duration[:]?|Shape|[ ]?:[ ]|[ ]{0,3}\(Entered as.*$)")
    newText=allwords.sub('', someText)
    if newText == " " or len(newText)<1:
        newText="None"
    return newText


def parse_response(url_response):
    # tree = html.fromstring(url_response)
    # # # print soup
    # # result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
    # # print result
    # # templist = list()
    # content = tree.xpath("//td//text()")
# def libx2():
    #validates whether or not the html is good enough for this stuff to work
    doc = libxml2dom.parseString(url_response, html=1)

    all_stuff = doc.xpath("//td//text()")
    #placeholder
    oc = doc.xpath("//td//text()[contains(., 'Occurred')]")
    # test = doc.xpath("//td//text()[contains(., 'Reported')]")
    # test = doc.xpath("//td//text()[contains(., 'Posted')]")
    loc = doc.xpath("//td//text()[contains(., 'Location')]")
    #duration
    dur = doc.xpath("//td//text()[contains(., 'Duration')]")
    #shape
    sh = doc.xpath("//td//text()[contains(., 'Shape')]")
    location = "None"
    shape1 = "None"
    duration = "None"
    # date= "NA"
    # time1= "NA"

    #how many nodes we got here; anything after 5 in python indices should qualify
    length = len(all_stuff)
    # is_Summary = re.compile(r'Summary')
    #our text field
    removeHTML = re.compile(r'\&\w.*;')
    text =''
    for i in range(6, length):

        this=all_stuff[i].textContent+' '
        # this1 = removeHTML.sub('', this)
        text+=''.join(this)
        # text=''.join(all_stuff[i].toString())

    # text = text.decode("utf-8", "ignore")
    text=text.rstrip()


    # test = doc.xpath("//td//text()[contains(., '')]")


    occurred = regFix(oc[0])
    date = occurred.split()[0]
    try:
        time1 = occurred.split()[1]
    except:
        # date = "None"
        # date = occurred.split()[0]
        time1="None"
    # try:
    #     time1 = occurred.split()[1]
    # except:
    #     time1="None"
    #leaving reported just in case we need it later
    # reported = regFix(content[1])
    # location = regFix(loc[0]).decode('iso-8859-2', errors='ignore')
    # location = regFix(loc[0]).decode('latin-1', errors='ignore')
    # location = regFix(loc[0]).decode('utf-8', errors='ignore')
    location = regFix(loc[0]).decode('iso-8859-1', errors='ignore')
    # location = "FILLER"
    shape1 = regFix(sh[0])
    duration = regFix(dur[0])
    # text_blob1 = content[6]
    # is_Summary = re.match(r'Summary', text_blob1)
    # if is_Summary:
        # summary = regFix(text_blob1)
        # text = content[7]
    # else:
        # text = text_blob1
    def testing():
        # print reported, "reported"
        print location, "Location"
        print shape, "shape"
        print duration, "duration"
        # if is_Summary:
        #     print summary, "summary"
        print text, "text"
        print date, "date"
        print time1, "time"
    # testing()
    # values = ([date, time1, location, shape1, duration, text])
    # cvswrite(values)
    return ([date, time1, location, shape1, duration, text])

#         values.append([cal_date, time1, location, shape1, duration, description])
#         # print number_of_pages, " complete so far"
#         # with tqdm(total=length) as pbar:
#         #     pbar.update(number_of_pages)
# time.sleep(3)

def enumerate_lxml(shape_fromlist):

    vals = []

    # number_of_pages=0

    #calling function to return set of links
    # print shape_fromlist

    innerLinks = shapeLinkList(shape_fromlist)
    # try:
    #     length= len(innerLinks)

    # except:
    #     print "THIS SHAPE ISNT ON FILE", shape_fromlist



    # time.sleep(1)

    for page in tqdm(innerLinks):
        timeout_counter=0


        time.sleep(random.randrange(3,5,1))
        # number_of_pages=1

        #page is [u'002/S02935.html']
        #url needs to be :http://www.nuforc.org/webreports/002/S02935.html
        # http://www.nuforc.org/webreports/036/S36881.html
        # http://www.nuforc.org/webreports/122/S122431.html

        url = "http://www.nuforc.org/webreports/{0}".format(page)

        #Thanks to https://github.com/tmwsiy2012/playground/blob/4a79ccf94260eb3c6159c47f7745cc7ffba17794/ufo_data_scraper/test_scraper.py for several lines of code
        success = False
        while not success:

            try:
                response = requests.get(url,timeout=10, headers=header_push)


                #if 200 status for empty pages like http://www.nuforc.org/webreports/035/S35193.html
                if len(response.content)==0:
                    print "bad file", url
                    break
                if response.status_code == requests.codes.ok:
                    # timeout_counter=0
                    vals.append(parse_response(response.text))
                    # vals.append(parse_response(response.content))
                    # output.writerow(vals)
                    # number_of_pages =1
                    time.sleep(0.5)
                    success = True
                else:
                    break

            except:
                print 'Problem retrieving ', url, shape_fromlist, timeout_counter
                time.sleep(20)
                timeout_counter+=1
                # continue
                if timeout_counter > max_retry_count :
                    print timeout_counter, "timeout counter"
                    print 'Retry count exceeded:', url
                    timeout_counter=0
                    time.sleep(30)
                    break
                    # continue
                else:
                    # print "JOE JOE JOE"
                    # print timeout_counter, "timeout"
                    # print max_retry_count, "max retry"
                    # http://www.nuforc.org/webreports/116/S116243.html
                    # break
                    continue
        # else:
            #     print 'Retry count exceeded:', url
            #     timeout_counter=0
            #     time.sleep(30)
            #     break

            # response = requests.get(url)

            # parser = etree.HTMLParser()

            # tree   = etree.parse(StringIO(response.content), parser)

            # result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
            # print(result)
            # if success:
                # def cvswrite(vals):
                # vals=parse_response(response.content)
    # csvwrite(writestyle, THEPATH, vals)

                # vals=parse_response(response.content)
                # csvwrite(writestyle, THEPATH, vals)
                # output.writerow(vals)

    # print "finished writing csv for ", shape
        #     # values.append(parse_response(response.content))
        #     values=parse_response(response.content)

        #     time.sleep(3)


    df = pd.DataFrame(vals)
    vals = list()
    # file.close()
    print "Finished processing",shape
    return df






df = pd.DataFrame()
for shape in test_list:

    df= enumerate_lxml(shape)

    title = "nuforc_"+shape+".csv"
    THEPATH = os.path.join(clean_path, title)
    df.to_csv(THEPATH, sep=',', header= headers, index_label='rowNumber', encoding='utf-8')
    print "Finished writing",shape
    # time.sleep(1)?
# df.to_csv("testencode.csv", sep=',', header= headers, index_label='rowNumber', encoding='utf-8')
print time.clock() - start_time, "seconds"
# # print df


# df.to_csv('nuforc_main.csv', sep=',', header= headers, index_label= "rowNumber", encoding= 'utf-8')



