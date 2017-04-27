# encoding=utf8

from selenium import webdriver
import BeautifulSoup
import re
import time
import json
# Created by Gao Dashan 2017/4/27

# This crawler is based on simulating browser clicking behavior to turn to next page by utilizing selenium.
# Due to the slow displaying process of the browser, this program runs quite slow and occasionally appears
# unstable.
# The Multipage_cnblogs_clawler.py used urllib and is thus much faster.


def crwal(soup, page_index):
    # param: soup: web page data to be analysised
    #        page_index: the page index of current page.
    post_list_div = soup.find(attrs={"id": "post_list"})
    titlelnk = post_list_div.findAll(attrs={"class": "titlelnk"})
    post_item_summary = post_list_div.findAll(attrs={"class": "post_item_summary"})
    post_item_foot = post_list_div.findAll(attrs={"class": "post_item_foot"})
    lightblue = post_list_div.findAll(attrs={"class": "lightblue"})
    article_comment = post_list_div.findAll(attrs={"class": "article_comment"})
    article_view = post_list_div.findAll(attrs={"class": "article_view"})
    # get the link index of next page
    paging = soup.find(attrs={"id": "paging_block"})
    next_pages = paging.findAll(attrs={"class": "pager"})
    next_p = len(next_pages[0].contents)-1
    # get the index of the current page
    href = next_pages[0].contents[next_p]['href']
    href_ind = href.lstrip('/sitehome/p/')
    href_ind = str(int(href_ind) - 1)
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
,    for i in range(length):
        time[i] = re.search(time_re, time[i]).group(0)
        comment[i] = re.search(num_re, comment[i]).group(0)
        view[i] = re.search(num_re, view[i]).group(0)
        # Print data
        print 'Title:', title[i], '\n', 'Abstract:', summary[i]
        print 'Author:', name[i], '\t', 'Time:', time[i], '\t', 'Comment:', comment[i], '\t', 'View:', view[i], '\n'

    # read data from cnblogs_data_from_CCTP.json
    if page_index > 1:
        with open('cnblogs_data_from_CCTP.json', 'r') as in_file:
            data = json.load(in_file)
    else:
        data = {}
    for i in range(len(time)):
        # take the order of a record as its key
        data[href_ind+'_%d' % i] = []
        # append data to the key
        data[href_ind+'_%d' % i].append({
            'view': view[i],
            'title': title[i],
            'summary': summary[i],
            'author': name[i],
            'comment': comment[i],
            'time': time[i]
        })
    with open('cnblogs_data_from_CCTP.json', 'w') as outfile:
        json.dump(data, outfile)
    # return: next_p is the input of itera(next_index). It is the index to the next page.
    return next_p


def itera(next_page, pa):
    print '-------------------This is a divider-------------\n'
    st = '//*[@id="paging_block"]/div/a[' + '%d' % next_page + ']'
    driver.find_element_by_xpath(st).click()
    time.sleep(5)
    webdata2 = driver.page_source
    soup2 = BeautifulSoup.BeautifulSoup(webdata2)
    return crwal(soup2, pa)


if __name__ == '__main__':
    crawl_page_number = 4  # Crawl 4 pages here as illustration
    page_index = 0
    driver = webdriver.Chrome()
    a = 'http://www.cnblogs.com'
    driver.get(a)
    webdata = driver.page_source
    soup1 = BeautifulSoup.BeautifulSoup(webdata)
    next_page = crwal(soup1, 1)
    for i in range(crawl_page_number - 1):
        next_page = itera(next_page, i + 2)


