# cnblogs crawler
Author: Gao Dashan  
Time: 2017/4/27   
## Abstract
This project develops simple web crawlers which can crawl data about articles from "www.cnblogs.com" and store them in a JSON file. Four versions were implemented as following:

### V1 single page crawler:    
This crawler crawl data from the main page of "www.cnblogs.com" and write data to json file naemd 'blogs_data.json', it also print out data in console.  
**Libraries** used: urllib, BeautifulSoup, re, json    
Each article has a number as its key in the json file.   
Each article data is organized in a form:   
```python
    'key_number': {
        'view': view[i],
        'title': title[i],
        'summary': summary[i],
        'author': name[i],
        'comment': comment[i],
        'time': time[i]
    }
```
Console output demo:  
![console](https://github.com/GaoDashan1/cnblogs_crawler/blob/master/V1_p1.png)
### V2 multipage crawler 1:   
In order to access the next page of the main page, I initially choose to simulate the **click behavior** by means of utilizing a webdrive from selenium. However, the display of the web page became a bottleneck. Though a webdriver without displaying the web page is available, I turn to another approach after I found appending the href attribute of the tab to the mian page url can also work.  
**Libraries** used: BeautifulSoup, re, json, selenium  
### V3 multipage crawler 2:  
In this program the urllib library comes back. It directly get access to any page by:  
```python
    target_url = 'http://www.cnblogs.com/sitehome/p/'+str(page_index+1)  # page_index+1: webpage number
    res = urllib.urlopen(target_url)
    soup = BeautifulSoup.BeautifulSoup(res)
    process_web_page(soup, page_index+1)
 ```
### V4 multithread crawler:   
Based on V3, multithread is added to largly improve the profermance. The **"V4_data_MultiThread_crawled.json"** file contains data crawled from 200 pages, which is more than 3M.   
Console output demo:  
![V4](https://github.com/GaoDashan1/cnblogs_crawler/blob/master/V4_p1.png)
![V4](https://github.com/GaoDashan1/cnblogs_crawler/blob/master/V4_p3.png)

JSON demo:  
Key formate: pageNumber_postNumber, eg: 121_14 : page 121, 15th post.  
![json](https://github.com/GaoDashan1/cnblogs_crawler/blob/master/V4_p2.png)
