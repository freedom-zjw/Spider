# -*- coding: utf-8 -*-
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
from Spider.items import MovieItem


class MovieSpider(scrapy.Spider):
    """
    name:用于区别spider,名字必须唯一
    allowed_domains: 允许扒取的域名
    start_urls: Spider在启动时进行爬取的url列表,
                后续的url可从初始的url获取的数据中提取
    parse():是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 
            Response 对象将会作为唯一的参数传递给该函数。 该方法负责解
            析返回的数据(response data)，提取数据(生成item)以及生成需
            要进一步处理的URL的 Request 对象。
    """
    name = 'movie'
    url = 'https://movie.douban.com/top250'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        item = MovieItem()
        selector = scrapy.Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for movie in movies:
            # 提取电影标题
            title = movie.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each
            # 提取电影简要介绍
            movieInfo = movie.xpath('div[@class="bd"]/p/text()').extract()
            # 提取电影评分
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/ \
                                span[@class="rating_num"]/text()').extract()[0]
            # 提取电影概括
            quote = movie.xpath('div[@class="bd"]/p/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = ';'.join(movieInfo).replace(' ', '').replace('\n', '')
            item['star'] = star[0]
            item['quote'] = quote
            yield item
        # 获取下一页的url
        nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextPage:
            nextPage = nextPage[0]
            print(self.url + str(nextPage))
            yield scrapy.Request(self.url + str(nextPage), callback=self.parse)
            """
            scrapy.http.Request([
                    url, 
                    callback, 
                    method='GET', 
                    headers, 
                    body, 
                    cookies, 
                    meta, 
                    encoding='utf-8', 
                    priority=0, 
                    dont_filter=False, 
                    errback
            ])
            parameters:
                  url(string): 用于请求的URL
                  callback(callable):指定一个回调函数，该回调函数以这个request的response作为第一个参数。
                                    如果未指定callback，则默认使用spider的parse()方法。
                  method(string):HTTP请求的方法，默认为GET（看到GET你应该明白了，过不不明白建议先学习urllib或者requets模块）
                  meta(dict):指定Request.meta属性的初始值。如果给了该参数，dict将会浅拷贝。(浅拷贝不懂的赶紧回炉)
                  body(str或unicode): 请求体。如果unicode传递了a，那么它被编码为 str使用传递的编码（默认为utf-8）。
                                     如果 body没有给出，则存储一个空字符串。不管这个参数的类型，存储的最终值将是一
                                    个str（不会是unicode或None）。
                  headers（dict） - 这个请求的头。dict值可以是字符串（对于单值标头）或列表（对于多值标头）。
                  如果 None作为值传递，则不会发送HTTP头。
                  cookie（dict或list） - 请求cookie。这些可以以两种形式发送：
                    1、使用dict:
request_with_cookies = Request(url="http://www.example.com", cookies={'currency': 'USD', 'country': 'UY'})
                    2、使用字典的list
request_with_cookies = Request(url="http://www.example.com",
                               cookies=[{'name': 'currency',
                                        'value': 'USD',
                                        'domain': 'example.com',
                                        'path': '/currency'}])
                    后面这种形式可以定制cookie的domain和path属性，只有cookies为接下来的请求保存的时候才有用。
                    当网站在response中返回cookie时，这些cookie将被保存以便未来的访问请求。这是常规浏览器的行为。如果你想避免修改当前
                    正在使用的cookie,你可以通过设置Request.meta中的dont_merge_cookies为True来实现。
request_with_cookies = Request(url="http://www.example.com",
                               cookies={'currency': 'USD', 'country': 'UY'},
                               meta={'dont_merge_cookies': True})
                    encoding(string):请求的编码， 默认为utf-8
                    priority(int):请求的优先级
                    dont_filter(boolean):指定该请求是否被 Scheduler过滤。该参数可以是request重复使用（Scheduler默认过滤重复请求）。谨慎使用！！
                    errback(callable):处理异常的回调函数。
            """