# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TudiItem(scrapy.Item):
    totalUrl=scrapy.Field()
    ordnum=scrapy.Field()
    country = scrapy.Field()
    num = scrapy.Field()
    myname = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    myuse = scrapy.Field()
    way = scrapy.Field()
    price = scrapy.Field()
    person = scrapy.Field()
    start = scrapy.Field()
    finish = scrapy.Field()
    compact = scrapy.Field()
