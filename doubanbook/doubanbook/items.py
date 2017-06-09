# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanbookItem(scrapy.Item):
	name=scrapy.Field()#书名
	url=scrapy.Field()#网址
	year=scrapy.Field()#出版年份
	publishing=scrapy.Field()#出版社
	author=scrapy.Field()#作者
	tags=scrapy.Field()#分类
	score=scrapy.Field()#豆瓣分数
	people=scrapy.Field()#评价人数