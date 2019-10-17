# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request
from bs4 import BeautifulSoup
from ScUniversity.items import ScUniversityItem

class ScUniversitySpider(scrapy.Spider):
    name = 'ScUniversity'
    allowed_domains = ['college.gaokao.com']
    start_urls = ['http://college.gaokao.com/schlist']

    #def __init__(self):

    def start_requests(self):
        print('爬取高校')
        for i in range(1, 108):
            print('正在下载第%s业数据' % i)
            self.url = 'http://college.gaokao.com/schlist/p%s' % i
            yield Request(self.url, self.parse)

    def parse(self, response):

        html = response.text
        soup = BeautifulSoup(html,"html5lib")

        div_a_alluniver = soup.find('div',class_ = 'scores_List')

        item = ScUniversityItem()

        if div_a_alluniver is not None:
            for dl_univeritem in div_a_alluniver.find_all('dl'):
                    if dl_univeritem is not None:
                        strong = dl_univeritem.find('strong')['title']
                        li = dl_univeritem.find_all('li')
                        item['univername'] = strong
                        item['univerlocadd'] = li[0].text[6:]
                        item['univertype'] = li[2].text[5:]
                        item['univerproper'] = li[4].text[5:]
                        item['univerdist'] = li[1].text[5:]
                        item['univerfrom'] = li[3].text[5:]
                        item['univerurl'] = li[5].text[5:]
                        yield item
                        time.sleep(1)




