# -*- coding: utf-8 -*-
import scrapy,json
from scrapy import Spider,Request
from urllib.parse import urlencode
from scrapy_test.items import ImageItem


class Image360Spider(scrapy.Spider):
    name = 'image360'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def start_requests(self):
        data = {'ch':'beauty','listtype':'new'}
        base_url = 'http://image.so.com/zj?'
        for page in range(1,self.settings.get('MAX_PAGE') + 1):
            # print('------第%s页'%page)
            data['sn'] = page * 30
            #将字典转化为url的get参数
            params = urlencode(data)
            # print(params)
            url = base_url + params
            yield Request(url,self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            yield item