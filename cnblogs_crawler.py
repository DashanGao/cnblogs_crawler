# encoding=utf8

import urllib
import BeautifulSoup
import re
import json

# Created by Gao Dashan on 2017/4/26

# Crawl target data from "www.cnblogs.com"
target_url = "http://www.cnblogs.com"
res = urllib.urlopen(target_url)
soup = BeautifulSoup.BeautifulSoup(res)
post_list_div = soup.find(attrs={"id": "post_list"})
titlelnk = post_list_div.findAll(attrs={"class": "titlelnk"})
post_item_summary = post_list_div.findAll(attrs={"class": "post_item_summary"})
post_item_foot = post_list_div.findAll(attrs={"class": "post_item_foot"})
lightblue = post_list_div.findAll(attrs={"class": "lightblue"})
article_comment = post_list_div.findAll(attrs={"class": "article_comment"})
article_view = post_list_div.findAll(attrs={"class": "article_view"})
length = len(titlelnk)

# create new reference to hold modified strings
title = titlelnk
time = post_item_foot
name = lightblue
comment = article_comment
view = article_view
summary = post_item_summary

for i in range(length):
        title[i] = titlelnk[i].string.strip()
        summary[i] = post_item_summary[i].contents[len(post_item_summary[i].contents)-1].string.strip()
        time[i] = post_item_foot[i].contents[2].strip()
        name[i] = lightblue[i].string
        comment[i] = article_comment[i].a.string
        view[i] = article_view[i].a.string

# regular expression pattern: time_re : time regexp    num_re : view and comment number regexp
time_re = re.compile(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}')
num_re = re.compile(r'\d+')

# text format regulation
for i in range(length):
    time[i] = re.search(time_re, time[i]).group(0)
    comment[i] = re.search(num_re, comment[i]).group(0)
    view[i] = re.search(num_re, view[i]).group(0)
    # Print data
    print title[i], '\n', summary[i]
    print name[i], '\t', time[i], '\t', comment[i], '\t', view[i], '\n'

# generate a dictionary
data = {}
for i in range(len(time)):
    # take the order of a record as its key
    data[i] = []
    # append data to the key
    data[i].append({
        'view': view[i],
        'title': title[i],
        'summary': summary[i],
        'author': name[i],
        'comment': comment[i]
    })

# write data to a file in JSON format
with open('cnblogs_data.json', 'w') as outfile:
        json.dump(data, outfile)
