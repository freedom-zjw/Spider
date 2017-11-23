# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
import codecs
from scrapy.exporters import JsonItemExporter


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


"""
下面为两种导出json的方式，第一种导出一个数组，数组每个元素是一个json格式的dict
第二种是直接每一行是一个json格式的dict
"""


class MoviePipeline(object):
    # 调用scrapy 提供的 json exporter 导出 json 文件
    def __init__(self):
        self.file = open('data.json', 'wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        # 开启倒数
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    # 将Item实例导出到json文件
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
        

class MoviePipeline2(object):
    # 自定义导出json
    def __init__(self):
        self.file = codecs.open('data2.json', 'w', encoding='utf-8')
    
    # 处理结束后关闭文件IO流
    def close_spider(self, spider):
        self.file.close()
    
    # 将Item实例导出到json文件
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item


class MoviePipeline3(object):
    # 将数据存储到mysql
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='***', passwd='***', db='***',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.cursor.execute("truncate table Movie")
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            self.cursor.execute("insert into Movie (name,movieInfo,star,quote) VALUES (%s,%s,%s,%s)", (
                item['title'], item['movieInfo'], item['star'], item['quote']))
            self.conn.commit()
        except pymysql.Error:
            print("Error%s,%s,%s,%s" % (item['title'], item['movieInfo'], item['star'], item['quote']))
        return item
     