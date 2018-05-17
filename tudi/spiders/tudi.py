# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.http import FormRequest
from tudi.items import *
from bs4 import BeautifulSoup
from ..settings import SPIDER_DATE


class TudiEndSpider(scrapy.Spider):
    name = 'tudi'
    allowed_domains = ['www.landchina.com']
    start_urls = ['http://www.landchina.com/default.aspx?tabid=263&ComName=default']

    headers = {
        'Host': 'www.landchina.com',
        'Proxy-Connection': 'keep-alive',
        # 'Content-Length': '3122',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://www.landchina.com',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://www.landchina.com/default.aspx?tabid=263&ComName=default',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    #爬取日期
    date = SPIDER_DATE
    spider_date = '9f2c3acd-0256-4da2-a659-6949c4671a2a:' + date

    def start_requests(self):

        yield scrapy.FormRequest(
            url='http://www.landchina.com/default.aspx?tabid=263&ComName=default',
            # headers=self.headers,
            formdata={'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                                                       'TAB_QuerySubmitConditionData': self.spider_date,
                                                       'TAB_QuerySubmitPagerData': '1'},
            callback=self.parse_page)

    def parse_page(self, response):
        urldomain = 'http://www.landchina.com/'
        bs = BeautifulSoup(response.text, 'lxml')
        info_list = bs.select('tr[class=gridItem],tr[class=gridAlternatingItem]')

        for info in info_list:
            item = TudiItem()
            item['ordnum'] = re.sub(r'(\d)\.',r'\1',info.find_all('td')[0].text.strip())
            full_url=urldomain + info.a['href']
            item['totalUrl']=full_url
            print(full_url)

            yield Request(url=full_url, meta={'item': item}, callback=self.parse_item, dont_filter=True)

        # 下一页的跳转
        nowpage = response.xpath('//tr/td[@class="pager"][2]/span[1]/text()').extract()[0]
        print('------当前页',nowpage)
        nextpage = int(nowpage) + 1
        str_nextpage = str(nextpage)
        nextLink = response.xpath('//tr/td[@class="pager"][2]/a[last()-1]/@onclick').extract()
        # if len(nextLink):
        if nextpage<4:
            yield scrapy.FormRequest(
            url = 'http://www.landchina.com/default.aspx?tabid=263&ComName=default',formdata={
                                                               'TAB_QueryConditionItem': '9f2c3acd-0256-4da2-a659-6949c4671a2a',
                                                               'TAB_QuerySubmitConditionData': self.spider_date,
                                                               # 'TAB_QuerySubmitPagerData': '2'
                                                               'TAB_QuerySubmitPagerData': str_nextpage
                                                           },
                # headers=self.headers,
                callback=self.parse_page,dont_filter=True
            )

    def parse_item(self, response):
        item = response.meta['item']
        # print('222222',item)
        try:
            item['country'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['country'] = 'None'
            print('异常===',e)
        try:
            item['num'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['num'] = 'None'
        try:
            item['myname'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['myname'] = 'None'
        try:
            item['address'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['address'] = 'None'
        try:
            item['area'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['area'] = 'None'
        try:
            item['myuse'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['myuse'] = 'None'
        try:
            item['way'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['way'] = 'None'
        try:
            item['price'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['price'] = 'None'
        try:
            item['person'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['person'] = 'None'
        try:
            item['start'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['start'] = 'None'
        try:
            item['finish'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['finish'] = 'None'
        try:
            item['compact'] = response.xpath(
                '//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl"]/text()').extract()[0]
        except Exception as e:
            item['compact'] = 'None'
        yield item