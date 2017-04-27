# encoding=utf8

import BeautifulSoup
import re
import json
import urllib
# Created by Gao Dashan 2017/4/27
# This is a single thread crawler designed to crawl posts data from "www.cnblogs.com"
# The number of pages to be crawled can be determined from 1 to 200.


def process_web_page(soup, page_index):
    # param: soup: web page data to be analysised
    #        page_index: the page index of current page.
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
    # process data
    for i in range(length):
        title[i] = titlelnk[i].string.strip()
        summary[i] = post_item_summary[i].contents[len(post_item_summary[i].contents) - 1].string.strip()
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
        print 'Title:', title[i], '\n', 'Abstract:', summary[i]
        print 'Author:', name[i], '\t', 'Time:', time[i], '\t', 'Comment:', comment[i], '\t', 'View:', view[i], '\n'

    # Read data from JSON
    if page_index > 1:
        with open('Multiage_cnblogs_crawler_data.json', 'r') as in_file:
            data = json.load(in_file)
    else:
        data = {}

    # Generate JSON data for each record.
    for i in range(len(time)):
        # take the order of a record as its key
        data[str(page_index)+'_%d' % i] = []
        # append data to the key
        data[str(page_index)+'_%d' % i].append({
            'view': view[i],
            'title': title[i],
            'summary': summary[i],
            'author': name[i],
            'comment': comment[i]
        })

    # Write data to JSON
    with open('Multiage_cnblogs_crawler_data.json', 'w') as outfile:
        json.dump(data, outfile)
    # return: next_p is the input of itera(next_index). It is the index to the next page.
    return


def itera(page_index):
    # This function opens a new page and pass the webpage to process_web_page() to process.
    print '-------------------Page ' + str(page_index+1) + ' ---------------\n'
    target_url = 'http://www.cnblogs.com/sitehome/p/'+str(page_index+1)
    res = urllib.urlopen(target_url)
    soup2 = BeautifulSoup.BeautifulSoup(res)
    process_web_page(soup2, page_index+1)
    return


if __name__ == '__main__':
    crawl_page_number = 20  # Number of page to be crawled.
    for i in range(crawl_page_number):
        itera(i)


