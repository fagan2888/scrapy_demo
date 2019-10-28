# -*- coding: utf-8 -*-
import scrapy
from scrapy_demo.items import ScrapyDemoItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
import urllib.parse
import socket
import datetime
import re


class ManualSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['172.28.128.1:9312']
    start_urls = ['http://172.28.128.1:9312/properties/index_00000.html']

    def parse(self, response):
        # 获取下一页
        next_selector = response.xpath('//*[contains(@class,"next")]//@href')
        for url in next_selector.extract():
            mc = re.search(r'\d+', url)
            page = int(mc.group(0))
            # 限制页数
            if page > 2:
                break
            yield scrapy.Request(urllib.parse.urljoin(response.url, url), dont_filter=True)

        # 获取列表项目
        item_selector = response.xpath('//*[@itemprop="url"]/@href')
        for url in item_selector.extract():
            yield scrapy.Request(urllib.parse.urljoin(response.url, url), callback=self.parse_item)

    def parse_item(self, response):
        """ This function parse_item a property page.

        @url http://172.28.128.1:9312/properties/index_00000.html
        @returns items 1
        @scrapes title price description address images
        @scrapes url project spider server date        
        """

        # 使用item装载器ItemLoader
        # 使用MapCompose处理器
        ld = ItemLoader(item=ScrapyDemoItem(), response=response)
        ld.add_xpath('title', '//*[@itemprop="name"][1]/text()', MapCompose(str.strip, str.title))
        ld.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',', ''), float), re='[,.0-9]+')
        ld.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(str.strip), Join())
        ld.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()', MapCompose(str.strip))
        ld.add_xpath('images', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i: urllib.parse.urljoin(response.url, i)))

        # 使用add_value添加单个值
        ld.add_value('url', response.url)
        ld.add_value('project', self.settings.get('BOT_NAME'))
        ld.add_value('spider', self.name)
        ld.add_value('server', socket.gethostname())
        ld.add_value('date', datetime.datetime.now())

        yield ld.load_item()
