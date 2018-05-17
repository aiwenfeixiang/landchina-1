# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

class TudiPipeline(object):

    tudiInsert = '''insert into tudi(totalUrl,ordnum,country,address,area,myuse,way,compact)values('{totalUrl}','{ordnum}','{country}','{address}','{area}','{myuse}','{way}','{compact}')'''
    tudiInsert2 = '''insert into tudi_detail(country,num,myname,address,area,myuse,way,price,person,start,finish,compact)values('{country}','{num}','{myname}','{address}','{area}','{myuse}','{way}','{price}','{person}','{start}','{finish}','{compact}')'''


    def __init__(self, settings):
        self.settings = settings

    def process_item(self, item, spider):
        # print('+++++++++',item)
        sqltext = self.tudiInsert.format(
            totalUrl=pymysql.escape_string(item['totalUrl']),
            country=pymysql.escape_string(item['country']),
            address=pymysql.escape_string(item['address']),
            area=pymysql.escape_string(item['area']),
            myuse=pymysql.escape_string(item['myuse']),
            way=pymysql.escape_string(item['way']),
            compact=pymysql.escape_string(item['compact']),
            ordnum=pymysql.escape_string(item['ordnum'])
        )
        sqltext2 = self.tudiInsert2.format(
            totalUrl=pymysql.escape_string(item['totalUrl']),
            country=pymysql.escape_string(item['country']),
            num=pymysql.escape_string(item['num']),
            myname=pymysql.escape_string(item['myname']),
            address=pymysql.escape_string(item['address']),
            area=pymysql.escape_string(item['area']),
            myuse=pymysql.escape_string(item['myuse']),
            way=pymysql.escape_string(item['way']),
            price=pymysql.escape_string(item['price']),
            person=pymysql.escape_string(item['person']),
            start=pymysql.escape_string(item['start']),
            finish=pymysql.escape_string(item['finish']),
            compact=pymysql.escape_string(item['compact']),
            )
    # spider.log(sqltext)

        self.cursor.execute(sqltext)
        self.cursor.execute(sqltext2)

        return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        # 连接数据库
        self.connect = pymysql.connect(
            host=self.settings.get('MYSQL_HOST'),
            port=self.settings.get('MYSQL_PORT'),
            db=self.settings.get('MYSQL_DBNAME'),
            user=self.settings.get('MYSQL_USER'),
            passwd=self.settings.get('MYSQL_PASSWD'),
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
