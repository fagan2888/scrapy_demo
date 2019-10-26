# -*- coding: utf-8 -*-
import scrapy


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # 执行爬取 scrapy crawl basic
    # 提取并保存数据 scrapy crawl basic -o basic.json
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'toscrape-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        # 分析提取数据
        for quote in response.css('div.quote'):
            yield {
                'title': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
