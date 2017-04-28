# -*- coding: utf-8 -*-
# 采集诗词工具类

from ext import db as mysql_db

from bs4 import BeautifulSoup
import requests
import re

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
import random

headers = {
    'User-Agent': random.choice(USER_AGENTS),
    'Referer': 'www.baidu.com'}


class Ci(mysql_db.Model):  # 古诗词
    __tablename__ = 'dt_boot_ci'
    id = mysql_db.Column(mysql_db.Integer, primary_key=True)
    title = mysql_db.Column(mysql_db.String(256))
    author = mysql_db.Column(mysql_db.String(256))
    dynasty = mysql_db.Column(mysql_db.String(256))
    content = mysql_db.Column(mysql_db.BLOB)
    media = mysql_db.Column(mysql_db.String(256))


def SpliderDetail(detail_url,proxy):
    if detail_url is None:
        return
    bs_detail = BeautifulSoup(requests.get(url=detail_url,headers=headers,proxies=proxy).content, 'lxml')
    title = str(bs_detail.select_one(
        'body > div.main3 > div.shileft > div.son1 > h1'))  # body > div.main3 > div.shileft > div.son1 > h1
    dynasty = str(bs_detail.select_one(
        'body > div.main3 > div.shileft > div.son2 > p '))  # body > div.main3 > div.shileft > div.son2 > p:nth-child(2)
    author = str(bs_detail.select_one('body > div.main3 > div.shileft > div.son2 > p + p  > a'))
    content = str(bs_detail.select_one('body > div.main3 > div.shileft > div.son2 > div.cont'))[29:-6]
    print(content)
    if author == 'None':
        author = str(bs_detail.select_one(
            'body > div.main3 > div.shileft > div.son2 > p + p  '))  # body > div.main3 > div.shileft > div.son2 > p:nth-child(2)
    # re_ti = re.search(r'<h1>[\u4E00-\u9FFF]+·?[\u4E00-\u9FFF]+</h1>', title)
    re_dy = re.search(r'</span>[\u4E00-\u9FFF]+</p>', dynasty)
    re_au = re.search(r'>[\u4E00-\u9FFF]+<', author)

    title_rs = '未知'
    author_rs = '未名'
    dynasty_rs = '未知'
    title_rs = title[4:-5]

    if re_dy:
        dynasty_rs = re_dy.group(0)[7:-4]

    if re_au:
        author_rs = re_au.group(0)[1:-1]

    ci = Ci()
    ci.title = title_rs.encode('utf-8')
    ci.author = author_rs.encode('utf-8')
    ci.dynasty = dynasty_rs.encode('utf-8')
    ci.content = content.encode('utf-8')
    ci.media = ''
    mysql_db.session.add(ci)
    mysql_db.session.commit()
    print(title_rs + '--' + dynasty_rs.replace("\n", "") + '--' + author_rs.replace("\n", ""))


import time


def CiSplider(ci_url='http://so.gushiwen.org/type.aspx?p=1', proxy={}, header={}):
    bs = BeautifulSoup(requests.get(url=ci_url, proxies=proxy, headers=header).content, 'lxml')
    for item in bs.find_all(attrs={"class": "sons"}):
        m = re.search(r'<p><a href="/\w+.aspx', str(item))
        if m:
            SpliderDetail('http://so.gushiwen.org/' + m.group(0).split('/')[1],proxy)
        time.sleep(1)

        # if __name__ == '__main__':
        #     CiSplider()
