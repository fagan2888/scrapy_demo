# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_demo.items import ScrapyDemoItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
import urllib.parse
import socket
import datetime


class EasySpider(CrawlSpider):
    name = 'easy'
    # allowed_domains = ['http://172.28.128.1']
    start_urls = ['http://172.28.128.1:9312/properties/index_00000.html']

    # LinkExtractor专门用于抽取链接
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"next")]')),
        Rule(LinkExtractor(restrict_xpaths='//*[@itemprop="url"]'), callback='parse_item'),
    )

    def parse_item(self, response):
        """ This function parse_item a property page.

        @url http://172.28.128.1:9312/properties/index_00000.html
        @returns items 1
        @scrapes title price description address images
        @scrapes url project spider server date        
        """

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

        return ld.load_item()
