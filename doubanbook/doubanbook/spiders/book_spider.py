# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from doubanbook.items import DoubanbookItem
import re

class MoiveSpider(CrawlSpider):
    name="book"
    allowed_domains=["book.douban.com"]
    start_urls=["https://book.douban.com/tag/%E7%88%B1%E6%83%85"]
    rules=[
        Rule(SgmlLinkExtractor(allow=(r'https://book.douban.com/tag/.*?\?start=\d+.*'))),
        Rule(SgmlLinkExtractor(allow=(r'https://book.douban.com/subject/[\d]+/?$')),callback="parse_item"),      
    ]

    def parse_item(self,response):
        type_out = True
        sel=Selector(response)
        item=DoubanbookItem()
        item['name']=sel.xpath('//*[@id="wrapper"]/h1/span/text()').extract()[0]
        item['url']=response.url
        try:
            item['author']=sel.xpath('//*[@id="info"]/a[1]/text()').extract()[0]
        except Exception,e:
            type_out = False
            item['author']=sel.xpath('//*[@id="info"]/span[1]/a/text()').extract()[0]
        try:
            item['year'] = re.search(r'<span class="pl">出版年:</span> ([-\d]+)',response.body).group(1)
        except:
            item['year'] = "未知";
        # item['year']=sel.xpath('//*[@id="info"]/span[2]/following-sibling::text()').extract()[0]
        item['publishing']=sel.xpath('//*[@id="info"]/span[2]/following-sibling::text()').extract()[0]
        item['tags']= sel.xpath('//*[@id="db-tags-section"]/div/span/a/text()').extract()
        item['score']= sel.xpath('//*[@id="interest_sectl"]/div/div[2]/strong/text()').extract()[0]
        try:
            item['people']= sel.xpath('//*[@id="interest_sectl"]/div/div[2]/div/div[2]/span/a/span/text()').extract()[0]
        except Exception,e:
            item['people']= "0"
        return item