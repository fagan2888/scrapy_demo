# -*- coding: utf-8 -*-
import scrapy


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    #执行爬取 scrapy crawl basic
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'toscrape-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
