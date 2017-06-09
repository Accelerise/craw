# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import requests
import re
from lxml import etree

user_id = ""

# 去除标题中的非法字符 (Windows)
def validateTitle(title):
    rstr = ur"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title

def createDir():
    save_path = u"新浪博客抓取"+user_id
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path

def getUrls(myPage):
    pools = [];
    page_num = int(re.search(u'title="跳转至最后一页">(\d*)</a>', myPage).group(1))
    for i in range(1,page_num+1):
        url = "http://blog.sina.com.cn/s/articlelist_"+user_id+"_0_"+str(i)+".html"
        myPage = requests.get(url).content.decode("utf-8")
        dom = etree.HTML(myPage)
        urls = dom.xpath('//span[@class="atc_title"]/a/@href')
        for url in urls:
            pools.append(url)
    return pools

def downloadPosts(start_page,pools,save_path):
    num = int(re.search(u'<strong>全部博文</strong><em>\((\d*)\)</em>', start_page).group(1))
    for index in range(0,num):
        start_page = requests.get(pools[index]).content.decode("utf-8")
        title = re.search(r'class="titName SG_txta">(.*?)</h2>', start_page, re.S).group(1)
        title = validateTitle(title)
        time = re.search(r'<span class="time SG_txtc">\((.*?)\)</span>', start_page, re.S).group(1)
        post = re.search(ur'<!-- 正文开始 -->(.*?)<!-- 正文结束 -->', start_page, re.S).group(1)
        filename = unicode(str(index))+"_"+title
        
        path = save_path+"/"+filename+".html"
        print (u"downloading:"+title).encode('utf-8')
        with open(path, "w+") as fp:
            fp.write('<h1>%s</h1>\n<h5>%s</h5>\n source:<a href="%s">%s</a>\n%s' % (title.encode("utf-8"), time.encode("utf-8"), pools[index], pools[index], post.encode("utf-8")))

if __name__ == '__main__':
    print "start"
    # 从键盘读取博主ID
    user_id = str(raw_input(u'请输入将要爬取的新浪博主ID（数字）： '.encode('utf-8')))
    # 创建目录
    save_path = createDir()
    # 生成入口Url
    start_url = "http://blog.sina.com.cn/s/articlelist_"+user_id+"_0_1.html"
    # 获取入口页
    myPage = requests.get(start_url).content.decode("utf-8")
    # myPage = urllib2.urlopen(start_url).read().decode("utf-8")
    # 搜集Url
    pools = getUrls(myPage)
    # 下载文章
    downloadPosts(myPage,pools,save_path)
    print "end"