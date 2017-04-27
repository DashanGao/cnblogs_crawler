# encoding=utf8

import BeautifulSoup
import re
import json
import urllib
import threading
import Queue
from multiprocessing import cpu_count
import time
# Created by Gao Dashan 2017/4/27
# This is a multi thread crawler designed to crawl posts data from "www.cnblogs.com"
# The number of pages to be crawled can be determined from 1 to 200.

crawl_page_number = 200  # Number of pages to be crawled.
thread_number = cpu_count()*2  # Number of threads
exit_flag = 0


class crawlThread(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        while not exit_flag:
            print self.name
            iterate_crawl()


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
        # # Print data
        # print 'Title:', title[i], '\n', 'Abstract:', summary[i]
        # print 'Author:', name[i], '\t', 'Time:', time[i], '\t', 'Comment:', comment[i], '\t', 'View:', view[i], '\n'

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
            'comment': comment[i],
            'time': time[i]
        })

    # JSON file IO
    file_lock.acquire()
    # Read data from JSON
    if page_index > 1:
        with open('Multithread_crawler_data.json', 'r') as in_file:
            data0 = json.load(in_file)
        in_file.close()
    else:
        data0 = {}
    data0.update(data)
    # Write data to JSON
    with open('Multithread_crawler_data.json', 'w') as out_file:
        json.dump(data0, out_file)
    out_file.close()
    # return: next_p is the input of itera(next_index). It is the index to the next page.
    file_lock.release()
    return


def iterate_crawl():
    # This function opens a new page and pass the webpage to process_web_page() to process.
    queue_lock.acquire()
    page_index = page_queue.get()
    queue_lock.release()
    print str(page_index) + '---------- time:' + str(time.clock()-start_time) + 's'
    target_url = 'http://www.cnblogs.com/sitehome/p/'+str(page_index+1)
    res = urllib.urlopen(target_url)
    soup2 = BeautifulSoup.BeautifulSoup(res)
    process_web_page(soup2, page_index+1)
    return


# record initial time
start_time = time.clock()
# lock for page queue
queue_lock = threading.Lock()
# page queue is used for maintaining a not accessed page list for threads
page_queue = Queue.Queue(crawl_page_number)
# JSON file lock
file_lock = threading.Lock()
# thread pool
threads = []
# write page numbers to queue
queue_lock.acquire()
for i in range(crawl_page_number):
    page_queue.put(i)
queue_lock.release()
threadID = 1
# create an empty file
with open('Multithread_crawler_data.json', 'w') as outfile:
    json.dump({}, outfile)
outfile.close()
# start threads, the number of threads is the minimum of thread number and page number.
for threadNum in range(min(thread_number, crawl_page_number)):
    thread = crawlThread(threadID)
    thread.start()
    threads.append(thread)
    threadID += 1

# wait for crawling.
while not page_queue.empty():
    pass
exit_flag = 1

for t in threads:
    t.join()

# print statistics
print str(crawl_page_number) + ' pages crawled.\n' + \
      str(min(thread_number, crawl_page_number)) + " threads\n" + \
      'Time elapsed: ' + str(time.clock()-start_time) + 's'

