# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors


class DoubanbookPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                db = 'craw',
                user = 'root',
                passwd = '123456',
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',
                use_unicode = False
        )
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    def compress(self,tags):
    	res = ""
    	lenTags=len(tags)
        for n in xrange(lenTags):
            res+=tags[n]
            if n<lenTags-1:
                res+='/'
        return res
    def _conditional_insert(self,tx,item):
		log.msg(item,level=log.DEBUG)
		tx.execute("select * from book where name= %s",(item['name'],))
		result=tx.fetchone()
		if result:
			log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
		else:
			tags=self.compress(item['tags'])
			item['author'] = ''.join(item['author'].split())
			item['author'] = item['author'].replace("[","").replace("]",".")
			print \
			"insert into book (name,url,year,publishing,author,tags,score,people) values ('%s','%s','%s','%s','%s','%s','%s','%s')"%\
			    (item['name'],item['url'],item['year'],item['publishing'],item['author'],tags,float(item['score']),int(item['people']))
			tx.execute(\
			"insert into book (name,url,year,publishing,author,tags,score,people) values (%s,%s,%s,%s,%s,%s,%s,%s)",\
			(item['name'],item['url'],item['year'],item['publishing'],item['author'],tags,float(item['score']),int(item['people'])))
			log.msg("Item stored in db: %s" % item, level=log.DEBUG)

    def handle_error(self, e):
        log.err(e)