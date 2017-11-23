# Spider
一个用python scrapy框架写的爬虫例子

本例子爬取的是豆瓣影评中的top250 的相关信息

<br>

### 关于Scrapy

* 官方文档-中文:https://scrapy-chs.readthedocs.io/zh_CN/stable/intro/tutorial.html
* Documents-ENG:https://docs.scrapy.org/en/latest/

<br>

### 安装

安装基于python 3

* Linux or mac

  ~~~shell
  pip3 install scrapy
  ~~~

* windows

  * 先下载Twisted模块：https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted

    选择对应的python版本和windows操作系统位数的whl文件下载

    比如我的机子是python35，windows64位系统，则下载了

    ~~~
    Twisted‑17.9.0‑cp35‑cp35m‑win_amd64.whl
    ~~~

    下载完后用pip 安装

    ~~~shell
    pip install Twisted‑17.9.0‑cp35‑cp35m‑win_amd64.whl
    ~~~

  * 安装scrapy

    ~~~shell
    pip install scrapy
    ~~~

  * 下载安装pywin32：https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/

    例如我下载的是

    ~~~
    pywin32-220.win-amd64-py3.5.exe
    ~~~

    双击exe安装即可


<br>

### 关于本例子

  本例子爬取豆瓣电影TOP 250 的信息

####代码结构说明：

* Spider/items.py: 保存爬取到数据的容器

* Spider/pipelines.py: 处理爬取到的数据，这里我写了三种处理数据的类，可自己选择使用

  * MoviePipeline类：调用scrapy提供的json exporter 导出 json 格式数据

  * MoviePipeline2类：用json模块自定义导出 json 格式数据

  * MoviePipeline3类：将数据导入到mysql

  * 若想使用某一个类， 我这里默认使用了MoviePipeline2,则需要在settings.py中加入如下代码:

    ~~~ python
    ITEM_PIPELINES = {
       'Spider.pipelines.MoviePipeline2': 300,
    }
    ~~~

    后面的数据是优先级，如果要执行多个不同的pipeline 类，优先级小的先执行

* Spider/setting.py: 一些设置

  * 为防止有些文件不能被扒，先设置不遵守robots协议

    ~~~python
    ROBOTSTXT_OBEY = False
    ~~~


  * 加入了导出数据到文件时使用utf-8编码

    ~~~python
    FEED_EXPORT_ENCODING = 'utf-8'
    ~~~

* Spider/spiders/MovieSpider.py：自定义的爬虫

#### 运行

* 在根目录下：

  ~~~ shell
  scrapy crawl movie
  ~~~

  得到了导出的json格式数据 data.json

<br>

### 伪装代理

有的网站有反扒功能, 这时需要我们伪装自己，提供两种方法, 本例子默认使用第二种方法

* 加入浏览器的头信息

  * 在setting.py中加入以下内容

    ~~~python
    USER_AGENT_LIST = ['zspider/0.9-dev http://feedback.redkolibri.com/',
                        'Xaldon_WebSpider/2.0.b1',
                        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) Speedy Spider (http://www.entireweb.com/about/search_tech/speedy_spider/)',
                        'Mozilla/5.0 (compatible; Speedy Spider; http://www.entireweb.com/about/search_tech/speedy_spider/)',
                        'Speedy Spider (Entireweb; Beta/1.3; http://www.entireweb.com/about/search_tech/speedyspider/)',
                        'Speedy Spider (Entireweb; Beta/1.2; http://www.entireweb.com/about/search_tech/speedyspider/)',
                        'Speedy Spider (Entireweb; Beta/1.1; http://www.entireweb.com/about/search_tech/speedyspider/)',
                        'Speedy Spider (Entireweb; Beta/1.0; http://www.entireweb.com/about/search_tech/speedyspider/)',
                        'Speedy Spider (Beta/1.0; www.entireweb.com)',
                        'Speedy Spider (http://www.entireweb.com/about/search_tech/speedy_spider/)',
                        'Speedy Spider (http://www.entireweb.com/about/search_tech/speedyspider/)',
                        'Speedy Spider (http://www.entireweb.com)',
                        'Sosospider+(+http://help.soso.com/webspider.htm)',
                        'sogou spider',
                        'Nusearch Spider (www.nusearch.com)',
                        'nuSearch Spider (compatible; MSIE 4.01; Windows NT)',
                        'lmspider (lmspider@scansoft.com)',
                        'lmspider lmspider@scansoft.com',
                        'ldspider (http://code.google.com/p/ldspider/wiki/Robots)',
                        'iaskspider/2.0(+http://iask.com/help/help_index.html)',
                        'iaskspider',
                        'hl_ftien_spider_v1.1',
                        'hl_ftien_spider',
                        'FyberSpider (+http://www.fybersearch.com/fyberspider.php)',
                        'FyberSpider',
                        'everyfeed-spider/2.0 (http://www.everyfeed.com)',
                        'envolk[ITS]spider/1.6 (+http://www.envolk.com/envolkspider.html)',
                        'envolk[ITS]spider/1.6 ( http://www.envolk.com/envolkspider.html)',
                        'Baiduspider+(+http://www.baidu.com/search/spider_jp.html)',
                        'Baiduspider+(+http://www.baidu.com/search/spider.htm)',
                        'BaiDuSpider',
                        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0) AddSugarSpiderBot www.idealobserver.com',
                       ]
    ~~~

  * 在spider同级目录下建立一个MidWare文件夹里面 写一个HeaderMidWare.py 内容为：

    ~~~python
    # encoding: utf-8
    from scrapy.utils.project import get_project_settings
    import random

    settings = get_project_settings()

    class ProcessHeaderMidware():
        """process request add request info"""

        def process_request(self, request, spider):
            """
            随机从列表中获得header， 并传给user_agent进行使用
            """
            ua = random.choice(settings.get('USER_AGENT_LIST'))  
            spider.logger.info(msg='now entring download midware')
            if ua:
                request.headers['User-Agent'] = ua
                # Add desired logging message here.
                spider.logger.info(u'User-Agent is : {} {}'.format(request.headers.get('User-Agent'), request))
            pass
    ~~~

  * 在setting.py中添加

    ~~~python
    DOWNLOADER_MIDDLEWARES = {
        'Spider.MidWare.HeaderMidWare.ProcessHeaderMidware': 543,
    }
    ~~~

* 使用fake_userAgent

  * 安装fake_userAgent

    ~~~python
    pip install fake-useragent
    ~~~

  * 在spider同级目录下建立一个MidWare文件价里面写一个user_agent_middlewares.py文件内容为

    ~~~python
    # -*- coding: utf-8 -*-
    from fake_useragent import UserAgent

    class RandomUserAgentMiddlware(object):
        #随机跟换user-agent
        def __init__(self,crawler):
            super(RandomUserAgentMiddlware,self).__init__()
            self.ua = UserAgent()
            self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')#从setting文件中读取RANDOM_UA_TYPE值

        @classmethod
        def from_crawler(cls,crawler):
            return cls(crawler)

        def process_request(self,request,spider):  ###系统电泳函数
            def get_ua():
                return getattr(self.ua,self.ua_type)
            # user_agent_random=get_ua()
            request.headers.setdefault('User_Agent',get_ua())
            pass
    ~~~

  * 在setting.py中添加

    ~~~python
    RANDOM_UA_TYPE = 'random'##random    chrome
    DOWNLOADER_MIDDLEWARES = {
    　　'projectName.MidWare.user_agent_middlewares.RandomUserAgentMiddlware': 543, 
      　'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    }
    ~~~

    ​