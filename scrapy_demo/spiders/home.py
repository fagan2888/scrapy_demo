# -*- coding: utf-8 -*-
import scrapy
import urllib.parse
from scrapy_demo.items import ScrapyDemoItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join


class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['http://172.28.128.1:9312']
    start_urls = ['http://172.28.128.1:9312/properties/index_00000.html']

    def parse(self, response):
        # self.log('title: %s' % response.xpath('//*[@itemprop="name"][1]/text()').extract())
        # self.log('price: %s' % response.xpath('//*[@itemprop="price"][1]/text()').re('[.0-9]+'))
        # self.log('description: %s' % response.xpath('//*[@itemprop="description"][1]/text()').extract())
        # self.log('address: %s' % response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract())
        # self.log('image_urls: %s' % response.xpath('//*[@itemprop="image"][1]/@src').extract())

        # 创建一个新的item
        # item = ScrapyDemoItem()
        # item['title'] = response.xpath('//*[@itemprop="name"][1]/text()').extract()
        # item['price'] = response.xpath('//*[@itemprop="price"][1]/text()').re('[.0-9]+')
        # item['description'] = response.xpath('//*[@itemprop="description"][1]/text()').extract()
        # item['address'] = response.xpath('//*[@itemtype="http://schema.org/Place"][1]/text()').extract()
        # item['images'] = response.xpath('//*[@itemprop="image"][1]/@src').extract()
        # # 使用yield返回,而非return item
        # yield item

        # 使用item装载器ItemLoader
        # 使用MapCompose处理器
        ld = ItemLoader(item=ScrapyDemoItem(), response=response)
        ld.add_xpath('title', '//*[@itemprop="name"][1]/text()', MapCompose(str.strip, str.title))
        ld.add_xpath('price', '//*[@itemprop="price"][1]/text()', MapCompose(lambda i: i.replace(',', ''), float), re='[,.0-9]+')
        ld.add_xpath('description', '//*[@itemprop="description"][1]/text()', MapCompose(str.strip), Join())
        ld.add_xpath('address', '//*[@itemtype="http://schema.org/Place"][1]/text()', MapCompose(str.strip))
        ld.add_xpath('images', '//*[@itemprop="image"][1]/@src', MapCompose(lambda i: urllib.parse.urljoin(response.url, i)))

        yield ld.load_item()
